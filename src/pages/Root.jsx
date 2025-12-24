import React from 'react';
import ChatWidget from '../components/ChatWidget/ChatWidget';
import TextSelectionHandler from '../components/TextSelectionHandler/TextSelectionHandler';

// Global state to handle text selection
let globalSelectedText = '';

const setGlobalSelectedText = (text) => {
  globalSelectedText = text;
};

const getGlobalSelectedText = () => {
  return globalSelectedText;
};

const Root = ({ children }) => {
  return (
    <>
      {children}
      <TextSelectionHandler onSelection={setGlobalSelectedText} />
      <ChatWidget selectedText={getGlobalSelectedText()} />
    </>
  );
};

export default Root;