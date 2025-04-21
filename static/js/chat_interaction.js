document.addEventListener("DOMContentLoaded", function () {
  const chatForm = document.getElementById("chatForm");
  const messageInput = document.getElementById("messageInput");
  const chatMessages = document.getElementById("chatMessages");
  const typingIndicator = document.getElementById("typingIndicator");

  // Scroll to bottom of chat
  function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
  scrollToBottom();

  // Add message to chat
  function addMessage(message, isUser = true) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${isUser ? "user" : "bot"}`;

    const contentDiv = document.createElement("div");
    contentDiv.className = "message-content";
    contentDiv.textContent = message;

    const timeDiv = document.createElement("div");
    timeDiv.className = "message-time";
    timeDiv.textContent = new Date().toLocaleString();

    messageDiv.appendChild(contentDiv);
    messageDiv.appendChild(timeDiv);

    typingIndicator.insertAdjacentElement("beforebegin", messageDiv);
    scrollToBottom();
  }

  // Show/hide typing indicator
  function setTypingIndicator(visible) {
    typingIndicator.style.display = visible ? "block" : "none";
    if (visible) scrollToBottom();
  }

  // Handle form submission
  chatForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    const message = messageInput.value.trim();
    if (!message) return;

    // Add user message
    addMessage(message, true);
    messageInput.value = "";

    // Show typing indicator
    setTypingIndicator(true);

    try {
      const response = await fetch("/send_message/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
            .value,
        },
        body: JSON.stringify({ message: message }),
      });

      const data = await response.json();

      if (data.status === "success") {
        // Add bot response
        addMessage(data.response, false);
      } else {
        console.error("Error:", data.message);
      }
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setTypingIndicator(false);
    }
  });
});
