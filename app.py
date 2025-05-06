
from flask import Flask, request, render_template
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

def generate_response(prompt):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def generator_route(page_name):
    def route_func():
        result = ""
        if request.method == "POST":
            brand = request.form.get("brand")
            industry = request.form.get("industry")
            topic = request.form.get("topic")
            prompt = f"Generate {page_name.replace('_', ' ')} content for brand '{brand}' in the {industry} industry about: {topic}"
            result = generate_response(prompt)
        return render_template(f"{page_name}.html", result=result)
    return route_func

pages = ["quick_post", "plan", "calendar", "bio", "hashtags", "hook", "series", "trend"]

for page in pages:
    app.add_url_rule(f"/{page}", page, generator_route(page), methods=["GET", "POST"])

if __name__ == "__main__":
    app.run(debug=True)
