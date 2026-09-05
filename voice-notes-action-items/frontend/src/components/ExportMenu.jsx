import { useState, useRef, useEffect } from 'react';
import jsPDF from 'jspdf';

export default function ExportMenu({ tasks }) {
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    const handleClick = (e) => {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false);
    };
    if (open) document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, [open]);

  const copyMarkdown = () => {
    if (tasks.length === 0) return;
    const markdown = tasks.map(t => {
      const status = t.completed ? '[x]' : '[ ]';
      const deadline = t.deadline ? ` (due: ${t.deadline})` : '';
      const priority = t.priority ? ` [${t.priority}]` : '';
      return `- ${status} ${t.task}${deadline}${priority}`;
    }).join('\n');
    navigator.clipboard.writeText(markdown);
    setOpen(false);
  };

  const exportCSV = () => {
    if (tasks.length === 0) return;
    const headers = ['Task', 'Deadline', 'Priority', 'Category', 'Status'];
    const rows = tasks.map(t => [
      `"${t.task.replace(/"/g, '""')}"`,
      `"${t.deadline || ''}"`,
      `"${t.priority || ''}"`,
      `"${t.category || ''}"`,
      t.completed ? 'Completed' : 'Pending'
    ]);
    const csv = [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'voice_notes_tasks.csv';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    setOpen(false);
  };

  const exportPDF = () => {
    if (tasks.length === 0) return;
    const doc = new jsPDF();
    doc.setFontSize(18);
    doc.text('Voice Notes', 14, 22);
    doc.setFontSize(11);
    let y = 35;
    tasks.forEach((t, i) => {
      if (y > 270) { doc.addPage(); y = 20; }
      const status = t.completed ? '[x]' : '[ ]';
      const deadline = t.deadline ? ` (due: ${t.deadline})` : '';
      const text = `${i + 1}. ${status} ${t.task}${deadline}`;
      const split = doc.splitTextToSize(text, 180);
      doc.text(split, 14, y);
      y += (split.length * 7) + 3;
    });
    doc.save('voice_notes_tasks.pdf');
    setOpen(false);
  };

  const exportICS = () => {
    if (tasks.length === 0) return;
    let ics = 'BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Voice Notes//EN\n';
    tasks.forEach(t => {
      const now = new Date();
      const dtstamp = now.toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
      ics += `BEGIN:VEVENT\nUID:${t.id}-${now.getTime()}@voicenotes.local\nDTSTAMP:${dtstamp}\nDTSTART;VALUE=DATE:${dtstamp.substring(0, 8)}\nSUMMARY:${t.task}\nDESCRIPTION:Deadline: ${t.deadline || 'None'} | Priority: ${t.priority}\nEND:VEVENT\n`;
    });
    ics += 'END:VCALENDAR';
    const blob = new Blob([ics], { type: 'text/calendar;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'voice_notes_tasks.ics';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    setOpen(false);
  };

  return (
    <div className="export-wrapper" ref={ref}>
      <button
        className={`export-trigger ${open ? 'open' : ''}`}
        onClick={() => setOpen(!open)}
      >
        Export <span className="chevron">&#9662;</span>
      </button>
      {open && (
        <div className="export-menu">
          <button onClick={copyMarkdown}>Copy Markdown</button>
          <button onClick={exportCSV}>Download CSV</button>
          <button onClick={exportPDF}>Download PDF</button>
          <button onClick={exportICS}>Export Calendar</button>
        </div>
      )}
    </div>
  );
}
