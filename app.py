
from flask import Flask, request, render_template
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
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
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that writes engaging and effective social media content."},
                    {"role": "user", "content": prompt}
                ]
            )
            result = response.choices[0].message.content.strip()

            if include_hashtags:
                hashtag_prompt = f"Generate 10 relevant and trending hashtags for a post about: {topic}"
                tag_response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": hashtag_prompt}
                    ]
                )
                hashtags = tag_response.choices[0].message.content.strip()
        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("index.html", result=result, hashtags=hashtags)

if __name__ == "__main__":
    app.run(debug=True)
