from flask import Flask, render_template

app = Flask(__name__)

# Example API route - to start server, run "python server.py"

@app.route("/members")
def members():
    return {"members": ["Member1", "Member2"]}

@app.route("/")
def home():
    return render_template("../client/public/index.html")

if __name__ == "__main__":
    app.run(debug=True)