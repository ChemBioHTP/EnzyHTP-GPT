from flask import Flask

app = Flask(__name__)

# Example API route - to start server, run "python server.py"

@app.route("/members")
def members():
    return {"members": ["Member1", "Member2"]}

if __name__ == "__main__":
    app.run(debug=True)