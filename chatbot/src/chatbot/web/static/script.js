let ws = new WebSocket("ws://" + window.location.host + "/ws");

ws.onmessage = function(event) {
    const message = JSON.parse(event.data);
    addMessage(message.text, message.sender);
};

function sendMessage() {
    const input = document.getElementById('message-input');
    const message = input.value.trim();
    if (message) {
        ws.send(JSON.stringify({text: message}));
        addMessage(message, 'user');
        input.value = '';
    }
}

function addMessage(text, sender) {
    const messages = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    // Use innerHTML instead of textContent to render HTML
    if (sender === 'user') {
        // For user messages, we still use textContent to prevent XSS
        messageDiv.textContent = text;
    } else {
        // For bot messages, we allow HTML rendering
        messageDiv.innerHTML = text;

        // Add event listeners to any links in the response
        const links = messageDiv.querySelectorAll('a');
        links.forEach(link => {
            // Make sure links open in new tab for external URLs
            if (link.getAttribute('href').startsWith('http')) {
                link.setAttribute('target', '_blank');
                link.setAttribute('rel', 'noopener noreferrer');
            }
        });
    }

    messages.appendChild(messageDiv);
    messages.scrollTop = messages.scrollHeight;
}

document.getElementById('message-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Add connection status handling
ws.onopen = function() {
    console.log('Connected to chat server');
};

ws.onclose = function() {
    console.log('Disconnected from chat server');
    // You could add UI feedback here
};

ws.onerror = function(error) {
    console.error('WebSocket error:', error);
    // You could add UI feedback here
};