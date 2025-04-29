from flask import Flask, request, render_template
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def dashboard():
    return render_template("dashboard.html")

@app.route("/quick_post", methods=["GET", "POST"])
def quick_post():
    result = ""
    hashtags = ""
    if request.method == "POST":
        platform = request.form.get("platform")
        tone = request.form.get("tone")
        goal = request.form.get("goal")
        topic = request.form.get("topic")
        include_hashtags = request.form.get("include_hashtags")

        prompt = f"Write a {tone} social media post for {platform} with the goal to {goal}. Topic: {topic}"

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            result = response.choices[0].message.content.strip()

            if include_hashtags:
                hashtag_prompt = f"Generate 10 relevant hashtags for a post about: {topic}"
                tag_response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": hashtag_prompt}]
                )
                hashtags = tag_response.choices[0].message.content.strip()
        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("quick_post.html", result=result, hashtags=hashtags)

@app.route("/plan", methods=["GET", "POST"])
def plan():
    ideas = []
    if request.method == "POST":
        niche = request.form.get("niche")
        tone = request.form.get("tone")

        prompt = f"Generate a 7-day social media content plan for a business in the {niche} niche. Use a {tone} tone. Label each day from Monday to Sunday."

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            text = response.choices[0].message.content.strip()
            ideas = text.split("\\n")
        except Exception as e:
            ideas = [f"Error: {str(e)}"]

    return render_template("plan.html", ideas=ideas)

@app.route("/calendar", methods=["GET", "POST"])
def calendar():
    ideas = []
    if request.method == "POST":
        niche = request.form.get("niche")
        tone = request.form.get("tone")

        prompt = f"Generate a 30-day social media content plan for a business in the {niche} niche. Use a {tone} tone. List one idea per day, clearly labeled Day 1 to Day 30."

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            text = response.choices[0].message.content.strip()
            ideas = text.split("\\n")
        except Exception as e:
            ideas = [f"Error: {str(e)}"]

    return render_template("calendar.html", ideas=ideas)

@app.route("/bio", methods=["GET", "POST"])
def bio():
    result = ""
    if request.method == "POST":
        profession = request.form.get("profession")

        prompt = f"Write a professional and catchy social media bio for a {profession}. Keep it concise, engaging, and suitable for Instagram, LinkedIn, or TikTok."

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            result = response.choices[0].message.content.strip()
        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("bio.html", result=result)

@app.route("/hashtags", methods=["GET", "POST"])
def hashtags():
    result = ""
    if request.method == "POST":
        topic = request.form.get("topic")

        prompt = f"Generate 15 trending and relevant hashtags for a social media post about: {topic}"

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            result = response.choices[0].message.content.strip()
        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("hashtags.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
