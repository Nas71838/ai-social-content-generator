
from flask import Flask, request, render_template
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")

@app.route("/quick_post", methods=["GET", "POST"])
def quick_post():
    result = ""
    hashtags = ""
    if request.method == "POST":
        topic = request.form.get("topic")
        prompt = f"Write a great social media post about: {topic}"
        response = openai.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
        result = response.choices[0].message.content.strip()

        hashtag_prompt = f"Generate 10 relevant hashtags for a post about: {topic}"
        tag_response = openai.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": hashtag_prompt}])
        hashtags = tag_response.choices[0].message.content.strip()

    return render_template("quick_post.html", result=result, hashtags=hashtags)

@app.route("/plan", methods=["GET", "POST"])
def plan():
    ideas = []
    if request.method == "POST":
        niche = request.form.get("niche")
        prompt = f"Give me a 7-day content plan for a {niche} brand."
        response = openai.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
        text = response.choices[0].message.content.strip()
        ideas = text.split("\n")
    return render_template("plan.html", ideas=ideas)

@app.route("/calendar", methods=["GET", "POST"])
def calendar():
    ideas = []
    if request.method == "POST":
        niche = request.form.get("niche")
        prompt = f"Create a 30-day content calendar for a {niche} business. Label each day."
        response = openai.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
        text = response.choices[0].message.content.strip()
        ideas = text.split("\n")
    return render_template("calendar.html", ideas=ideas)

@app.route("/bio", methods=["GET", "POST"])
def bio():
    result = ""
    if request.method == "POST":
        profession = request.form.get("profession")
        prompt = f"Create a professional and catchy social media bio for a {profession}"
        response = openai.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
        result = response.choices[0].message.content.strip()
    return render_template("bio.html", result=result)

@app.route("/hashtags", methods=["GET", "POST"])
def hashtags():
    result = ""
    if request.method == "POST":
        topic = request.form.get("topic")
        prompt = f"Generate 15 hashtags for: {topic}"
        response = openai.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
        result = response.choices[0].message.content.strip()
    return render_template("hashtags.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
