import { useState, useRef, useEffect } from 'react';

export default function VoiceRecorder({ onRecordingComplete }) {
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const timerRef = useRef(null);

  useEffect(() => {
    if (isRecording) {
      timerRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);
    } else {
      clearInterval(timerRef.current);
      setRecordingTime(0);
    }
    return () => clearInterval(timerRef.current);
  }, [isRecording]);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && isRecording) {
        cancelRecording();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isRecording]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      mediaRecorderRef.current.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data);
      };
      mediaRecorderRef.current.onstop = () => {
        if (chunksRef.current.length > 0) {
          const type = mediaRecorderRef.current.mimeType || 'audio/webm';
          const audioBlob = new Blob(chunksRef.current, { type });
          onRecordingComplete(audioBlob);
        }
        chunksRef.current = [];
        stream.getTracks().forEach(track => track.stop());
      };
      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (err) {
      console.error('Error accessing microphone:', err);
      alert('Microphone access is required to record voice notes.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const cancelRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      chunksRef.current = [];
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const formatTime = (seconds) => {
    const m = Math.floor(seconds / 60).toString().padStart(2, '0');
    const s = (seconds % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
  };

  const progressPercent = isRecording ? Math.min((recordingTime / 120) * 100, 100) : 0;

  return (
    <div>
      <span className="section-label">Record</span>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1rem', padding: '2rem 0' }}>
        <button
          className={`rec-mic ${isRecording ? 'recording' : ''}`}
          onClick={isRecording ? stopRecording : startRecording}
        >
          {isRecording ? (
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <rect x="4" y="4" width="12" height="12" rx="1" fill="var(--accent)" />
            </svg>
          ) : (
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M10 2C8.34 2 7 3.34 7 5V10C7 11.66 8.34 13 10 13C11.66 13 13 11.66 13 10V5C13 3.34 11.66 2 10 2Z" stroke="var(--fg)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M5 9V10C5 12.76 7.24 15 10 15C12.76 15 15 12.76 15 10V9" stroke="var(--fg)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M10 15V18" stroke="var(--fg)" strokeWidth="1.5" strokeLinecap="round"/>
              <path d="M8 18H12" stroke="var(--fg)" strokeWidth="1.5" strokeLinecap="round"/>
            </svg>
          )}
        </button>

        {isRecording ? (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem', width: '100%' }}>
            <span style={{ fontSize: '0.82rem', fontVariantNumeric: 'tabular-nums', color: 'var(--fg-muted)' }}>
              {formatTime(recordingTime)} <span style={{ opacity: 0.5 }}>· Esc to cancel</span>
            </span>
            <div className="rec-progress-track">
              <div className="rec-progress-fill" style={{ width: `${progressPercent}%` }} />
            </div>
          </div>
        ) : (
          <span style={{ fontSize: '0.82rem', color: 'var(--fg-muted)' }}>Tap to start recording</span>
        )}
      </div>
    </div>
  );
}
