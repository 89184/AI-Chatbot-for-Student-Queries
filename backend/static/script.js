// MAIN SCRIPT - Chat Functionality

// DOM Elements - Using CORRECT IDs from HTML
const messagesContainer = document.getElementById('messages');
const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const typingIndicator = document.getElementById('typing');
const welcomeScreen = document.getElementById('welcome');

console.log('Script loaded!');
console.log('Elements found:', {
    messagesContainer: !!messagesContainer,
    chatMessages: !!chatMessages,
    userInput: !!userInput,
    sendBtn: !!sendBtn,
    typingIndicator: !!typingIndicator,
    welcomeScreen: !!welcomeScreen
});

// ===== HELPERS =====
function getTimestamp() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ===== ADD MESSAGE =====
function addMessage(message, isUser = false) {
    // Hide welcome screen
    if (welcomeScreen) welcomeScreen.style.display = 'none';
    
    const div = document.createElement('div');
    div.className = `message ${isUser ? 'user' : ''}`;
    
    const avatar = isUser ? '' : '';
    
    div.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-bubble">
            ${escapeHtml(message)}
            <span class="message-time">${getTimestamp()}</span>
        </div>
    `;
    
    if (chatMessages) {
        chatMessages.appendChild(div);
        if (messagesContainer) messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}

// ===== TYPING INDICATOR =====
function showTyping() {
    if (typingIndicator) {
        typingIndicator.style.display = 'flex';
        if (messagesContainer) messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}

function hideTyping() {
    if (typingIndicator) {
        typingIndicator.style.display = 'none';
    }
}

// ===== SEND MESSAGE =====
async function sendMessage() {
    if (!userInput) {
        console.error('User input not found!');
        return;
    }
    
    const message = userInput.value.trim();
    if (!message) return;

    // Disable input
    userInput.disabled = true;
    if (sendBtn) sendBtn.disabled = true;

    // Add user message
    addMessage(message, true);
    userInput.value = '';
    showTyping();

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        hideTyping();
        addMessage(data.response);
    } catch (error) {
        hideTyping();
        addMessage('Sorry, I\'m having trouble connecting. Please try again.');
        console.error('Error:', error);
    } finally {
        userInput.disabled = false;
        if (sendBtn) sendBtn.disabled = false;
        userInput.focus();
    }
}

// ===== CLEAR CHAT =====
function clearChat() {
    if (chatMessages) chatMessages.innerHTML = '';
    if (welcomeScreen) welcomeScreen.style.display = 'flex';
}

// ===== EVENT LISTENERS =====
if (sendBtn) {
    sendBtn.addEventListener('click', sendMessage);
    console.log('Send button listener added');
}

if (userInput) {
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage();
        }
    });
    console.log(' User input listener added');
}

// Quick action buttons
document.querySelectorAll('.quick-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const msg = btn.getAttribute('data-msg');
        if (userInput) {
            userInput.value = msg;
            sendMessage();
        }
    });
});

// New chat button
const newChatBtn = document.getElementById('newChatBtn');
if (newChatBtn) {
    newChatBtn.addEventListener('click', clearChat);
}

// Auto-focus
if (userInput) {
    userInput.focus();
}

// Keyboard shortcut: Ctrl+K = New Chat
document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        clearChat();
    }
});

console.log('Chat functionality loaded!');
