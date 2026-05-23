import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

notion = Client(auth=NOTION_TOKEN)

def get_existing_assignments():
    results = notion.databases.query(NOTION_DATABASE_ID)
    existing = set()
    for page in results["results"]:
        props = page["properties"]
        name = props.get("Assignment Name", {}).get("title", [])
        if name:
            existing.add(name[0]["text"]["content"])
    return existing

def add_assignment(assignment_name, course_name, due_date, status):
    properties = {
        "Assignment Name": {
            "title": [{"text": {"content": assignment_name}}]
        },
        "Course": {
            "rich_text": [{"text": {"content": course_name}}]
        },
        "Status": {
            "select": {"name": status}
        }
    }
    if due_date:
        properties["Due Date"] = {
            "date": {"start": due_date}
        }
    notion.pages.create(
        parent={"database_id": NOTION_DATABASE_ID},
        properties=properties
    )

def sync_assignments(assignments):
    existing = get_existing_assignments()
    new_count = 0
    for a in assignments:
        if a["assignment_name"] not in existing:
            add_assignment(
                a["assignment_name"],
                a["course_name"],
                a["due_date"],
                a["status"]
            )
            new_count += 1
            print(f"Added: {a['assignment_name']}")
        else:
            print(f"Skipped (already exists): {a['assignment_name']}")
    print(f"Sync complete — {new_count} new assignments added.")