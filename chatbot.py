import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

session_context = {}

#Ek baar download hoga, after that skip ho jayega
nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("wordnet")

lemmatizer = WordNetLemmatizer()

def preprocess(text):
    # 1. Lowercase
    text = text.lower()

    #2. Punctuation/special character hatao (only kept a-z, 0-9, space)
    text = re.sub(r"[^a-z0-9\s]", "", text)

    # 3. Tokenize
    tokens = word_tokenize(text)

    # 4. Lemmatize (pehle noun, phir verb form)
    tokens = [
        lemmatizer.lemmatize(lemmatizer.lemmatize(word), pos="v")
        for word in tokens
    ]

    return " ".join(tokens)

import json
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

CONFIDENCE_THRESHOLD = 0.3
FALLBACK = "Sorry, I didn't understand that. Could you please rephrase?"

#intents.json load karo
with open("intents.json", encoding="utf-8") as f:
    data = json.load(f)


#Each pattern ko uske tag ke sath store kro
patterns = []
tags = []
required_contexts = [] #har pattern ke liye required context (ya None)

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        patterns.append(preprocess(pattern))
        tags.append(intent["tag"])
        required_contexts.append(intent.get("context_required"))

#TF - IDF vectorizer train karo
vectorizer = TfidfVectorizer()
pattern_vectors = vectorizer.fit_transform(patterns)

MIN_COVERAGE = 0.7 #user ke kam se kam 70% words vocabulary mei hona chahiye

def get_intent(user_message, session_id=None):
    cleaned = preprocess(user_message)

    #empty string (jaise Hindi script) ka direct fallback
    if not cleaned.strip():
        return None, 0.0

    #Coverage check: kitne words bot ko aate hai?
    analyzer = vectorizer.build_analyzer()
    words = analyzer(cleaned)

    if not words:
        return None, 0.0
    
    known = [w for w in words if w in vectorizer.vocabulary_]
    coverage = len(known) / len(words)

    if coverage < MIN_COVERAGE:
        return None, 0.0

    user_vector = vectorizer.transform([cleaned])
    scores = cosine_similarity(user_vector, pattern_vectors)[0]

    current_context = session_context.get(session_id)

    # Context-based intents only tab allowed hai jab context match kare
    for i, req in enumerate(required_contexts):
        if req is not None and req != current_context:
            scores[i] = 0.0

    best_index = scores.argmax()
    best_score = scores[best_index]

    if best_score < CONFIDENCE_THRESHOLD:
        return None, float(best_score)

    return tags[best_index], float(best_score)


def get_response(user_message, session_id=None):
    tag, score = get_intent(user_message, session_id)


    if tag is None:
        session_context.pop(session_id, None) # context reset
        return FALLBACK, "fallback", score

    for intent in data["intents"]:
        if intent["tag"] == tag:
            # Naya context set karo , ya old remove kro
            new_context = intent.get("context_set")
            if new_context:
                session_context[session_id] = new_context
            else:
                session_context.pop(session_id, None) # context reset
            return random.choice(intent["responses"]), tag, score

#Test
if __name__ == "__main__":
    tests = [
        "hello",
        "Where is my order?",
        "mera order kahan hai",
        "Can I get a refund",
        "what is the weather today",
        "मेरा ऑर्डर कहाँ है",
    ]
    for t in tests:
        response, tag, score = get_response(t)
        print(f"User: {t}\n  Intent: {tag} | Score: {score:.2f}\n  Bot: {response}\n")
