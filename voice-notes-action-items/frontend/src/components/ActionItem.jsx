import { useState, useRef, useEffect } from 'react';

export default function ActionItem({ task, onToggle, onDelete, onUpdate }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editValue, setEditValue] = useState(task.task);
  const inputRef = useRef(null);

  useEffect(() => {
    if (isEditing && inputRef.current) inputRef.current.focus();
  }, [isEditing]);

  const handleSave = () => {
    const trimmed = editValue.trim();
    if (!trimmed) {
      setEditValue(task.task);
      setIsEditing(false);
      return;
    }
    if (trimmed !== task.task) onUpdate(task.id, { task: trimmed });
    setIsEditing(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') handleSave();
    if (e.key === 'Escape') {
      setEditValue(task.task);
      setIsEditing(false);
    }
  };

  const priority = task.priority?.toLowerCase() || 'low';

  return (
    <div className={`task-item ${task.completed ? 'completed' : ''}`}>
      <input
        type="checkbox"
        className="custom-checkbox"
        checked={task.completed}
        onChange={() => onToggle(task)}
      />
      <div className="task-content">
        <div className="task-header">
          {isEditing ? (
            <input
              ref={inputRef}
              type="text"
              className="task-edit-input"
              value={editValue}
              onChange={(e) => setEditValue(e.target.value)}
              onBlur={handleSave}
              onKeyDown={handleKeyDown}
            />
          ) : (
            <span
              className="task-text"
              onClick={() => setIsEditing(true)}
              title="Click to edit"
            >
              {task.task}
            </span>
          )}
          <button
            className="btn-ghost danger"
            onClick={() => onDelete(task.id)}
            title="Delete task"
            style={{ padding: '0.25rem 0.375rem', fontSize: '0.75rem', flexShrink: 0 }}
          >
            ×
          </button>
        </div>
        <div className="task-meta">
          {task.deadline && (
            <span>{task.deadline}</span>
          )}
          <span style={{ display: 'flex', alignItems: 'center' }}>
            <span className={`priority-dot ${priority}`} />
            {task.priority}
          </span>
          {task.category && (
            <span className="category-label">{task.category}</span>
          )}
        </div>
      </div>
    </div>
  );
}
