import { useEffect } from 'react';

export default function Toast({ message, type, actionLabel, onAction, onClose }) {
  useEffect(() => {
    if (message && type !== 'action') {
      const timer = setTimeout(onClose, 3000);
      return () => clearTimeout(timer);
    } else if (message && type === 'action') {
      const timer = setTimeout(onClose, 5000);
      return () => clearTimeout(timer);
    }
  }, [message, type, onClose]);

  if (!message) return null;

  return (
    <div className="toast-container">
      <div className="toast">
        <span>{message}</span>
        {actionLabel && (
          <button
            className="toast action-btn"
            onClick={() => { onAction(); onClose(); }}
          >
            {actionLabel}
          </button>
        )}
      </div>
    </div>
  );
}
