document.addEventListener("DOMContentLoaded", function () {
  const chatForm = document.getElementById("chatForm");
  const messageInput = document.getElementById("messageInput");
  const chatMessages = document.getElementById("chatMessages");
  const typingIndicator = document.getElementById("typingIndicator");

  // Format markdown text
  function formatMarkdown(text) {
    // Replace headings (h1-h6)
    text = text.replace(/^### (.*$)/gm, "<h3>$1</h3>");
    text = text.replace(/^## (.*$)/gm, "<h2>$1</h2>");
    text = text.replace(/^# (.*$)/gm, "<h1>$1</h1>");

    // Replace bold text
    text = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
    // Replace italic text
    text = text.replace(/\*(.*?)\*/g, "<em>$1</em>");
    // Replace code blocks
    text = text.replace(/`(.*?)`/g, "<code>$1</code>");

    // Replace blockquotes
    text = text.replace(/^> (.*$)/gm, "<blockquote>$1</blockquote>");

    // Add line breaks
    text = text.replace(/\n/g, "<br>");

    return text;
  }

  // Apply formatMarkdown to all initial bot messages
  document.querySelectorAll(".bot-markdown").forEach(function (div) {
    div.innerHTML = formatMarkdown(div.textContent);
  });

  // Scroll to bottom of chat
  function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
  scrollToBottom();

  function getCurrentDateTime() {
    const now = new Date();

    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, "0"); // Months are zero-indexed
    const day = String(now.getDate()).padStart(2, "0");

    const hours = String(now.getHours()).padStart(2, "0");
    const minutes = String(now.getMinutes()).padStart(2, "0");
    const seconds = String(now.getSeconds()).padStart(2, "0");

    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
  }

  // Add message to chat
  function addMessage(message, isUser = true) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${isUser ? "user" : "bot"}`;

    const contentDiv = document.createElement("div");
    contentDiv.className = "message-content";
    // Format markdown for bot messages
    contentDiv.innerHTML = isUser ? message : formatMarkdown(message);

    const timeDiv = document.createElement("div");
    timeDiv.className = "message-time";
    timeDiv.textContent = getCurrentDateTime();

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

  // --- New Chat Button Logic ---
  const newConversationBtn = document.getElementById("newConversationBtn");
  if (newConversationBtn) {
    newConversationBtn.addEventListener("click", function () {
      // Clear chat window and reset conversation state
      chatMessages.innerHTML = "";
      chatMessages.appendChild(typingIndicator);
      scrollToBottom();
      // Remove active class from all conversation previews
      document
        .querySelectorAll(".conversation-preview")
        .forEach((el) => el.classList.remove("active"));
      // Focus the input
      messageInput.value = "";
      messageInput.focus();
      // Set a flag or variable if you want to track new conversation state
      window.currentConversationId = null;
    });
  }
});
