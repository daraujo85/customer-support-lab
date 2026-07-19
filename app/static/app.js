const log = document.getElementById("log");
const form = document.getElementById("form");
const input = document.getElementById("input");
const payloadPanel = document.getElementById("payload");
const payloadToggle = document.getElementById("payload-toggle");

let sessionId = null;
let payloadVisible = false;

function append(who, text) {
  const line = document.createElement("div");
  line.className = `msg msg-${who}`;
  line.textContent = text;
  log.appendChild(line);
  log.scrollTop = log.scrollHeight;
}

// Aula 2.1: busca o payload de conversação (role/content) que uma API de LLM
// receberia — ainda não chamamos nenhuma, só expomos a estrutura real.
async function refreshPayload() {
  if (!payloadVisible || !sessionId) return;
  const res = await fetch(`/api/chat/${sessionId}/payload`);
  const data = await res.json();
  payloadPanel.textContent = JSON.stringify(data.payload, null, 2);
}

payloadToggle.addEventListener("click", () => {
  payloadVisible = !payloadVisible;
  payloadPanel.hidden = !payloadVisible;
  payloadToggle.textContent = payloadVisible ? "Ocultar payload" : "Ver payload";
  if (payloadVisible) refreshPayload();
});

async function send(message) {
  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, message }),
  });
  const data = await res.json();
  sessionId = data.session_id;
  append("bot", data.reply);
  await refreshPayload();
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
