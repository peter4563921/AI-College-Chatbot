const API_BASE = "http://127.0.0.1:5000/api";
const chatMessages = document.getElementById("chatMessages");
const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const suggestions = document.getElementById("suggestions");
const themeToggle = document.getElementById("themeToggle");

const sessionId =
  localStorage.getItem("chatSessionId") ||
  crypto.randomUUID();

localStorage.setItem("chatSessionId", sessionId);

const suggestedQuestions = [
  "What courses are available?",
  "What is the MCA eligibility?",
  "Tell me about fees structure",
  "Hostel and transport details",
  "What placement support is available?",
  "Contact information",
  "Scholarship details",
  "Important admission dates"
];

function nowTime() {
  return new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit"
  });
}

function addMessage(role, text) {
  const bubble = document.createElement("div");
  bubble.className = "message " + role;

  const body = document.createElement("div");
  body.textContent = text;

  const time = document.createElement("span");
  time.className = "time";
  time.textContent = nowTime();

  bubble.append(body, time);

  chatMessages.appendChild(bubble);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addTyping() {
  const bubble = document.createElement("div");
  bubble.className = "message bot";

  bubble.innerHTML =
    '<span class="typing"><span></span><span></span><span></span></span>';

  chatMessages.appendChild(bubble);
  chatMessages.scrollTop = chatMessages.scrollHeight;

  return bubble;
}

async function sendMessage(message) {

  const clean = message.trim();

  if (!clean) return;

  addMessage("user", clean);

  messageInput.value = "";

  const typing = addTyping();

  try {

    const response = await fetch(API_BASE + "/chat", {

      method: "POST",

      headers: {
        "Content-Type": "application/json"
      },

      body: JSON.stringify({
        message: clean,
        session_id: sessionId
      })

    });

    let data;
    try {
      data = await response.json();
    } catch (e) {
      const text = await response.text().catch(() => '');
      data = { message: text || 'Invalid JSON response from server' };
    }

    typing.remove();

    if (!response.ok) {
      throw new Error(data.message || "Server Error");
    }

    addMessage("bot", data.data.reply);

  } catch (err) {

    typing.remove();

    addMessage(
      "bot",
      "❌ " + err.message
    );

    console.error(err);

  }

}

suggestedQuestions.forEach((question) => {

  const btn = document.createElement("button");

  btn.type = "button";

  btn.textContent = question;

  btn.onclick = () => sendMessage(question);

  suggestions.appendChild(btn);

});

chatForm.addEventListener("submit", (e) => {

  e.preventDefault();

  sendMessage(messageInput.value);

});

messageInput.addEventListener("keydown", (e) => {

  if (e.key === "Enter" && !e.shiftKey) {

    e.preventDefault();

    chatForm.requestSubmit();

  }

});

themeToggle.addEventListener("click", () => {

  const theme =
    document.documentElement.dataset.theme === "dark"
      ? "light"
      : "dark";

  document.documentElement.dataset.theme = theme;

  localStorage.setItem("theme", theme);

});

document.documentElement.dataset.theme =
  localStorage.getItem("theme") || "light";

addMessage(
  "bot",
  "Welcome. Ask me about KVCET courses, fees, admission, hostel, transport, placements, scholarships, faculty or contact details."
);