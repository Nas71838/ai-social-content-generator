from flask import Flask, request, render_template
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        platform = request.form.get("platform")
        tone = request.form.get("tone")
        topic = request.form.get("topic")

        prompt = f"Write a {tone} social media post for {platform} about: {topic}"

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful social media assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            result = response.choices[0].message.content.strip()
        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
