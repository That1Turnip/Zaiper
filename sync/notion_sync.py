from notion_client import Client

def get_existing_assignments(notion_token, notion_database_id):
    notion = Client(auth=notion_token)
    results = notion.databases.query(notion_database_id)
    existing = set()
    for page in results["results"]:
        props = page["properties"]
        name = props.get("Assignment Name", {}).get("title", [])
        if name:
            existing.add(name[0]["text"]["content"])
    return existing

def add_assignment(notion_token, notion_database_id, assignment_name, course_name, due_date, status):
    notion = Client(auth=notion_token)
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
        parent={"database_id": notion_database_id},
        properties=properties
    )

def sync_assignments(notion_token, notion_database_id, assignments):
    existing = get_existing_assignments(notion_token, notion_database_id)
    new_count = 0
    for a in assignments:
        if a["assignment_name"] not in existing:
            add_assignment(
                notion_token,
                notion_database_id,
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