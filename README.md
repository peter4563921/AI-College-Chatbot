# AI-Powered College Enquiry Chatbot

A full-stack MCA final year project for college enquiries. Students, parents and visitors can ask natural language questions. Admins can update the knowledge base, and chatbot answers reflect changes immediately.

## Tech Stack

Frontend: HTML5, CSS3, JavaScript, responsive glassmorphism UI.
Backend: Python Flask REST API.
Database: MySQL.
AI: Google Gemini API.
Deployment: GitHub and Render.

## Local Setup

1. Create a MySQL database named college_chatbot.
2. Run database/schema.sql and database/seed.sql.
3. Copy .env.example to .env and update MySQL and Gemini values.
4. Install dependencies with: pip install -r requirements.txt
5. Run backend with: python -m backend.app
6. Open frontend/index.html for chatbot and frontend/admin.html for admin panel.

Default admin seeded for demo:
Email: admin@kvcet.edu
Password: admin123

Change the admin password before production use.

## Main APIs

POST /chat
POST /login
POST /admin/login
GET /courses
GET /fees
GET /placements
GET /hostel
GET /admission
GET /departments
GET /scholarships
GET /contact
GET/POST/PUT/DELETE /admin/<resource>

## Deployment

Push this folder to GitHub. Create a Render Python Web Service. Use build command pip install -r requirements.txt and start command gunicorn backend.app:app. Add all variables from .env.example in Render settings. Use an external MySQL provider and import the SQL files.

## Safety

The chatbot uses only the database knowledge base as context. If the question is unrelated or information is missing, it politely refuses instead of guessing.
