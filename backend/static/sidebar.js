// SIDEBAR FUNCTIONALITY

// DOM Elements
const sidebar = document.getElementById('sidebar');
const collapseBtn = document.getElementById('collapseBtn');
const menuBtn = document.getElementById('menuBtn');
const newChatBtn = document.getElementById('newChatBtn');

// ===== COLLAPSE/EXPAND =====
if (collapseBtn && sidebar) {
    collapseBtn.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
        
        // Save state
        try {
            localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
        } catch (e) {}
    });
}

// ===== MOBILE MENU =====
if (menuBtn && sidebar) {
    menuBtn.addEventListener('click', () => {
        sidebar.classList.toggle('open');
    });
}

// ===== CLOSE ON OUTSIDE CLICK =====
document.addEventListener('click', (e) => {
    if (window.innerWidth <= 768) {
        if (sidebar && !sidebar.contains(e.target) && menuBtn && !menuBtn.contains(e.target)) {
            sidebar.classList.remove('open');
        }
    }
});

// ===== CLOSE ON RESIZE =====
window.addEventListener('resize', () => {
    if (window.innerWidth > 768 && sidebar) {
        sidebar.classList.remove('open');
    }
});

// ===== HISTORY ITEMS =====
document.querySelectorAll('.history-item').forEach(item => {
    item.addEventListener('click', () => {
        // Remove active from all
        document.querySelectorAll('.history-item').forEach(h => h.classList.remove('active'));
        // Add active to clicked
        item.classList.add('active');
        
        // Close sidebar on mobile
        if (window.innerWidth <= 768 && sidebar) {
            sidebar.classList.remove('open');
        }
        
        // Clear chat
        const chatMessages = document.getElementById('chatMessages');
        const welcome = document.getElementById('welcome');
        if (chatMessages) chatMessages.innerHTML = '';
        if (welcome) welcome.style.display = 'flex';
    });
});

// ===== NEW CHAT =====
if (newChatBtn) {
    newChatBtn.addEventListener('click', () => {
        // Clear chat
        const chatMessages = document.getElementById('chatMessages');
        const welcome = document.getElementById('welcome');
        if (chatMessages) chatMessages.innerHTML = '';
        if (welcome) welcome.style.display = 'flex';
        
        // Remove active from all history
        document.querySelectorAll('.history-item').forEach(h => h.classList.remove('active'));
        
        // Focus on input
        const userInput = document.getElementById('userInput');
        if (userInput) userInput.focus();
    });
}

// ===== LOAD SAVED STATE =====
try {
    const saved = localStorage.getItem('sidebarCollapsed');
    if (saved === 'true' && sidebar) {
        sidebar.classList.add('collapsed');
    }
} catch (e) {}

console.log('Sidebar loaded!');