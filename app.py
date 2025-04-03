from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def check_url():
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            return "Please enter a URL", 400
        try:
            # Example API request (modify as needed)
            response = requests.get(f"https://some-api.com/check?url={url}")
            if response.status_code == 200:
                return response.text
            else:
                return "Error checking URL", 500
        except Exception as e:
            return f"Error: {str(e)}", 500

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

