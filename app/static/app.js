const log = document.getElementById("log");
const form = document.getElementById("form");
const input = document.getElementById("input");

let sessionId = null;

function append(who, text) {
  const line = document.createElement("div");
  line.className = `msg msg-${who}`;
  line.textContent = text;
  log.appendChild(line);
  log.scrollTop = log.scrollHeight;
}

async function send(message) {
  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, message }),
  });
  const data = await res.json();
  sessionId = data.session_id;
  append("bot", data.reply);
}

form.addEventListener("submit", (ev) => {
  ev.preventDefault();
  const message = input.value;
  input.value = "";
  if (message.trim()) append("user", message);
  send(message);
});

// Dispara a saudação assim que a página abre (evento inicial, sem input do usuário).
send("");
