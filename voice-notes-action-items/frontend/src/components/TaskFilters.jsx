export default function TaskFilters({ filter, setFilter, sort, setSort }) {
  const statusOptions = ['All', 'Pending', 'Completed'];
  const priorityOptions = ['All', 'High', 'Medium', 'Low'];
  const sortOptions = [
    { value: 'createdAt', label: 'Newest' },
    { value: 'deadline', label: 'Deadline' },
    { value: 'priority', label: 'Priority' },
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', marginBottom: '1rem' }}>
      <div className="filter-row">
        {statusOptions.map(opt => (
          <button
            key={opt}
            className={`filter-pill ${filter.status === opt ? 'active' : ''}`}
            onClick={() => setFilter({ ...filter, status: opt })}
          >
            {opt}
          </button>
        ))}
        <div className="filter-divider" />
        {priorityOptions.map(opt => (
          <button
            key={opt}
            className={`filter-pill ${filter.priority === opt ? 'active' : ''}`}
            onClick={() => setFilter({ ...filter, priority: opt })}
          >
            {opt}
          </button>
        ))}
        <div className="filter-divider" />
        {sortOptions.map(opt => (
          <button
            key={opt.value}
            className={`filter-pill ${sort === opt.value ? 'active' : ''}`}
            onClick={() => setSort(opt.value)}
          >
            {opt.label}
          </button>
        ))}
      </div>
    </div>
  );
}
