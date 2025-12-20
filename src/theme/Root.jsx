import React, { useState } from 'react';
import { AuthProvider } from './AuthContext';
import ChatWidget from '../components/ChatWidget/ChatWidget';
import TextSelectionHandler from '../components/TextSelectionHandler/TextSelectionHandler';

const Root = ({ children }) => {
  const [selectedText, setSelectedText] = useState('');

  return (
    <AuthProvider>
      <>
        {children}
        <TextSelectionHandler onSelection={setSelectedText} />
        <ChatWidget selectedText={selectedText} />
      </>
    </AuthProvider>
  );
};

export default Root;