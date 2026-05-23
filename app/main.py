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

    os.environ["CANVAS_API_TOKEN"] = session["canvas_token"]
    os.environ["CANVAS_BASE_URL"] = "https://kettering.instructure.com"
    os.environ["NOTION_TOKEN"] = session["notion_token"]
    os.environ["NOTION_DATABASE_ID"] = session["notion_database_id"]

    return redirect(url_for("dashboard"))

@app.route("/dashboard", methods=["GET"])
def dashboard():
    assignments = get_all_assignments()
    return render_template("dashboard.html", assignments=assignments)

@app.route("/sync", methods=["POST"])
def sync():
    assignments = get_all_assignments()
    sync_assignments(assignments)
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)