from flask import Flask, render_template, request, redirect, url_for, session
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'sync'))

from canvas_client import get_all_assignments
from notion_sync import sync_assignments

app = Flask(__name__)
app.secret_key = "zaiper_secret_key"

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/setup", methods=["POST"])
def setup():
    session["canvas_token"] = request.form.get("canvas_token")
    session["notion_token"] = request.form.get("notion_token")
    session["notion_database_id"] = request.form.get("notion_database_id")
    return redirect(url_for("dashboard"))

@app.route("/dashboard", methods=["GET"])
def dashboard():
    canvas_token = session.get("canvas_token")
    notion_token = session.get("notion_token")
    notion_database_id = session.get("notion_database_id")

    if not canvas_token or not notion_token or not notion_database_id:
        return redirect(url_for("index"))

    try:
        assignments = get_all_assignments(
            canvas_token,
            "https://kettering.instructure.com"
        )
    except Exception as e:
        assignments = []
        print(f"Canvas error: {e}")

    return render_template("dashboard.html", assignments=assignments)

@app.route("/sync", methods=["POST"])
def sync():
    canvas_token = session.get("canvas_token")
    notion_token = session.get("notion_token")
    notion_database_id = session.get("notion_database_id")

    if not canvas_token or not notion_token or not notion_database_id:
        return redirect(url_for("index"))

    try:
        assignments = get_all_assignments(
            canvas_token,
            "https://kettering.instructure.com"
        )
        sync_assignments(notion_token, notion_database_id, assignments)
    except Exception as e:
        print(f"Sync error: {e}")

    return redirect(url_for("dashboard"))

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)