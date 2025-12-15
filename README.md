# Portfolio Backend API

FastAPI backend server for the Portfolio application providing contact form email functionality.

## Features

- **FastAPI** - Modern, fast web framework for building APIs
- **CORS Support** - Configured to work with Next.js frontend
- **Email Support** - Send contact form submissions via email (SMTP)
- **Auto-generated Documentation** - Available at `/docs` and `/redoc`
- **Type Safety** - Using Pydantic models for request/response validation

## Setup

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure email settings:
   - Copy `.env.example` to `.env`
   - Update the email configuration with your SMTP credentials

**For Gmail:**
- Set `SMTP_USER` to your Gmail address
- Set `SMTP_PASSWORD` to an [App Password](https://support.google.com/accounts/answer/185833) (not your regular password)
- Set `RECIPIENT_EMAIL` to the email where you want to receive contact form submissions

Example `.env`:
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-16-char-app-password
RECIPIENT_EMAIL=your-email@gmail.com
```

4. Run the server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

- `GET /` - Root endpoint with API info
- `GET /health` - Health check endpoint
- `POST /api/contact` - Submit contact form (sends email)

### Contact Form Payload

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "subject": "Question about your portfolio",
  "message": "I'd like to discuss a project..."
}
```

## Documentation

Once the server is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Development

The server runs on:
- **Host:** 0.0.0.0
- **Port:** 8000
- **Auto-reload:** Enabled

Frontend (Next.js) should be running on port 3000.

## Deployment

### Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

**Option 1: Using Render Dashboard (Recommended)**

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New +** → **Web Service**
3. Connect your GitHub/GitLab repository
4. Configure the service:
   - **Name:** `jitendra-portfolio-api`
   - **Runtime:** `Python`
   - **Build Command:** `pip install -r requirements.txt` or `./build.sh`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT` or `./start.sh`
5. Add Environment Variables in the **Environment** section:
   - `ALLOWED_ORIGINS` - Your frontend URL (e.g., `https://your-app.vercel.app`)
   - `GEMINI_API_KEY` - Your Gemini API key
   - `GEMINI_MODEL_NAME` - Gemini model name
   - `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `RECIPIENT_EMAIL` - Email config
   - `UNREAL_SPEECH_API_KEY`, `UNREAL_SPEECH_VOICE` - Speech API config (optional)
   - `OPENROUTER_API_KEY`, `OPENROUTER_MODEL` - OpenRouter config (optional)
6. Click **Create Web Service**

**Option 2: Using Blueprint (render.yaml)**

1. Fork/push this repository to your GitHub account
2. In Render Dashboard, click **New +** → **Blueprint**
3. Connect to your repository containing `render.yaml`
4. Render will auto-detect and configure the service
5. Configure environment variables in the dashboard

**Render Files:**
- `render.yaml` - Blueprint configuration
- `build.sh` - Build script
- `start.sh` - Start script

---

### Deploy to Railway

1. Go to [Railway](https://railway.app/)
2. Click **New Project** → **Deploy from GitHub repo**
3. Select your repository
4. Railway will auto-detect `railway.json` and configure the service
5. Add environment variables in the **Variables** tab
6. Deploy!

**Railway Files:**
- `railway.json` - Railway configuration
- `Procfile` - Process configuration
