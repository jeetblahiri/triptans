import os
from flask import Flask, render_template, request

app = Flask(__name__)

# 1️⃣  List each question sentence in order
RAW_QUESTIONS = [
    "Do you have severe dizziness or depression with migraine headaches?",
    "Do you have very severe intolerable headache very often?",
    "Do you have migraine headache last for more than 4 hours more often?",
    "Do you have migraine headaches for more than 8 days a month?",
    "Do you take triptans 2 hours after onset of migraine headache more often?",
    "Do you have migraine headaches limiting your daily activities very often?",
    "Do you often take triptans more than 10 days in a month for headaches?"
]

QUESTIONS = [{"key": f"q{i}", "text": txt} for i, txt in enumerate(RAW_QUESTIONS, 1)]
KEYS      = [q["key"] for q in QUESTIONS]

# ──────────────────────────────────────────────────────────────
# 3️⃣  Decision engine – implements the provided rules

def diagnose(ans):
    # Question indices (0-based: Q1=0, Q2=1, ..., Q7=6)
    Q1, Q2, Q3, Q4, Q5, Q6, Q7 = range(7)
    drivers = {Q1, Q3, Q4, Q5, Q7}   # driver questions set

    # Normalize answers into "YES"/"NO"
    answers = ["YES" if ans.get(k) else "NO" for k in KEYS]
    total_yes = answers.count("YES")
    yes_in_drivers = sum(answers[i] == "YES" for i in drivers)

    # Rule 1 & 2
    if yes_in_drivers >= 2:
        return "High probability of Triptans Refractory"
    if yes_in_drivers == 1:
        return "High probability of Triptans Nonresponders"

    # Rule 3: If all NO
    if total_yes == 0:
        return "Probable Triptans responder"

    # Rule 4: If YES only in Q2 and/or Q6
    yes_indices = {i for i, val in enumerate(answers) if val == "YES"}
    if yes_indices.issubset({Q2, Q6}):
        return "Probable Triptans responder"

    # Fallback
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
