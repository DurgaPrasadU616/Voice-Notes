import { useState } from 'react';

export default function TextInput({ onAnalyze }) {
  const [text, setText] = useState('');

  const handleSubmit = () => {
    if (text.trim()) {
      onAnalyze(text);
      setText('');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div>
      <span className="section-label">Or type a note</span>
      <textarea
        className="input-styled"
        placeholder="e.g., Finish the report by Friday and call Alex tomorrow morning..."
        value={text}
        maxLength={3000}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={handleKeyDown}
      />
      <button
        className="btn-primary"
        onClick={handleSubmit}
        disabled={!text.trim()}
      >
        Analyze
      </button>
    </div>
  );
}
