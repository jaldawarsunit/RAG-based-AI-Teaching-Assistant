document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const chatContainer = document.getElementById('chatContainer');
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const clearChatButton = document.getElementById('clearChat');
    const processingOverlay = document.getElementById('processingOverlay');
    const processingSteps = document.querySelectorAll('.step');
    
    // Auto-resize textarea
    messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 150) + 'px';
    });
    
    // Send message function
    async function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        addMessageToChat('user', message);
        messageInput.value = '';
        messageInput.style.height = 'auto';
        
        // Disable input and show processing
        messageInput.disabled = true;
        sendButton.disabled = true;
        showProcessingAnimation();
        
        try {
            // Send to backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            
            // Update processing steps
            updateProcessingStep(3, true);
            
            // Add slight delay for natural feel
            await new Promise(resolve => setTimeout(resolve, 500));
            
            // Hide processing overlay
            hideProcessingAnimation();
            
            // Add assistant response to chat
            addMessageToChat('assistant', data.response);
            
        } catch (error) {
            console.error('Error:', error);
            hideProcessingAnimation();
            addMessageToChat('assistant', 'Sorry, I encountered an error. Please try again.');
        } finally {
            // Re-enable input
            messageInput.disabled = false;
            sendButton.disabled = false;
            messageInput.focus();
        }
    }
    
    // Add message to chat UI
    function addMessageToChat(type, message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        
        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        messageDiv.innerHTML = `
            <div class="avatar">
                <i class="fas ${type === 'user' ? 'fa-user' : 'fa-robot'}"></i>
            </div>
            <div class="content">
                <div class="message-header">
                    <span class="sender">${type === 'user' ? 'You' : 'Teaching Assistant'}</span>
                    <span class="time">${time}</span>
                </div>
                <div class="message-text">${formatMessage(message)}</div>
            </div>
        `;
        
        chatContainer.appendChild(messageDiv);
        scrollToBottom();
    }
    
    // Format message with line breaks and markdown-like formatting
    function formatMessage(message) {
        return message
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`([^`]+)`/g, '<code>$1</code>');
    }
    
    // Show processing animation with step-by-step updates
    function showProcessingAnimation() {
        processingOverlay.style.display = 'flex';
        
        // Reset and animate steps
        processingSteps.forEach((step, index) => {
            step.classList.remove('active');
            setTimeout(() => {
                step.classList.add('active');
            }, index * 800); // Stagger the step activations
        });
    }
    
    // Update specific processing step
    function updateProcessingStep(stepNumber, isComplete) {
        const step = document.getElementById(`step${stepNumber}`);
        if (step) {
            if (isComplete) {
                step.innerHTML = `<i class="fas fa-check"></i><span>Step ${stepNumber} complete!</span>`;
                step.classList.add('active');
            }
        }
    }
    
    // Hide processing animation
    function hideProcessingAnimation() {
        processingOverlay.style.display = 'none';
        // Reset steps for next time
        processingSteps.forEach(step => {
            step.classList.remove('active');
        });
    }
    
    // Scroll chat to bottom
    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    
    // Clear chat history
    async function clearChat() {
        if (confirm('Are you sure you want to clear the chat?')) {
            try {
                await fetch('/clear', { method: 'POST' });
                // Remove all messages except welcome
                const messages = document.querySelectorAll('.message:not(.assistant:first-child)');
                messages.forEach(msg => msg.remove());
                
                // Add cleared notification
                const notificationDiv = document.createElement('div');
                notificationDiv.className = 'message assistant';
                notificationDiv.innerHTML = `
                    <div class="avatar">
                        <i class="fas fa-robot"></i>
                    </div>
                    <div class="content">
                        <div class="message-text" style="background: #e3f2fd; color: #1976d2;">
                            <i class="fas fa-info-circle"></i> Chat history cleared
                        </div>
                    </div>
                `;
                chatContainer.appendChild(notificationDiv);
                scrollToBottom();
            } catch (error) {
                console.error('Error clearing chat:', error);
            }
        }
    }
    
    // Event Listeners
    sendButton.addEventListener('click', sendMessage);
    
    messageInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    clearChatButton.addEventListener('click', clearChat);
    
    // Load chat history on page load
    async function loadChatHistory() {
        try {
            const response = await fetch('/history');
            const data = await response.json();
            
            // Clear default welcome if we have history
            if (data.history.length > 0) {
                const welcomeMsg = document.querySelector('.message.assistant:first-child');
                if (welcomeMsg) welcomeMsg.remove();
                
                // Add history messages
                data.history.forEach(msg => {
                    addMessageToChat(msg.type, msg.message);
                });
            }
        } catch (error) {
            console.error('Error loading chat history:', error);
        }
    }
    
    // Initialize
    messageInput.focus();
    loadChatHistory();
});