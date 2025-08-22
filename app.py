import os
from flask import Flask, render_template, request

app = Flask(__name__)

# 1️⃣  List each question sentence in order
RAW_QUESTIONS = [
    "Do you have frequent hyperacidity problem or vomiting or loose motions?",
    "Do you have very severe migraine very often?",
    "Does your migraine headache last for more than 4 hrs more often?",
    "Do you have migraine headaches more than 8 days a month?",
    "Do you take triptans 2 hrs after onset of migraine headache more often?",
    "Are your migraine headaches limit your daily activities very often?",
    "Do you often take triptans more than 10 days in a month for headaches?"
]

QUESTIONS = [{"key": f"q{i}", "text": txt} for i, txt in enumerate(RAW_QUESTIONS, 1)]
KEYS      = [q["key"] for q in QUESTIONS]

# ──────────────────────────────────────────────────────────────
# 3️⃣  Decision engine – implements the provided rules

def diagnose(ans):
    # Normalize answers into YES/NO strings
    answers = ["YES" if ans[k] else "NO" for k in KEYS]
    yes_count = answers.count("YES")

    # Rule 1: If Q5 or Q7 is YES → High probability of Triptans Nonresponder
    if answers[4] == "YES" or answers[6] == "YES":
        return "High probability of Triptans Nonresponder"

    # Rule 2: If 2 or more YES → High probability of Triptans Nonresponder
    if yes_count >= 2:
        return "High probability of Triptans Nonresponder"

    # Rule 3 & 4: If 0 or 1 YES → Probable Triptans responder
    return "Probable Triptans responder"

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
        decision = diagnose(ans)
    except Exception as e:
        return render_template(
            "index.html",
            questions=QUESTIONS,
            error=str(e)
        ), getattr(e, "code", 500)

    answers_display = [(q["text"], "Yes" if ans[q["key"]] else "No") for q in QUESTIONS]
    return render_template("result.html", decision=decision, answers=answers_display)

# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
