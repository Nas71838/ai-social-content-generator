
from flask import Flask, request, render_template
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")

@app.route("/plan", methods=["GET", "POST"])
def plan():
    ideas = []
    if request.method == "POST":
        niche = request.form.get("niche")
        tone = request.form.get("tone")

        prompt = f"Generate a 7-day social media content plan for a business in the {niche} niche. Use a {tone} tone. List one idea per day (Monday to Sunday), clearly labeled."

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            text = response.choices[0].message.content.strip()
            ideas = text.split("\n")
        except Exception as e:
            ideas = [f"Error: {str(e)}"]

    return render_template("plan.html", ideas=ideas)

@app.route("/generate_caption", methods=["POST"])
def generate_caption():
    idea = request.form.get("idea")

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Write a social media post caption for this idea: {idea}"}]
        )
        caption = response.choices[0].message.content.strip()
    except Exception as e:
        caption = f"Error: {str(e)}"

    return render_template("caption.html", idea=idea, caption=caption)

if __name__ == "__main__":
    app.run(debug=True)
