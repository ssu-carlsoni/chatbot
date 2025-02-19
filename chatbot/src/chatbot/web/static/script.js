let ws;
let reconnectInterval = 1000; // Start with 1 second
const maxReconnectInterval = 30000; // Max of 30 seconds
let reconnectTimer;
let messageQueue = [];
let isConnected = false;

function connectWebSocket() {
    ws = new WebSocket("ws://" + window.location.host + "/ws");

    ws.onopen = function() {
        console.log('Connected to chat server');
        isConnected = true;
        reconnectInterval = 1000; // Reset reconnect interval
        showConnectionStatus('connected');

        // Send any queued messages
        while (messageQueue.length > 0 && isConnected) {
            const message = messageQueue.shift();
            ws.send(JSON.stringify(message));
        }
    };

    ws.onmessage = function(event) {
        const message = JSON.parse(event.data);
        addMessage(message.text, message.sender);
    };

    ws.onclose = function() {
        console.log('Disconnected from chat server');
        isConnected = false;
        showConnectionStatus('disconnected');
        scheduleReconnect();
    };

    ws.onerror = function(error) {
        console.error('WebSocket error:', error);
        isConnected = false;
        showConnectionStatus('error');
        // Don't need to schedule reconnect here as onclose will fire after onerror
    };
}

function scheduleReconnect() {
    clearTimeout(reconnectTimer);
    reconnectTimer = setTimeout(function() {
        console.log(`Attempting to reconnect... (retry in ${reconnectInterval/1000}s)`);
        connectWebSocket();
        // Exponential backoff with jitter for reconnection attempts
        reconnectInterval = Math.min(reconnectInterval * 1.5 * (0.9 + Math.random() * 0.2), maxReconnectInterval);
    }, reconnectInterval);
}

function showConnectionStatus(status) {
    const statusElement = document.getElementById('connection-status');
    if (!statusElement) return;
    statusElement.className = 'badge';
    switch(status) {

        case 'connected':
            statusElement.textContent = 'Connected';
            statusElement.classList.add('text-bg-success');
            break;
        case 'disconnected':
            statusElement.textContent = 'Disconnected - Attempting to reconnect...';
            statusElement.classList.add('text-bg-warning');
            break;
        case 'error':
            statusElement.textContent = 'Connection Error';
            statusElement.classList.add('text-bg-danger');
            break;
    }
}

function sendMessage() {
    const input = document.getElementById('message-input');
    const message = input.value.trim();
    if (message) {
        // remove all messages
        const messages = document.getElementById('messages');
        messages.innerHTML = '';

        const messageObj = {text: message};

        if (isConnected) {
            ws.send(JSON.stringify(messageObj));
        } else {
            messageQueue.push(messageObj);
            showConnectionStatus('disconnected');
        }

        addMessage(message, 'user');
        input.value = '';
    }
}

function addMessage(text, sender) {
    const messages = document.getElementById('messages');
    const messageDiv = document.createElement('div');

    // Use innerHTML instead of textContent to render HTML
    if (sender === 'user') {
        // For user messages, we still use textContent to prevent XSS
        messageDiv.className = 'alert alert-secondary';
        messageDiv.innerHTML = '<i class="fa-solid fa-user"></i> ';
        const span = document.createElement('span');
        span.textContent = text;
        messageDiv.appendChild(span);
    } else {
        // For bot messages, we allow HTML rendering
        messageDiv.className = `alert alert-light`;
        messageDiv.innerHTML = '<i class="fa-solid fa-graduation-cap"></i> ' + text;

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

// Initialize connection when page loads
connectWebSocket();
