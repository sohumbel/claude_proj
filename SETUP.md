# Resume Roaster - Full Stack Setup Guide

This guide will help you set up and run the complete Resume Roaster application, connecting the React frontend to the Python backend.

## Architecture Overview

```
Frontend (React + Vite)
    ↓ HTTP API
Backend Server (FastAPI)
    ↓ Processing
Python Modules (parser → analyzer → roaster)
    ↓ AI Generation
Claude API + Video Generation
```

## Prerequisites

- **Node.js** (v18 or higher)
- **Python** (v3.8 or higher)
- **Anthropic API Key** (get one at https://console.anthropic.com/)

## Backend Setup

### 1. Install Python Dependencies

```bash
cd resume-roaster
pip install -r requirements.txt
```

This will install:
- FastAPI & Uvicorn (web server)
- Anthropic (Claude AI)
- pdfplumber & python-docx (resume parsing)
- gTTS & moviepy (video generation)
- Other dependencies

### 2. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:

```bash
ANTHROPIC_API_KEY=your_api_key_here
```

### 3. Start the Backend Server

```bash
python server.py
```

The backend API will start on http://localhost:8000

You can view API documentation at: http://localhost:8000/docs

## Frontend Setup

### 1. Install Node Dependencies

```bash
# From the project root directory
npm install
```

### 2. Configure Environment Variables (Optional)

If you're running the backend on a different host/port, create a `.env.local` file:

```bash
cp .env.example .env.local
```

Edit `.env.local` to set the backend URL (default is http://localhost:8000):

```bash
VITE_API_URL=http://localhost:8000
```

### 3. Start the Frontend Development Server

```bash
npm run dev
```

The frontend will start on http://localhost:5173

## Running the Complete Application

1. **Start Backend** (Terminal 1):
   ```bash
   cd resume-roaster
   python server.py
   ```

2. **Start Frontend** (Terminal 2):
   ```bash
   npm run dev
   ```

3. **Open Browser**:
   Navigate to http://localhost:5173

## How It Works

### Upload Flow

1. User uploads PDF resume on the frontend
2. Frontend sends file to `POST /api/upload` endpoint
3. Backend saves file and returns a `job_id`
4. Frontend navigates to `/generate?jobId={job_id}`

### Processing Flow

1. Frontend polls `GET /api/status/{job_id}` every 2 seconds
2. Backend processes resume through stages:
   - **Analyzing**: Parsing PDF and analyzing content
   - **Roasting**: Generating roast text with Claude AI
   - **Generating**: Creating video with text-to-speech
   - **Complete**: Video ready for viewing

3. When complete, frontend displays video using `GET /api/video/{job_id}`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/api/upload` | POST | Upload resume and start processing |
| `/api/status/{job_id}` | GET | Get processing status |
| `/api/result/{job_id}` | GET | Get final results |
| `/api/video/{job_id}` | GET | Stream/download video |

## Troubleshooting

### Backend Issues

**ImportError: No module named 'fastapi'**
- Solution: Install dependencies with `pip install -r requirements.txt`

**API Key Error**
- Solution: Make sure your `.env` file has a valid `ANTHROPIC_API_KEY`

**Video Generation Not Working**
- Check that gTTS and moviepy are installed
- MoviePy may require additional system dependencies (ffmpeg)
- Install ffmpeg:
  - macOS: `brew install ffmpeg`
  - Ubuntu: `apt-get install ffmpeg`
  - Windows: Download from ffmpeg.org

### Frontend Issues

**CORS Error**
- Solution: Make sure backend is running and CORS is configured (already done in server.py)

**API Connection Failed**
- Check that backend is running on port 8000
- Verify VITE_API_URL in `.env.local` matches backend URL

**Upload Fails**
- Check file is PDF format and under 10MB
- Check browser console for error messages

### Common Issues

**Port Already in Use**
- Backend: Change port in server.py (default 8000)
- Frontend: Vite will automatically use next available port

**Processing Takes Too Long**
- First run may be slower (Claude API cold start)
- Video generation can take 30-60 seconds
- Check backend terminal for progress logs

## Development Tips

### Hot Reload

- Frontend: Changes auto-reload thanks to Vite
- Backend: Server runs with `reload=True`, so code changes trigger restart

### Debugging

- Backend logs appear in terminal running `python server.py`
- Frontend console: Open browser DevTools (F12)
- API Testing: Use Swagger UI at http://localhost:8000/docs

### Video Generation

The video generation uses:
- **gTTS** for text-to-speech (Google's TTS)
- **moviepy** for video creation

For production, consider upgrading to:
- ElevenLabs API (better voice quality)
- D-ID or Synthesia (talking avatar videos)

## Production Deployment

### Backend

1. Use production WSGI server (gunicorn):
   ```bash
   gunicorn server:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
   ```

2. Add job queue (Celery/Redis) for async processing

3. Use database (PostgreSQL) instead of in-memory job storage

4. Add file storage (S3/CloudFlare R2) for videos

### Frontend

1. Build for production:
   ```bash
   npm run build
   ```

2. Deploy `dist/` folder to:
   - Vercel
   - Netlify
   - CloudFlare Pages
   - Any static hosting

3. Set environment variable:
   ```
   VITE_API_URL=https://your-api-domain.com
   ```

## Tech Stack Summary

**Frontend:**
- React 18
- TypeScript
- Vite
- Tailwind CSS
- shadcn/ui
- React Router
- TanStack Query

**Backend:**
- FastAPI
- Python 3.8+
- Anthropic Claude API
- pdfplumber
- gTTS
- moviepy

## Next Steps

- Add authentication (user accounts)
- Store roast history
- Add more roast tones/personalities
- Improve video generation with avatars
- Add social sharing features
- Mobile app

## Support

For issues or questions:
- Check backend logs for errors
- Check browser console for frontend errors
- Review API docs at http://localhost:8000/docs

Happy roasting! 🔥
