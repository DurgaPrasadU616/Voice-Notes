import { useState, useEffect, useRef } from 'react';
import * as api from './api';
import VoiceRecorder from './components/VoiceRecorder';
import TextInput from './components/TextInput';
import ProcessingStatus from './components/ProcessingStatus';
import Summary from './components/Summary';
import ActionItemList from './components/ActionItemList';
import TaskFilters from './components/TaskFilters';
import ThemeToggle from './components/ThemeToggle';
import Toast from './components/Toast';
import ExportMenu from './components/ExportMenu';

export default function App() {
  const [tasks, setTasks] = useState([]);
  const [summary, setSummary] = useState('');
  const [filter, setFilter] = useState({ status: 'All', priority: 'All' });
  const [sort, setSort] = useState('createdAt');
  const [processingStep, setProcessingStep] = useState('');
  const [isLoadingTasks, setIsLoadingTasks] = useState(true);
  const [toast, setToast] = useState({ message: '', type: '', actionLabel: '', onAction: null });
  const pendingDeletes = useRef(new Map());

  const playSuccessFeedback = () => {
    if (navigator.vibrate) navigator.vibrate([100, 50, 100]);
    try {
      const ctx = new (window.AudioContext || window.webkitAudioContext)();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.type = 'sine';
      osc.frequency.setValueAtTime(800, ctx.currentTime);
      gain.gain.setValueAtTime(0.1, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.1);
      osc.start();
      osc.stop(ctx.currentTime + 0.1);
    } catch (e) {}
  };

  useEffect(() => { loadTasks(); }, []);

  const loadTasks = async () => {
    setIsLoadingTasks(true);
    try {
      const data = await api.fetchTasks();
      setTasks(data);
    } catch (err) {
      showToast('Failed to load tasks.', 'error');
    } finally {
      setIsLoadingTasks(false);
    }
  };

  const showToast = (message, type = 'success', actionLabel = null, onAction = null) => {
    setToast({ message, type, actionLabel, onAction });
  };

  const handleAudioRecording = async (audioBlob) => {
    try {
      setProcessingStep('Transcribing audio...');
      const { transcript } = await api.transcribeAudio(audioBlob);
      if (!transcript || transcript.trim() === '') {
        showToast('No speech detected. Please try again.', 'error');
        setProcessingStep('');
        return;
      }
      await processText(transcript);
    } catch (err) {
      console.error(err);
      showToast(err.message || 'Error during transcription.', 'error');
      setProcessingStep('');
    }
  };

  const handleTextAnalyze = async (text) => {
    if (!text || text.trim() === '') {
      showToast('Please enter some text.', 'error');
      return;
    }
    if (text.length > 3000) {
      showToast('Text is too long (max 3000 characters).', 'error');
      return;
    }
    await processText(text);
  };

  const processText = async (text) => {
    try {
      setProcessingStep('Analyzing text for actions...');
      const result = await api.extractActions(text);
      setSummary(result.summary);
      if (result.action_items && result.action_items.length > 0) {
        setProcessingStep('Saving tasks...');
        await api.saveTasks(result.action_items);
        await loadTasks();
        playSuccessFeedback();
        showToast('Tasks successfully extracted.', 'success');
      } else {
        showToast('No actionable tasks found in the note.', 'success');
      }
    } catch (err) {
      console.error(err);
      showToast(err.message || 'Failed to process the note.', 'error');
    } finally {
      setProcessingStep('');
    }
  };

  const toggleTask = async (task) => {
    try {
      const updated = await api.updateTask(task.id, { completed: !task.completed });
      setTasks(tasks.map(t => t.id === updated.id ? updated : t));
    } catch (err) {
      showToast('Failed to update task status.', 'error');
    }
  };

  const updateTask = async (id, updates) => {
    try {
      const updated = await api.updateTask(id, updates);
      setTasks(tasks.map(t => t.id === updated.id ? updated : t));
      showToast('Task updated.', 'success');
    } catch (err) {
      showToast('Failed to update task.', 'error');
    }
  };

  const deleteTask = (id) => {
    const taskToDelete = tasks.find(t => t.id === id);
    if (!taskToDelete) return;
    setTasks(prev => prev.filter(t => t.id !== id));
    const timeoutId = setTimeout(async () => {
      try {
        await api.deleteTask(id);
        pendingDeletes.current.delete(id);
      } catch (err) {
        setTasks(prev => [...prev, taskToDelete]);
        showToast('Failed to delete task.', 'error');
      }
    }, 5000);
    pendingDeletes.current.set(id, { timeoutId, task: taskToDelete });
    showToast('Task deleted.', 'action', 'Undo', () => {
      const pending = pendingDeletes.current.get(id);
      if (pending) {
        clearTimeout(pending.timeoutId);
        setTasks(prev => [...prev, pending.task]);
        pendingDeletes.current.delete(id);
        showToast('Deletion undone.', 'success');
      }
    });
  };

  const clearAllTasks = async () => {
    if (!window.confirm('Are you sure you want to clear all tasks?')) return;
    try {
      await api.clearAllTasks();
      setTasks([]);
      setSummary('');
      showToast('All tasks cleared.', 'success');
    } catch (err) {
      showToast('Failed to clear tasks.', 'error');
    }
  };

  const clearCompletedTasks = async () => {
    if (!window.confirm('Are you sure you want to clear completed tasks?')) return;
    try {
      const completed = tasks.filter(t => t.completed);
      for (const t of completed) {
        await api.deleteTask(t.id);
      }
      setTasks(tasks.filter(t => !t.completed));
      showToast('Completed tasks cleared.', 'success');
    } catch (err) {
      showToast('Failed to clear some tasks.', 'error');
      await loadTasks();
    }
  };

  return (
    <div className="container">
      <header className="app-header">
        <div>
          <h1>Voice Notes</h1>
          <p className="tagline">Turn your thoughts into action.</p>
        </div>
        <ThemeToggle />
      </header>

      <main className="main-layout">
        <div className="input-section">
          <VoiceRecorder onRecordingComplete={handleAudioRecording} />
          <TextInput onAnalyze={handleTextAnalyze} />
          <ProcessingStatus step={processingStep} />
          {summary && !processingStep && <Summary text={summary} />}
        </div>

        <div className="results-section">
          {!processingStep && (
            <section>
              <div className="results-header">
                <span className="section-label">Action Items</span>
                <div className="results-actions">
                  {!isLoadingTasks && tasks.length > 0 && <ExportMenu tasks={tasks} />}
                  {tasks.some(t => t.completed) && (
                    <button className="btn-ghost" onClick={clearCompletedTasks}>Clear completed</button>
                  )}
                  {tasks.length > 0 && (
                    <button className="btn-ghost danger" onClick={clearAllTasks}>Clear all</button>
                  )}
                </div>
              </div>

              <TaskFilters filter={filter} setFilter={setFilter} sort={sort} setSort={setSort} />

              <ActionItemList
                tasks={tasks}
                filter={filter}
                sort={sort}
                isLoading={isLoadingTasks}
                onToggle={toggleTask}
                onDelete={deleteTask}
                onUpdate={updateTask}
              />
            </section>
          )}
        </div>
      </main>

      <Toast
        message={toast.message}
        type={toast.type}
        actionLabel={toast.actionLabel}
        onAction={toast.onAction}
        onClose={() => setToast({ message: '', type: '', actionLabel: '', onAction: null })}
      />
    </div>
  );
}
