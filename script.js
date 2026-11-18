const chatBox = document.getElementById("chat-box");
const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");
const newChatButton = document.getElementById("new-chat");

let conversationId = null;

// Add a message bubble to the chat window.
function showMessage(message, sender, isError = false) {
    const messageRow = document.createElement("div");
    messageRow.className = `message ${sender}`;

    if (isError) {
        messageRow.classList.add("error");
    }

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = message;

    messageRow.appendChild(bubble);
    chatBox.appendChild(messageRow);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Send the message to the Flask backend.
async function sendMessage(message) {
    sendButton.disabled = true;
    sendButton.textContent = "Sending...";

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message,
                conversation_id: conversationId
            })
        });

        const data = await response.json();

        if (!response.ok) {
            showMessage(data.error || "Could not get a reply. Please try again.", "bot", true);
            return;
        }

        conversationId = data.conversation_id;
        showMessage(data.reply, "bot");

    } catch (error) {
        showMessage("Cannot connect to the server. Make sure Flask is running.", "bot", true);
    } finally {
        sendButton.disabled = false;
        sendButton.textContent = "Send";
        messageInput.focus();
    }
}

// Run when the user presses Send or Enter.
chatForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const message = messageInput.value.trim();

    if (message === "") {
        return;
    }

    showMessage(message, "user");
    messageInput.value = "";

    await sendMessage(message);
});

// Start a separate conversation.
newChatButton.addEventListener("click", async function () {
    try {
        const response = await fetch("/api/new", {
            method: "POST"
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error("New chat could not be started.");
        }

        conversationId = data.conversation_id;
        chatBox.innerHTML = "";
        showMessage("New conversation started. What would you like to learn?", "bot");

    } catch (error) {
        showMessage("Could not start a new chat. Please try again.", "bot", true);
    }
});
