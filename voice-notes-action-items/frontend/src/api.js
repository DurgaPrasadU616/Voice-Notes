const API_BASE = import.meta.env.VITE_API_URL || '';

async function fetchWithRetry(url, options, maxRetries = 1, timeoutMs = 30000) {
  for (let i = 0; i <= maxRetries; i++) {
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), timeoutMs);
    try {
      const response = await fetch(url, { ...options, signal: controller.signal });
      clearTimeout(id);
      if (!response.ok) {
        if (response.status === 429) {
          throw new Error("Too many requests. Please wait a moment and try again.");
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (err) {
      clearTimeout(id);
      if (i === maxRetries) {
        if (err.name === 'AbortError') throw new Error("Request timed out. Please try again.");
        throw err;
      }
      console.warn(`Fetch failed for ${url}, retrying... (${i + 1}/${maxRetries})`);
    }
  }
}

export async function transcribeAudio(audioBlob) {
  const formData = new FormData();
  formData.append('audio', audioBlob, 'recording.webm');

  return fetchWithRetry(`${API_BASE}/api/transcribe`, {
    method: 'POST',
    body: formData
  }, 1, 60000); // 60 sec timeout to survive Render cold starts
}

export async function extractActions(text) {
  return fetchWithRetry(`${API_BASE}/api/extract-actions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  }, 1, 60000); // 60 sec timeout to survive Render cold starts
}

export async function saveTasks(tasks) {
  const res = await fetch(`${API_BASE}/api/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(tasks)
  });
  if (!res.ok) throw new Error("Failed to save tasks");
  return res.json();
}

export async function fetchTasks() {
  const res = await fetch(`${API_BASE}/api/tasks`);
  if (!res.ok) throw new Error("Failed to fetch tasks");
  return res.json();
}

export async function updateTask(id, updates) {
  const res = await fetch(`${API_BASE}/api/tasks/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(updates)
  });
  if (!res.ok) throw new Error("Failed to update task");
  return res.json();
}

export async function deleteTask(id) {
  const res = await fetch(`${API_BASE}/api/tasks/${id}`, {
    method: 'DELETE'
  });
  if (!res.ok) throw new Error("Failed to delete task");
  return res.json();
}

export async function clearAllTasks() {
  const res = await fetch(`${API_BASE}/api/tasks`, { method: 'DELETE' });
  if (!res.ok) throw new Error("Failed to clear tasks");
  return res.json();
}
