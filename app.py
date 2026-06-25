import os
from flask import Flask, render_template, request

app = Flask(__name__)

# List each yes/no questionnaire item and its score in order.
RAW_QUESTIONS = [
    ("Is the HIT-6 score between 60-78?", 2),
    ("Does the patient experience photophobia or phonophobia during headache?", 1),
    ("Does severe headache last for more than 2 hours?", 1),
    ("Do headache attacks last for more than 4 hours?", 1),
    ("Does headache limit daily activities?", 1),
    ("Does the patient experience headache on more than 15 days per month?", 1),
    ("Is the NPRS score more than 7/10?", 1),
]

QUESTIONS = [
    {"key": f"q{i}", "text": text, "score": score}
    for i, (text, score) in enumerate(RAW_QUESTIONS, 1)
]
KEYS = [q["key"] for q in QUESTIONS]
MAX_SCORE = sum(q["score"] for q in QUESTIONS)
FAILURE_THRESHOLD = 4

# ──────────────────────────────────────────────────────────────
# 3️⃣  Decision engine - implements the provided scoring rules

def calculate_score(ans):
    return sum(q["score"] for q in QUESTIONS if ans.get(q["key"]))


def diagnose(ans):
    score = calculate_score(ans)
    if score > FAILURE_THRESHOLD:
        return "Triptan Failure"
    return "Triptan Responder"

# ──────────────────────────────────────────────────────────────
# 4️⃣  Routes

@app.route("/", methods=["GET"])
def form():
    return render_template("index.html", questions=QUESTIONS)


@app.route("/diagnose", methods=["POST"])
def result():
    # Collect answers as booleans (yes = True, no = False)
    ans = {key: (request.form.get(key) == "yes") for key in KEYS}
    try:
        score = calculate_score(ans)
        decision = diagnose(ans)
    except Exception as e:
        return render_template(
            "index.html",
            questions=QUESTIONS,
            error=str(e)
        ), getattr(e, "code", 500)

    answers_display = [
        (
            q["text"],
            "Yes" if ans[q["key"]] else "No",
            q["score"] if ans[q["key"]] else 0,
        )
        for q in QUESTIONS
    ]
    return render_template(
        "result.html",
        decision=decision,
        score=score,
        max_score=MAX_SCORE,
        failure_threshold=FAILURE_THRESHOLD,
        answers=answers_display,
    )

# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
