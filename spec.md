# 🎙️ Voice Notes → Action Items

## 1. Project Overview

**Voice Notes → Action Items** is an AI-powered application that converts spoken voice notes into clear, structured and actionable tasks.

The user can record a voice note or enter text manually. The application uses AI to understand the note and extract important action items, deadlines, and priorities.

### Core Pipeline

```text
🎤 Voice Note
      ↓
📝 Speech-to-Text
      ↓
🤖 AI / LLM
      ↓
🔍 Action Item Extraction
      ↓
✅ Structured Action Items
```

---

# 2. Problem Statement

People often record voice notes containing multiple tasks, reminders, deadlines, and ideas.

However, manually converting these notes into organized tasks takes time and important actions can be missed.

This project automatically transforms unstructured voice notes into structured action items.

---

# 3. Objective

The main objective is to build a simple AI assistant that can:

* Accept a voice note.
* Convert speech into text.
* Understand the meaning of the note.
* Identify actionable tasks.
* Extract deadlines.
* Determine task priority.
* Display the results in an easy-to-use task list.

---

# 4. Target Users

The application can be useful for:

* Students
* Developers
* Professionals
* Teachers
* Project teams
* Anyone who uses voice notes for reminders and tasks

---

# 5. Core Features

## 5.1 Voice Recording

The user can record a voice note directly from the browser.

### Features

* Start recording
* Stop recording
* Recording status
* Audio processing indicator
* Clear recording option

Example:

```text
🎤 Start Recording

Recording...

⏹ Stop Recording
```

---

# 5.2 Speech-to-Text

The recorded audio is sent to the backend and converted into text using a Speech-to-Text model/API.

### Example Input

```text
Tomorrow I need to finish the college project and call Rahul about the presentation. I also need to submit the report by Monday.
```

### Transcript

```text
Tomorrow I need to finish the college project and call Rahul about the presentation. I also need to submit the report by Monday.
```

---

# 5.3 AI Action Item Extraction

The transcript is sent to an LLM.

The LLM identifies actionable tasks and extracts useful information.

### Information to Extract

Each action item should contain:

* Task
* Deadline
* Priority

### Example

Input:

```text
Tomorrow I need to finish the college project and call Rahul about the presentation. I also need to submit the report by Monday.
```

Output:

```json
{
  "action_items": [
    {
      "task": "Finish the college project",
      "deadline": "Tomorrow",
      "priority": "High"
    },
    {
      "task": "Call Rahul about the presentation",
      "deadline": null,
      "priority": "Medium"
    },
    {
      "task": "Submit the report",
      "deadline": "Monday",
      "priority": "High"
    }
  ]
}
```

---

# 6. Summary Generation

The AI should also generate a short summary of the voice note.

### Example

```text
You have three tasks related to your college project and presentation.
```

The summary should be short and easy to understand.

---

# 7. Text Input

The application should also support manual text input.

This allows users to test the application without recording audio.

### Example

```text
Complete the assignment by Friday and send the project report to the professor.
```

The application sends the text directly to the AI extraction system.

---

# 8. Action Items UI

The extracted tasks should be displayed as cards or a task list.

### Example

```text
┌──────────────────────────────────────┐
│ ☐ Finish the college project        │
│                                      │
│ 📅 Tomorrow                          │
│ 🔴 High Priority                     │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ ☐ Call Rahul about presentation     │
│                                      │
│ 📅 No deadline                       │
│ 🟡 Medium Priority                   │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ ☐ Submit the report                 │
│                                      │
│ 📅 Monday                            │
│ 🔴 High Priority                     │
└──────────────────────────────────────┘
```

---

# 9. Task Management

The user should be able to manage extracted tasks.

### Required Actions

* Mark task as completed
* Unmark task
* Delete task
* Clear all tasks

Completed tasks should have a visual indication.

Example:

```text
☑ Submit project report
```

---

# 10. Application States

The application should clearly show what is happening.

### State 1 — Ready

```text
Ready to record
```

### State 2 — Recording

```text
🔴 Recording...
```

### State 3 — Transcribing

```text
📝 Transcribing your voice...
```

### State 4 — Analyzing

```text
🤖 AI is finding your action items...
```

### State 5 — Completed

```text
✅ Action items ready
```

### State 6 — Error

```text
❌ Something went wrong.

Please try again.
```

---

# 11. Backend API

## 11.1 Transcription API

### Endpoint

```text
POST /api/transcribe
```

### Input

Audio file.

### Output

```json
{
  "transcript": "The transcribed voice note"
}
```

---

# 11.2 Action Item Extraction API

### Endpoint

```text
POST /api/extract-actions
```

### Input

```json
{
  "text": "Finish the project by Friday and call Rahul tomorrow."
}
```

### Output

```json
{
  "summary": "Two project-related tasks were identified.",
  "action_items": [
    {
      "task": "Finish the project",
      "deadline": "Friday",
      "priority": "High"
    },
    {
      "task": "Call Rahul",
      "deadline": "Tomorrow",
      "priority": "Medium"
    }
  ]
}
```

---

# 12. AI Processing Rules

The AI must follow these rules:

1. Extract only actionable tasks.
2. Do not invent tasks.
3. Preserve deadlines mentioned by the user.
4. Identify priority when the context clearly indicates it.
5. Use `null` when no deadline exists.
6. Keep task descriptions concise.
7. Generate a short summary.
8. Return valid JSON.
9. Do not add unnecessary explanations.
10. If there are no actionable tasks, return an empty action item list.

### No Action Example

Input:

```text
Today was a very busy day and I attended three classes.
```

Output:

```json
{
  "summary": "The note describes a busy day with three classes.",
  "action_items": []
}
```

---

# 13. Suggested AI Response Schema

The preferred response format is:

```json
{
  "summary": "Short summary of the note",
  "action_items": [
    {
      "task": "Task description",
      "deadline": "Deadline or null",
      "priority": "High | Medium | Low"
    }
  ]
}
```

---

# 14. Frontend

## Technology

The frontend will use:

* React
* Vite
* JavaScript
* CSS

## Main Components

```text
App
│
├── Header
├── VoiceRecorder
├── TextInput
├── ProcessingStatus
├── Summary
├── ActionItemList
│   └── ActionItem
└── Footer
```

---

# 15. Backend

## Technology

The backend will use:

* Python
* FastAPI
* AI APIs
* Speech-to-Text API

### Backend Structure

```text
backend/
│
├── app/
│   ├── main.py
│   ├── routes/
│   │   ├── transcription.py
│   │   └── actions.py
│   │
│   └── services/
│       ├── speech_to_text.py
│       └── ai_extraction.py
│
├── requirements.txt
└── .env
```

---

# 16. Frontend Structure

```text
frontend/
│
├── src/
│   ├── components/
│   │   ├── VoiceRecorder.jsx
│   │   ├── TextInput.jsx
│   │   ├── ActionItem.jsx
│   │   ├── ActionItemList.jsx
│   │   └── ProcessingStatus.jsx
│   │
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
│
├── package.json
└── vite.config.js
```

---

# 17. Environment Variables

The backend should store API keys in environment variables.

Example:

```env
OPENAI_API_KEY=your_api_key_here
```

Never expose secret API keys in the frontend.

Do not commit `.env` files to GitHub.

---

# 18. Security

The application should:

* Keep API keys on the backend.
* Never expose API keys in frontend JavaScript.
* Add `.env` to `.gitignore`.
* Validate uploaded audio files.
* Handle API errors safely.

---

# 19. Responsive Design

The application should work on:

* Desktop
* Laptop
* Tablet
* Mobile

The main interface should remain simple and easy to use.

---

# 20. User Interface Design

The UI should have:

### Header

```text
🎙️ Voice Notes
Turn your thoughts into action.
```

### Main Area

```text
┌───────────────────────────────────────┐
│                                       │
│          🎤 Record Voice Note         │
│                                       │
│          Click to start               │
│                                       │
└───────────────────────────────────────┘
```

### Alternative Text Input

```text
Or type your note here...

[ Analyze Note ]
```

### Results

```text
Your Action Items

☐ Finish project report
  📅 Tomorrow
  🔴 High

☐ Call Rahul
  📅 No deadline
  🟡 Medium
```

---

# 21. Demo Scenario

The main demonstration should use this voice note:

```text
I need to complete my project documentation tomorrow. I have to submit the final report by Monday. I also need to call Rahul about the presentation.
```

Expected result:

### Summary

```text
Three project-related tasks were identified.
```

### Tasks

```text
1. Complete project documentation
   Deadline: Tomorrow
   Priority: High

2. Submit the final report
   Deadline: Monday
   Priority: High

3. Call Rahul about the presentation
   Deadline: No deadline
   Priority: Medium
```

---

# 22. MVP Scope

The first version should focus only on the core workflow:

```text
Voice
 ↓
Speech-to-Text
 ↓
AI
 ↓
Action Items
 ↓
Task Management
```

The MVP does NOT require:

* User authentication
* Database
* Calendar integration
* Email integration
* Notifications
* Multiple languages
* Real-time streaming
* Mobile application
* Advanced analytics

---

# 23. Future Enhancements

Future versions could include:

* Conversation history
* Multiple languages
* Calendar integration
* Google Tasks integration
* Email reminders
* Due-date notifications
* User accounts
* Database storage
* Team collaboration
* AI-generated task suggestions
* Browser notifications
* Export to PDF/CSV
* Voice playback of extracted tasks

---

# 24. Deployment

## Frontend

Deploy the React frontend using:

```text
Vercel
```

## Backend

Deploy the FastAPI backend using:

```text
Railway
```

### Production Flow

```text
User
 ↓
Vercel Frontend
 ↓
Railway FastAPI Backend
 ↓
Speech-to-Text API
 ↓
LLM API
 ↓
Structured Action Items
 ↓
Vercel Frontend
```

---

# 25. Success Criteria

The project is successful when:

* [ ] User can open the deployed application.
* [ ] User can record a voice note.
* [ ] Audio reaches the backend.
* [ ] Speech is converted into text.
* [ ] AI analyzes the transcript.
* [ ] Action items are extracted.
* [ ] Deadlines are displayed.
* [ ] Priorities are displayed.
* [ ] User can mark tasks as complete.
* [ ] User can delete tasks.
* [ ] Text input also works.
* [ ] Errors are handled properly.
* [ ] The complete workflow works in production.

---

# 26. Final Product

The final application should provide a simple experience:

```text
           VOICE NOTES
                │
                ▼
        🎤 Record a Note
                │
                ▼
         📝 Transcription
                │
                ▼
          🤖 AI Analysis
                │
                ▼
        ┌─────────────────┐
        │ ACTION ITEMS    │
        ├─────────────────┤
        │ ☐ Task 1        │
        │   📅 Tomorrow   │
        │   🔴 High       │
        │                 │
        │ ☐ Task 2        │
        │   📅 Monday     │
        │   🟡 Medium     │
        └─────────────────┘
```

**Primary goal:** Convert an unstructured voice note into useful, structured action items with minimum user effort.
