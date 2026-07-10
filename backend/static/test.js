// Simple test script
console.log(' TEST SCRIPT LOADED!');

// Check if elements exist
const elements = {
    sidebar: document.getElementById('sidebar'),
    messages: document.getElementById('messages'),
    chatMessages: document.getElementById('chatMessages'),
    userInput: document.getElementById('userInput'),
    sendBtn: document.getElementById('sendBtn'),
    welcome: document.getElementById('welcome'),
    typing: document.getElementById('typing'),
    newChatBtn: document.getElementById('newChatBtn'),
    collapseBtn: document.getElementById('collapseBtn'),
    menuBtn: document.getElementById('menuBtn')
};

console.log('Elements found:');
Object.keys(elements).forEach(key => {
    console.log(`  ${key}: ${!!elements[key]}`);
});

// Test send function
window.testSend = function() {
    const input = document.getElementById('userInput');
    if (input) {
        input.value = 'Test message from console!';
        const event = new Event('input', { bubbles: true });
        input.dispatchEvent(event);
        
        // Try to trigger send
        const sendBtn = document.getElementById('sendBtn');
        if (sendBtn) {
            sendBtn.click();
        }
    }
};

console.log(' Test script ready! Run testSend() to test.');