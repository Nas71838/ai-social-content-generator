
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
        brand = request.form.get("brand")
        industry = request.form.get("industry")
        goal = request.form.get("goal")
        post_type = request.form.get("post_type")
        cta = request.form.get("cta")
        topic = request.form.get("topic")

        prompt = (
            f"Create a social media post for a brand named '{brand}' in the {industry} industry. "
            f"The goal is to {goal.lower()}, and the post type is '{post_type}'. "
            f"Include a call-to-action to '{cta}', and make it engaging and suitable for the platform. "
            f"The topic is: {topic}"
        )

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            result = response.choices[0].message.content.strip()

            hashtag_prompt = f"Generate 10 relevant hashtags for a social media post about: {topic} in the {industry} industry."
            tag_response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": hashtag_prompt}]
            )
            hashtags = tag_response.choices[0].message.content.strip()
        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("quick_post.html", result=result, hashtags=hashtags)

if __name__ == "__main__":
    app.run(debug=True)
