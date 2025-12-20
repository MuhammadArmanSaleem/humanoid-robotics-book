import React, { useState, useEffect } from 'react';
import styles from './TextSelectionHandler.module.css';

const TextSelectionHandler = ({ onSelection }) => {
  const [selection, setSelection] = useState(null);
  const [showButton, setShowButton] = useState(false);
  const [buttonPosition, setButtonPosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleSelection = () => {
      const selectedText = window.getSelection().toString().trim();

      if (selectedText) {
        const selectionObj = window.getSelection();
        if (selectionObj.rangeCount > 0) {
          const range = selectionObj.getRangeAt(0);
          const rect = range.getBoundingClientRect();

          // Position the button near the selection, slightly above it
          setButtonPosition({
            x: rect.left + rect.width / 2,
            y: rect.top - 40
          });

          setSelection(selectedText);
          setShowButton(true);
        }
      } else {
        setShowButton(false);
        setSelection(null);
      }
    };

    // Use a delay to ensure the selection is complete
    const handleMouseUp = () => {
      setTimeout(handleSelection, 500); // 500ms delay to avoid interference
    };

    const handleTouchEnd = () => {
      setTimeout(handleSelection, 500);
    };

    // Add event listeners
    document.addEventListener('mouseup', handleMouseUp);
    document.addEventListener('touchend', handleTouchEnd);

    // Cleanup event listeners
    return () => {
      document.removeEventListener('mouseup', handleMouseUp);
      document.removeEventListener('touchend', handleTouchEnd);
    };
  }, []);

  const handleAskAbout = () => {
    if (selection && onSelection) {
      onSelection(selection);
      setShowButton(false);
      // Clear the selection
      window.getSelection().removeAllRanges();
    }
  };

  if (!showButton) {
    return null;
  }

  return (
    <div
      className={styles.selectionButton}
      style={{
        left: `${buttonPosition.x}px`,
        top: `${buttonPosition.y}px`,
        transform: 'translateX(-50%)',
      }}
    >
      <button
        onClick={handleAskAbout}
        className={styles.askButton}
      >
        Ask about this
      </button>
    </div>
  );
};

export default TextSelectionHandler;