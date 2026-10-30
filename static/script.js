const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

let sessionId = null;

function addMessage(text, sender) {
  const div = document.createElement("div");
  div.className = "message " + sender;
  div.textContent = text;   // textContent XSS se bachata hai
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
  const text = input.value.trim();
  if (!text) return;

  addMessage(text, "user");
  input.value = "";

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, session_id: sessionId }),
    });
    const data = await res.json();
    sessionId = data.session_id;
    addMessage(data.response || data.error, "bot");
  } catch (err) {
    addMessage("Server error. Please try again.", "bot");
  }
}

sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendMessage();
});