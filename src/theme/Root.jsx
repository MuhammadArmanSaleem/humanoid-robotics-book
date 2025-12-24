import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { AuthProvider } from './AuthContext';
import ChatWidget from '../components/ChatWidget/ChatWidget';
import TextSelectionHandler from '../components/TextSelectionHandler/TextSelectionHandler';
import NavbarAuth from '../components/NavbarAuth/NavbarAuth';

const Root = ({ children }) => {
  const [selectedText, setSelectedText] = useState('');

  // Inject NavbarAuth into navbar after mount
  useEffect(() => {
    const container = document.getElementById('navbar-auth-container');
    if (container) {
      ReactDOM.render(
        <AuthProvider>
          <NavbarAuth />
        </AuthProvider>,
        container
      );
      return () => {
        ReactDOM.unmountComponentAtNode(container);
      };
    }
  }, []);

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