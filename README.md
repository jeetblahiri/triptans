
# Triptans – Flask app (ready for Render/Heroku/Railway)

## Project structure
```
triptans/
├─ app.py
├─ requirements.txt
├─ Procfile
└─ templates/
   ├─ index.html
   └─ result.html
```

## Local run
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
# open http://localhost:8080
```

## Model scoring
The app uses a seven-item yes/no questionnaire:

| S.No. | Question | Yes score |
| --- | --- | --- |
| 1 | Is the HIT-6 score between 60-78? | 2 |
| 2 | Does the patient experience photophobia or phonophobia during headache? | 1 |
| 3 | Does severe headache last for more than 2 hours? | 1 |
| 4 | Do headache attacks last for more than 4 hours? | 1 |
| 5 | Does headache limit daily activities? | 1 |
| 6 | Does the patient experience headache on more than 15 days per month? | 1 |
| 7 | Is the NPRS score more than 7/10? | 1 |

Maximum total score is 8. A score greater than 4 is interpreted as
`Triptan Failure`; a score of 4 or lower is interpreted as
`Triptan Responder`.

## Deploy (Render example)
1. Push this folder to a GitHub repo.
2. On Render, create **Web Service** → connect the repo.
3. Runtime: Python 3.11+
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn app:app`
6. Render will set `$PORT` automatically – app.py reads it.

> Note: Netlify does **not** run Python/Flask servers. If you want to keep Netlify for the frontend, host this Flask backend on Render/Railway and point your frontend to it (or add a proxy).
