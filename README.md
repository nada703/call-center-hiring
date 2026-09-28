# Call Center Hiring Website

## Local run

```bash
pip install -r requirements.txt
python app.py
```

Open:
http://127.0.0.1:5000

## Deploy to Render

1. Create a GitHub repository.
2. Upload:
   - `app.py`
   - `requirements.txt`
   - `render.yaml`
3. In Render: New -> Web Service -> connect the GitHub repo.
4. Use:
   - Language/Runtime: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Plan: Free
5. Deploy.

Render will give the service a public `onrender.com` URL.

## WhatsApp

The form opens WhatsApp to:
01090946660

The applicant's data is pre-filled in the WhatsApp message.
The applicant still needs to press Send.
