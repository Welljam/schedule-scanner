# Schedule Scanner

Turn a **photo of a staff schedule** into **Google Calendar events**. Upload an image, the app reads it with Google's Gemini vision model, lets you review and edit the shifts, then pushes them to your Google Calendar for a chosen week.

## What it does

- Scans a schedule image and extracts each person's weekly hours as structured JSON (Gemini vision).
- Lets the user pick a person, edit start/end times, and choose the target week.
- Sends the selected shifts to Google Calendar via OAuth 2.0.
- For best accuracy, the source schedule should follow a rows-and-columns layout (people as rows, days as columns).

## Expected schedule format

| People | Monday      | Tuesday     | Wednesday   | Thursday    | Friday      | Saturday    | Sunday |
|--------|-------------|-------------|-------------|-------------|-------------|-------------|--------|
| Name 1 | 07:00-16:00 |             | 10:00-14:00 |             | 08:00-12:00 |             |        |
| Name 2 |             | 09:00-17:00 |             | 13:00-19:00 |             |             |        |
| Name 3 | 07:00-16:00 | 07:00-16:00 |             |             | 14:00-19:00 | 10:00-15:00 |        |

*Empty cells mean no shift that day.*

## Tech stack

| Layer | Technology |
|-------|------------|
| Frontend | Angular 21 (standalone components, signals), Angular Material |
| Backend | Python, FastAPI, Pydantic |
| AI / Vision | Google Gemini 3.5 Flash Lite (image → JSON) |
| Integrations | Google Calendar API, Google OAuth 2.0 |
| Auth | OAuth 2.0 + PKCE, refresh tokens, HttpOnly/Secure cookies |
| Hosting | Vercel (Angular static site + FastAPI serverless functions) |
| Tooling | uv (Python deps), Angular CLI |

## Local development

**Backend**
```bash
cd backend
uv run uvicorn backend.main:app --reload   # http://localhost:8000
```

**Frontend**
```bash
cd frontend
npm install
ng serve                                   # http://localhost:4200
```

Requires a `backend/.env` with:
```
GEMINI_API_KEY=...
CLIENT_ID=...
CLIENT_SECRET=...
```