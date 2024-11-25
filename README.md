## E-commerce Order Management Chatbot

A conversational AI chatbot developed using Rasa, an open-source machine learning framework for automated text and voice-based assistants. The chatbot is designed to handle order-related queries for an e-commerce platform, providing seamless interactions for order placement, order tracking, and order cancellation.

# Project Overview
The chatbot provides users with a natural language interface to:

# Place Orders: Allows users to place new orders through conversational prompts.
# Track Orders: Tracks the status of orders by validating order numbers and fetching real-time information.
# Cancel Orders: Cancels orders based on validated order numbers.
# Handle General Inquiries: Provides contact information and refund policies to users.
It also includes intelligent handling for fallbacks (when the chatbot doesn't understand the user query) and the ability to switch contexts between tasks.

#Technologies Used
Rasa: Natural Language Understanding (NLU), Python, YAML

#Features
NLU (Natural Language Understanding): Utilizes Rasa NLU to identify and classify user intents such as place_order, track_order, and cancel_order, along with extracting entities like Order Number.
Custom Actions: The bot uses custom Python actions for real-time order validation, setting contexts for different actions, and interacting with external systems (like order databases).
Conversation Flow: The chatbot intelligently handles conversation flows using Rasa stories and rules, enabling the bot to react dynamically to user inputs and adjust its behavior based on context.
Context Switching: If the user changes their request (e.g., from canceling to tracking an order), the bot can easily switch context and continue the conversation without confusion.
Error Handling: The chatbot has robust error handling for cases where it doesn't understand the user’s request or when invalid data (e.g., incorrect order number) is provided.
