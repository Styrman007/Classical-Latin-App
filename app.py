from flask import Flask, render_template, request, session, redirect
import random
from latin_1st_declension_a import words

app = Flask(__name__)
app.secret_key = "super-secret-key"  # needed for session

@app.route("/", methods=["GET", "POST"])
def quiz():
    # First-time setup: session variables
    if "score" not in session:
        session["score"] = 0
        session["streaks"] = {w["English"]: 0 for w in words}
        session["locked"] = {}

    streaks = session["streaks"]
    locked = session["locked"]

    # Decrease lock counters
    for key in list(locked.keys()):
        locked[key] -= 1
        if locked[key] <= 0:
            del locked[key]

    # Handle POST (user clicked an answer)
    result = None
    if request.method == "POST":
        user_answer = request.form["answer"]
        correct = request.form["correct"]
        english = request.form["english"]
        
        if user_answer == correct:
            result = "✅ Õige vastus!"
            session["score"] += 1
            streaks[english] += 1
            if streaks[english] >= 3:
                locked[english] = 50
                streaks[english] = 0
                result += f" Sõna '{english}' lukustatud 50 küsimuseks."
        else:
            result = f"❌ Vale. Õige oli: {correct}"
            streaks[english] = 0

        session["streaks"] = streaks
        session["locked"] = locked

    # Get available words
    available_words = [w for w in words if w["English"] not in locked]
    if not available_words:
        return "Kõik sõnad on lukus! Proovi hiljem uuesti."

    # Pick question
    chosen = random.choice(available_words)
    english = chosen["English"]
    correct_latin = chosen["Latin"]
    wrong_choices = [w["Latin"] for w in words if w["Latin"] != correct_latin]
    options = random.sample(wrong_choices, 3) + [correct_latin]
    random.shuffle(options)

    return render_template("quiz.html",
                           english=english,
                           options=options,
                           correct=correct_latin,
                           result=result,
                           score=session["score"])
