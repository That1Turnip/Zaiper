import requests
import os
from dotenv import load_dotenv

load_dotenv()

CANVAS_API_TOKEN = os.getenv("CANVAS_API_TOKEN")
CANVAS_BASE_URL = os.getenv("CANVAS_BASE_URL")

headers = {
    "Authorization": f"Bearer {CANVAS_API_TOKEN}"
}

def get_courses():
    url = f"{CANVAS_BASE_URL}/api/v1/courses"
    params = {"enrollment_state": "active", "per_page": 50}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def get_assignments(course_id):
    url = f"{CANVAS_BASE_URL}/api/v1/courses/{course_id}/assignments"
    params = {"per_page": 50}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def get_all_assignments():
    all_assignments = []
    courses = get_courses()
    for course in courses:
        if "name" not in course:
            continue
        try:
            assignments = get_assignments(course["id"])
            for assignment in assignments:
                all_assignments.append({
                    "course_name": course["name"],
                    "assignment_name": assignment.get("name", "Unnamed"),
                    "due_date": assignment.get("due_at", None),
                    "status": "Not Submitted"
                })
        except Exception as e:
            print(f"Skipping course {course['id']}: {e}")
    return all_assignments