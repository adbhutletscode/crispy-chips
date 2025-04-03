// Chatbot functionality
document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const chatbotToggle = document.querySelector('.chatbot-toggle');
    const chatbotWindow = document.querySelector('.chatbot-window');
    const chatbotBody = document.querySelector('.chatbot-body');
    const chatbotInput = document.querySelector('.chatbot-input');
    const chatbotSend = document.querySelector('.chatbot-send');
    const chatbotNotification = document.querySelector('.chatbot-notification');
    
    // Bot responses
    const botResponses = {
        greeting: [
            "Hello! Welcome to Crispy Chips. How can I help you today?",
            "Hi there! I'm Crispy, your virtual assistant. What can I do for you?",
            "Welcome to Crispy Chips! I'm here to answer your questions."
        ],
        products: [
            "We offer a variety of delicious potato chips including Regular, Flavored, Spicy, and Organic options. Would you like to know more about any specific category?",
            "Our product range includes classic potato chips, flavored varieties, spicy options, and organic chips made with sustainable ingredients. Which would you like to explore?"
        ],
        shipping: [
            "We offer free shipping on orders over $50. Standard shipping takes 3-5 business days, and express shipping (additional fee) takes 1-2 business days.",
            "Shipping is free for orders above $50. We currently ship within the United States and Canada. Standard delivery takes 3-5 business days."
        ],
        returns: [
            "We have a 30-day return policy. If you're not satisfied with your purchase, you can return unopened items within 30 days for a full refund.",
            "Not happy with your purchase? No problem! You can return unopened products within 30 days for a full refund or exchange."
        ],
        ingredients: [
            "Our chips are made with premium potatoes, high-quality oils, and natural seasonings. All ingredients are listed on each product page. Our organic line uses 100% organic ingredients.",
            "We use only the finest potatoes and natural ingredients. Our organic line is certified organic, and we never use artificial preservatives or flavors in any of our products."
        ],
        contact: [
            "You can reach our customer service team at (555) 123-4567 or email us at info@crispychips.com. Our office hours are Monday-Friday, 9AM-5PM EST.",
            "Need to talk to a human? Call us at (555) 123-4567 or send an email to info@crispychips.com. We're available Monday through Friday, 9AM to 5PM EST."
        ],
        location: [
            "Our headquarters is located at 123 Crispy Lane, Chiptown, CT 12345. We have production facilities in three states across the US.",
            "We're based in Chiptown, CT with our main office at 123 Crispy Lane. We also have production facilities in California, Texas, and Michigan."
        ],
        fallback: [
            "I'm not sure I understand. Could you rephrase your question?",
            "I don't have information about that yet. Would you like to know about our products, shipping, returns, or contact information instead?",
            "I'm still learning! Could you try asking about our products, shipping policies, or contact information?"
        ]
    };
    
    // Quick reply options
    const quickReplyOptions = [
        { text: "Products", response: "products" },
        { text: "Shipping", response: "shipping" },
        { text: "Returns", response: "returns" },
        { text: "Ingredients", response: "ingredients" },
        { text: "Contact Us", response: "contact" }
    ];
    
    // Initial messages
    const initialMessages = [
        {
            text: getRandomResponse("greeting"),
            type: "bot",
            options: quickReplyOptions
        }
    ];
    
    // State
    let chatHistory = [];
    let isTyping = false;
    
    // Initialize
    function initChatbot() {
        // Show notification
        setTimeout(() => {
            chatbotNotification.style.display = 'flex';
        }, 3000);

        // Toggle chatbot
        chatbotToggle.addEventListener('click', toggleChatbot);

        // Minimize chatbot
        document.getElementById('chatbot-minimize').addEventListener('click', toggleChatbot);

        // Send message on button click
        chatbotSend.addEventListener('click', sendMessage);

        // Send message on Enter key
        chatbotInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        // Enable/disable send button based on input
        chatbotInput.addEventListener('input', function() {
            chatbotSend.disabled = chatbotInput.value.trim() === '';
        });

        // Adjust chatbot position on window resize
        window.addEventListener('resize', function() {
            if (chatbotWindow.classList.contains('active')) {
                ensureChatbotInViewport();
            }
        });

        // Load initial messages
        loadInitialMessages();
    }
    
    // Toggle chatbot window
    function toggleChatbot() {
        chatbotToggle.classList.toggle('active');

        if (!chatbotWindow.classList.contains('active')) {
            // Opening the chatbot
            chatbotWindow.style.display = 'flex';

            // Ensure the window is within viewport
            ensureChatbotInViewport();

            setTimeout(() => {
                chatbotWindow.classList.add('active');
                chatbotInput.focus();
            }, 10);

            // Hide notification
            chatbotNotification.style.display = 'none';
        } else {
            // Closing the chatbot
            chatbotWindow.classList.remove('active');
            setTimeout(() => {
                chatbotWindow.style.display = 'none';
            }, 300); // Match this with the CSS transition time
        }
    }

    // Ensure chatbot is within viewport
    function ensureChatbotInViewport() {
        // Get viewport dimensions
        const viewportWidth = window.innerWidth;
        const viewportHeight = window.innerHeight;

        // Get chatbot dimensions
        const chatbotRect = chatbotWindow.getBoundingClientRect();

        // Check if chatbot is outside viewport
        if (chatbotRect.right > viewportWidth) {
            // Adjust position to fit within viewport width
            chatbotWindow.style.right = '10px';
            chatbotWindow.style.left = 'auto';
        }

        if (chatbotRect.bottom > viewportHeight) {
            // Adjust height to fit within viewport
            const maxHeight = viewportHeight - chatbotRect.top - 20;
            chatbotWindow.style.maxHeight = maxHeight + 'px';
            chatbotBody.style.maxHeight = (maxHeight - 120) + 'px'; // Adjust for header and footer
        }
    }
    
    // Load initial messages
    function loadInitialMessages() {
        initialMessages.forEach(message => {
            addMessage(message.text, message.type, message.options);
        });
    }
    
    // Send message
    function sendMessage() {
        const message = chatbotInput.value.trim();
        if (message === '') return;
        
        // Add user message to chat
        addMessage(message, 'user');
        
        // Clear input
        chatbotInput.value = '';
        chatbotSend.disabled = true;
        
        // Process message and get response
        processMessage(message);
    }
    
    // Process message and generate response
    function processMessage(message) {
        // Show typing indicator
        showTypingIndicator();

        // For this demo, we'll use the local response generation
        // In a production environment, you would uncomment the fetch API code below
        // to send requests to your backend

        /*
        // Send request to API
        fetch('/api/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            // Hide typing indicator
            hideTypingIndicator();

            // Add bot response to chat
            addMessage(data.message, 'bot', data.options);

            // Scroll to bottom
            scrollToBottom();
        })
        .catch(error => {
            console.error('Error:', error);
            hideTypingIndicator();
            addMessage("Sorry, I'm having trouble connecting. Please try again later.", 'bot');
        });
        */

        // Simulate processing time
        setTimeout(() => {
            // Hide typing indicator
            hideTypingIndicator();

            // Generate response based on message content
            const response = generateResponse(message.toLowerCase());

            // Add bot response to chat
            addMessage(response.text, 'bot', response.options);

            // Scroll to bottom
            scrollToBottom();
        }, 1000 + Math.random() * 1000); // Random delay between 1-2 seconds
    }
    
    // Generate response based on user message
    function generateResponse(message) {
        // Check for keywords in message
        if (message.includes('product') || message.includes('chips') || message.includes('flavors')) {
            return {
                text: getRandomResponse('products'),
                options: [
                    { text: "Regular Chips", response: "Tell me about regular chips" },
                    { text: "Flavored Chips", response: "What flavors do you offer?" },
                    { text: "Organic Options", response: "Tell me about organic chips" }
                ]
            };
        } else if (message.includes('ship') || message.includes('delivery') || message.includes('order')) {
            return {
                text: getRandomResponse('shipping'),
                options: [
                    { text: "Shipping Costs", response: "How much is shipping?" },
                    { text: "Delivery Time", response: "How long does shipping take?" },
                    { text: "International", response: "Do you ship internationally?" }
                ]
            };
        } else if (message.includes('return') || message.includes('refund') || message.includes('exchange')) {
            return {
                text: getRandomResponse('returns'),
                options: null
            };
        } else if (message.includes('ingredient') || message.includes('allergen') || message.includes('gluten') || message.includes('organic')) {
            return {
                text: getRandomResponse('ingredients'),
                options: null
            };
        } else if (message.includes('contact') || message.includes('phone') || message.includes('email') || message.includes('call')) {
            return {
                text: getRandomResponse('contact'),
                options: null
            };
        } else if (message.includes('where') || message.includes('location') || message.includes('address')) {
            return {
                text: getRandomResponse('location'),
                options: null
            };
        } else if (message.includes('hello') || message.includes('hi') || message.includes('hey')) {
            return {
                text: getRandomResponse('greeting'),
                options: quickReplyOptions
            };
        } else {
            return {
                text: getRandomResponse('fallback'),
                options: quickReplyOptions
            };
        }
    }
    
    // Get random response from category
    function getRandomResponse(category) {
        const responses = botResponses[category];
        return responses[Math.floor(Math.random() * responses.length)];
    }
    
    // Add message to chat
    function addMessage(text, type, options = null) {
        // Create message element
        const messageEl = document.createElement('div');
        messageEl.classList.add('chatbot-message', type);
        
        // Add message text
        messageEl.textContent = text;
        
        // Add timestamp
        const timestamp = document.createElement('div');
        timestamp.classList.add('chatbot-timestamp');
        timestamp.textContent = getCurrentTime();
        messageEl.appendChild(timestamp);
        
        // Add message to chat
        chatbotBody.appendChild(messageEl);
        
        // Add options if provided
        if (options) {
            const optionsContainer = document.createElement('div');
            optionsContainer.classList.add('chatbot-options');
            
            options.forEach(option => {
                const optionEl = document.createElement('button');
                optionEl.classList.add('chatbot-option');
                optionEl.textContent = option.text;
                
                // Add click event
                optionEl.addEventListener('click', function() {
                    // Add user message
                    addMessage(option.text, 'user');
                    
                    // Process response
                    processMessage(option.response);
                    
                    // Remove options
                    optionsContainer.remove();
                });
                
                optionsContainer.appendChild(optionEl);
            });
            
            chatbotBody.appendChild(optionsContainer);
        }
        
        // Add to chat history
        chatHistory.push({
            text,
            type,
            timestamp: new Date()
        });
        
        // Scroll to bottom
        scrollToBottom();
    }
    
    // Show typing indicator
    function showTypingIndicator() {
        if (isTyping) return;
        
        isTyping = true;
        
        const typingIndicator = document.createElement('div');
        typingIndicator.classList.add('chatbot-message', 'typing');
        typingIndicator.id = 'typing-indicator';
        
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('div');
            dot.classList.add('typing-dot');
            typingIndicator.appendChild(dot);
        }
        
        chatbotBody.appendChild(typingIndicator);
        scrollToBottom();
    }
    
    // Hide typing indicator
    function hideTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
        isTyping = false;
    }
    
    // Get current time in HH:MM format
    function getCurrentTime() {
        const now = new Date();
        let hours = now.getHours();
        let minutes = now.getMinutes();
        const ampm = hours >= 12 ? 'PM' : 'AM';
        
        hours = hours % 12;
        hours = hours ? hours : 12;
        minutes = minutes < 10 ? '0' + minutes : minutes;
        
        return `${hours}:${minutes} ${ampm}`;
    }
    
    // Scroll chat to bottom
    function scrollToBottom() {
        chatbotBody.scrollTop = chatbotBody.scrollHeight;
    }
    
    // Initialize chatbot
    initChatbot();
});