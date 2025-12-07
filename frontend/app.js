// Configuration
const API_URL = '/api/chat';
let sessionId = null;
let customerId = null; // Default to guest/null to avoid "Priya Sharma"

// DOM Elements
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const sessionIdDisplay = document.getElementById('session-id');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Generate session ID
    sessionId = generateSessionId();
    sessionIdDisplay.textContent = `Session: ${sessionId}`;

    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});

// Generate session ID
function generateSessionId() {
    return 'SESS' + Math.random().toString(36).substr(2, 9).toUpperCase();
}

// Send message
async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    // Disable input
    userInput.disabled = true;
    sendButton.disabled = true;

    // Add user message to chat
    addMessage(message, 'user');

    // Clear input
    userInput.value = '';

    // Show typing indicator
    const typingIndicator = showTypingIndicator();

    try {
        // Send to API
        const response = await fetch(`${API_URL}/message`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId,
                customer_id: customerId,
                channel: 'web_chat'
            })
        });

        if (!response.ok) {
            throw new Error('Failed to get response');
        }

        const data = await response.json();

        // Remove typing indicator
        typingIndicator.remove();

        // Add assistant message
        addMessage(data.response, 'assistant');

    } catch (error) {
        console.error('Error:', error);
        typingIndicator.remove();
        addMessage('Sorry, I encountered an error. Please try again.', 'assistant');
    } finally {
        // Re-enable input
        userInput.disabled = false;
        sendButton.disabled = false;
        userInput.focus();
    }
}

// Add message to chat
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');

    // Common animation class
    const animClass = 'message-anim';

    if (sender === 'user') {
        // User Message Styling
        messageDiv.className = `flex gap-4 flex-row-reverse ${animClass}`;
        messageDiv.innerHTML = `
            <div class="w-8 h-8 rounded-full bg-[#2a2a2a] flex-shrink-0 flex items-center justify-center shadow-lg border border-white/10">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-user text-gray-300"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            </div>
            <div class="flex flex-col gap-2 max-w-[85%] items-end">
                <div class="bg-gradient-to-br from-[#667eea] to-[#764ba2] text-white rounded-2xl rounded-tr-none p-4 shadow-lg shadow-purple-900/20">
                    <div class="prose prose-invert prose-sm max-w-none">
                        ${formatMessage(text)}
                    </div>
                </div>
            </div>
        `;
    } else {
        // Assistant Message Styling
        messageDiv.className = `flex gap-4 ${animClass}`;
        messageDiv.innerHTML = `
            <div class="w-8 h-8 rounded-full bg-gradient-to-br from-[#667eea] to-[#764ba2] flex-shrink-0 flex items-center justify-center shadow-lg shadow-purple-900/20">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-sparkles text-white"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275Z"/></svg>
            </div>
            <div class="flex flex-col gap-2 max-w-[85%]">
                <div class="bg-[#1a1a1a]/80 backdrop-blur-sm border border-white/10 rounded-2xl rounded-tl-none p-4 text-gray-200 shadow-sm">
                    <div class="prose prose-invert prose-sm max-w-none">
                        ${formatMessage(text)}
                    </div>
                </div>
            </div>
        `;
    }

    chatMessages.appendChild(messageDiv);

    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Format message (basic markdown support)
function formatMessage(text) {
    if (!text) return '';

    // Convert line breaks
    text = text.replace(/\n/g, '<br>');

    // Convert bold
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Convert bullet points
    text = text.replace(/^- (.+)$/gm, '<li>$1</li>');

    // Wrap lists
    if (text.includes('<li>')) {
        text = text.replace(/(<li>.*<\/li>)/s, '<ul class="list-disc list-inside space-y-1 ml-1">$1</ul>');
    }

    return text;
}

// Show typing indicator
function showTypingIndicator() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'flex gap-4 message-anim';

    messageDiv.innerHTML = `
        <div class="w-8 h-8 rounded-full bg-gradient-to-br from-[#667eea] to-[#764ba2] flex-shrink-0 flex items-center justify-center shadow-lg shadow-purple-900/20">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-sparkles text-white"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275Z"/></svg>
        </div>
        <div class="flex flex-col gap-2 max-w-[85%]">
            <div class="bg-[#1a1a1a]/80 backdrop-blur-sm border border-white/10 rounded-2xl rounded-tl-none p-4 text-gray-200 shadow-sm">
                <div class="flex space-x-1 h-6 items-center">
                    <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0s"></div>
                    <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                    <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
                </div>
            </div>
        </div>
    `;

    chatMessages.appendChild(messageDiv);

    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;

    return messageDiv;
}
