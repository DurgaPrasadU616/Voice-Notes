import ActionItem from './ActionItem';

const priorityWeight = { High: 3, Medium: 2, Low: 1 };

export default function ActionItemList({ tasks, filter, sort, isLoading, onToggle, onDelete, onUpdate }) {
  if (isLoading) {
    return (
      <div className="task-list">
        {[1, 2, 3].map(i => (
          <div key={i} className="task-item" style={{ pointerEvents: 'none' }}>
            <div className="skeleton" style={{ width: 18, height: 18, borderRadius: 2, marginTop: 3, flexShrink: 0 }} />
            <div className="task-content">
              <div className="skeleton" style={{ width: '60%', height: 16, marginBottom: 6 }} />
              <div className="skeleton" style={{ width: '35%', height: 12 }} />
            </div>
          </div>
        ))}
      </div>
    );
  }

  let processedTasks = [...tasks];

  processedTasks = processedTasks.filter(task => {
    if (filter.status === 'Pending' && task.completed) return false;
    if (filter.status === 'Completed' && !task.completed) return false;
    if (filter.priority !== 'All' && task.priority !== filter.priority) return false;
    return true;
  });

  processedTasks.sort((a, b) => {
    if (sort === 'priority') return (priorityWeight[b.priority] || 0) - (priorityWeight[a.priority] || 0);
    if (sort === 'deadline') {
      if (!a.deadline) return 1;
      if (!b.deadline) return -1;
      return a.deadline.localeCompare(b.deadline);
    }
    return new Date(b.created_at) - new Date(a.created_at);
  });

  if (tasks.length === 0) {
    return (
      <div className="empty-state">
        <h3>No action items yet</h3>
        <p>Record a voice note or type a message to generate your first set of structured tasks.</p>
        <div className="try-example">
          <span className="try-label">Try saying</span>
          <p className="try-text">"Finish the report by Friday and call Alex tomorrow morning."</p>
        </div>
      </div>
    );
  }

  if (processedTasks.length === 0) {
    return (
      <div style={{ padding: '2rem 0', textAlign: 'center', color: 'var(--fg-muted)', fontSize: '0.88rem' }}>
        No tasks match the current filters.
      </div>
    );
  }

  return (
    <div className="task-list">
      {processedTasks.map(task => (
        <ActionItem
          key={task.id}
          task={task}
          onToggle={onToggle}
          onDelete={onDelete}
          onUpdate={onUpdate}
        />
      ))}
    </div>
  );
}
