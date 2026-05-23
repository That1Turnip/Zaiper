import requests

def get_courses(canvas_token, canvas_base_url):
    url = f"{canvas_base_url}/api/v1/courses"
    headers = {"Authorization": f"Bearer {canvas_token}"}
    params = {"enrollment_state": "active", "per_page": 50}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def get_assignments(course_id, canvas_token, canvas_base_url):
    url = f"{canvas_base_url}/api/v1/courses/{course_id}/assignments"
    headers = {"Authorization": f"Bearer {canvas_token}"}
    params = {"per_page": 50}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def get_all_assignments(canvas_token, canvas_base_url):
    all_assignments = []
    courses = get_courses(canvas_token, canvas_base_url)
    for course in courses:
        if "name" not in course:
            continue
        try:
            assignments = get_assignments(course["id"], canvas_token, canvas_base_url)
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