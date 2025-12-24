import React, { useState, useEffect, useRef } from 'react';
import { useBaseUrl } from '@docusaurus/useBaseUrl';
import clsx from 'clsx';
import styles from './ChatWidget.module.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const ChatWidget = ({ selectedText = '' }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Initialize session and widget state when component mounts
  useEffect(() => {
    const initSession = async () => {
      // Use existing session if available, otherwise create new one
      const existingSessionId = localStorage.getItem('chatbot_session_id');
      if (existingSessionId) {
        setSessionId(existingSessionId);
      }
    };

    // Restore chat widget open/closed state from localStorage
    const savedState = localStorage.getItem('chat-widget-state');
    if (savedState) {
      try {
        const parsedState = JSON.parse(savedState);
        setIsOpen(parsedState.isOpen || false);
      } catch (e) {
        // If parsing fails, default to closed
        setIsOpen(false);
      }
    }

    initSession();
  }, []);

  // Persist chat widget state to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('chat-widget-state', JSON.stringify({ isOpen }));
  }, [isOpen]);

  // Handle sending a message
  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString(),
    };

    // Add user message and loading indicator to chat
    const loadingMessage = {
      id: Date.now() + 0.5,
      role: 'loading',
      content: 'Thinking...',
      timestamp: new Date().toISOString(),
    };
    setMessages(prev => [...prev, userMessage, loadingMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Prepare the request with context
      const requestBody = {
        message: inputValue,
        context: {
          selected_text: selectedText,
          current_url: window.location.pathname,
          session_id: sessionId,
        },
      };

      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Update session ID if new one was provided
      if (data.session_id && !sessionId) {
        setSessionId(data.session_id);
        localStorage.setItem('chatbot_session_id', data.session_id);
      }

      // Create assistant message
      const assistantMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: data.content,
        sources: data.sources || [],
        navigation: data.navigation || [],
        timestamp: new Date().toISOString(),
      };

      // Remove loading indicator and add assistant message
      setMessages(prev => {
        const withoutLoading = prev.filter(msg => msg.role !== 'loading');
        return [...withoutLoading, assistantMessage];
      });
    } catch (error) {
      console.error('Error sending message:', error);
      // Remove loading indicator and add error message
      setMessages(prev => {
        const withoutLoading = prev.filter(msg => msg.role !== 'loading');
        const errorMessage = {
          id: Date.now() + 1,
          role: 'error',
          content: 'Sorry, I encountered an error. Please try again.',
          timestamp: new Date().toISOString(),
        };
        return [...withoutLoading, errorMessage];
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Handle Enter key press
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Function to render sources
  const renderSources = (sources) => {
    if (!sources || sources.length === 0) return null;

    return (
      <div className={styles.sources}>
        <h4>Sources:</h4>
        <ul>
          {sources.map((source, index) => (
            <li key={index}>
              <a
                href={source.url}
                target="_blank"
                rel="noopener noreferrer"
                className={styles.sourceLink}
              >
                {source.chapter} - {source.lesson}
              </a>
            </li>
          ))}
        </ul>
      </div>
    );
  };

  // Function to render navigation links
  const renderNavigation = (navigation) => {
    if (!navigation || navigation.length === 0) return null;

    return (
      <div className={styles.navigation}>
        <h4>Related Content:</h4>
        <ul>
          {navigation.map((link, index) => (
            <li key={index}>
              <a
                href={link.url}
                target="_blank"
                rel="noopener noreferrer"
                className={styles.navLink}
              >
                {link.title}
              </a>
            </li>
          ))}
        </ul>
      </div>
    );
  };

  // Function to render a message
  const renderMessage = (message) => {
    if (message.role === 'loading') {
      return (
        <div key={message.id} className={styles.loadingIndicator}>
          {message.content}
        </div>
      );
    }
    
    if (message.role === 'error') {
      return (
        <div key={message.id} className={styles.errorMessage}>
          {message.content}
        </div>
      );
    }
    
    return (
      <div key={message.id} className={clsx(styles.message, styles[message.role])}>
        <div className={styles.messageContent}>
          {message.content}
        </div>
        {message.role === 'assistant' && (
          <>
            {renderSources(message.sources)}
            {renderNavigation(message.navigation)}
          </>
        )}
      </div>
    );
  };

  return (
    <div className={styles.chatWidget}>
      {/* Floating button to open chat */}
      {!isOpen && (
        <button
          className={styles.floatingButton}
          onClick={() => setIsOpen(true)}
          aria-label="Open chat"
        >
          💬
        </button>
      )}

      {/* Chat window */}
      {isOpen && (
        <div className={styles.chatWindow}>
          <div className={styles.chatHeader}>
            <h3>Textbook Assistant</h3>
            <button
              className={styles.closeButton}
              onClick={() => setIsOpen(false)}
              aria-label="Close chat"
            >
              ×
            </button>
          </div>

          <div className={styles.chatMessages}>
            {messages.length === 0 ? (
              <div className={styles.emptyState}>
                Hello! I'm your textbook assistant. Ask me anything about the content on this page or any other topic from the textbook.
              </div>
            ) : (
              messages.map(renderMessage)
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className={styles.chatInput}>
            <textarea
              ref={inputRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask a question about the textbook content..."
              rows="2"
              disabled={isLoading}
              className={styles.textInput}
            />
            <button
              onClick={handleSendMessage}
              disabled={!inputValue.trim() || isLoading}
              className={clsx(styles.sendButton, {
                [styles.sendButtonDisabled]: !inputValue.trim() || isLoading,
              })}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatWidget;