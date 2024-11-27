# E-commerce Order Management Chatbot

A conversational AI chatbot developed using Rasa, an open-source machine learning framework for automated text and voice-based assistants. The chatbot leverages SpaCy for natural language processing and MySQL for managing order-related data. It is designed to handle order-related queries for an e-commerce platform, providing seamless interactions for order placement, order tracking, and order cancellation.

## Project Overview
The chatbot provides users with a natural language interface to:

### Place Orders: Users can place new orders seamlessly through conversational prompts. Item validation ensures accuracy and availability.
### Track Orders: Tracks the real-time status of orders by validating order numbers and fetching updated information directly from the database.
### Cancel Orders: Cancels orders securely after validating the provided order number, offering a confirmation message to the user.
### Handle General Inquiries: Provides essential information, including contact details and comprehensive refund policies, to address common user questions.
It also includes intelligent handling for fallbacks (when the chatbot doesn't understand the user query) and the ability to switch contexts between tasks.

##Technologies Used
Rasa: Natural Language Understanding (NLU), SpaCy, MySQL, Python, YAML

## Features
### Custom Actions: 
The bot uses custom Python actions for real-time order validation, setting contexts for different actions, and fetching and updating data from an external MySQL database.

### Conversation Flow: 
The chatbot intelligently handles conversation flows using Rasa stories and rules, enabling the bot to react dynamically to user inputs and adjust its behavior based on context.

### Context Switching: 
If the user changes their request (e.g., from canceling to tracking an order), the bot can easily switch context and continue the conversation without confusion.

### Error Handling: 
The chatbot has robust error handling for cases where it doesn't understand the user’s request or when invalid data (e.g., incorrect order number) is provided.
