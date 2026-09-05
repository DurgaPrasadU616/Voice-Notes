# Voice Notes → Action Items

An AI-powered web application that converts unstructured voice notes into organized action items using OpenAI's Whisper and GPT-4o-mini.

## Project Structure

- `/backend` - FastAPI Python application
- `/frontend` - React + Vite application

## Local Development Setup

### Backend
1. `cd backend`
2. Create a virtual environment: `python -m venv .venv`
3. Activate it:
   - Windows: `.venv\Scripts\activate`
   - Mac/Linux: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file based on `.env.example` and add your `OPENAI_API_KEY`.
6. Run the server: `uvicorn app.main:app --reload`
   - The API will be available at `http://localhost:8000`

### Frontend
1. `cd frontend`
2. Install dependencies: `npm install`
3. Run the development server: `npm run dev`
   - The app will be available at `http://localhost:5173`

## Production Deployment

### Backend (e.g., Render, Railway, Heroku)
1. Ensure your deployment platform is set to use Python 3.11+.
2. Set the following Environment Variables in your hosting dashboard:
   - `OPENAI_API_KEY`: Your OpenAI key
   - `FRONTEND_URL`: The deployed URL of your frontend (e.g., `https://my-frontend.vercel.app`)
3. **Start Command**: 
   The platform should start the app using:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
   *(Ensure the host injects the `$PORT` environment variable, which Render does automatically).*
4. A `/health` endpoint is available at the root level to monitor uptime.

### Frontend (e.g., Vercel, Netlify)
1. Connect your GitHub repository to your Vercel/Netlify account.
2. Set the root directory to `frontend`.
3. Set the following Environment Variable in your hosting dashboard:
   - `VITE_API_URL`: The deployed URL of your backend (e.g., `https://my-backend.onrender.com`)
4. Build command: `npm run build`
5. Output directory: `dist`
