# Backend Setup Guide

This guide will help you set up and start the backend for the CodeToGive project.

## 1. Create and Activate a Virtual Environment (Recommended)
```
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

## 2. Install Dependencies
```
pip install -r requirements.txt
```

## 3. Run the Backend
Navigate to the folder containing the Flask app (e.g., `tutorial` or your main app folder):
```
cd tutorial
python flask.py
```
The backend should now be running!
Try `http://localhost:8082/test` to see if it works!

## 6. API Endpoints
- `/test` - Sample endpoint to check if the service is alive

## Troubleshooting
- Ensure all dependencies are installed
- Check your `.env` file for correct values

---

Feel free to contribute and improve the backend!
