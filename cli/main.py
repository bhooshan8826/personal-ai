"""
Personal AI Assistant CLI
"""
import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import requests
import json

app = typer.Typer(help="Personal AI Assistant CLI")
console = Console()

# API Configuration
API_BASE_URL = "http://localhost:8000"

def api_request(method: str, endpoint: str, json_data: dict = None, params: dict = None):
    """Make API request"""
    url = f"{API_BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}

    try:
        if method == "GET":
            response = requests.get(url, params=params, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=json_data, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=json_data, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)

        response.raise_for_status()
        return response.json() if response.text else {}
    except requests.exceptions.ConnectionError:
        console.print("[red]Error: Cannot connect to API. Is the backend running?[/red]")
        raise typer.Exit(1)
    except requests.exceptions.HTTPError as e:
        console.print(f"[red]Error: {e.response.status_code} - {e.response.text}[/red]")
        raise typer.Exit(1)


@app.command()
def chat(message: str, conversation_id: Optional[str] = None):
    """Chat with the AI assistant"""
    with console.status("Thinking..."):
        result = api_request(
            "POST",
            "/api/v1/chat",
            json_data={"message": message, "conversation_id": conversation_id}
        )

    console.print(f"\n[cyan]Intent:[/cyan] {result.get('intent', 'unknown')}")
    console.print(f"\n[green]Response:[/green]\n{result.get('response', 'No response')}\n")


@app.command()
def task_create(title: str, description: Optional[str] = None, priority: str = "medium"):
    """Create a new task"""
    with console.status("Creating task..."):
        result = api_request(
            "POST",
            "/api/v1/tasks",
            json_data={"title": title, "description": description, "priority": priority}
        )

    console.print(f"[green]✓ Task created![/green]\n")
    console.print(f"  ID: {result.get('id')}")
    console.print(f"  Title: {result.get('title')}")
    console.print(f"  Priority: {result.get('priority')}\n")


@app.command()
def task_list(status: Optional[str] = None):
    """List tasks"""
    with console.status("Loading tasks..."):
        result = api_request(
            "GET",
            "/api/v1/tasks",
            params={"status": status} if status else None
        )

    tasks = result.get("tasks", [])

    if not tasks:
        console.print("[yellow]No tasks found.[/yellow]")
        return

    table = Table(title="Your Tasks")
    table.add_column("ID", style="cyan", width=8)
    table.add_column("Title", style="white")
    table.add_column("Priority", style="yellow")
    table.add_column("Status", style="green")

    for task in tasks:
        table.add_row(
            task["id"][:8],
            task["title"],
            task["priority"],
            task["status"]
        )

    console.print(table)


@app.command()
def task_complete(task_id: str):
    """Mark a task as complete"""
    with console.status("Completing task..."):
        result = api_request(
            "PUT",
            f"/api/v1/tasks/{task_id}/complete"
        )

    console.print(f"[green]✓ Task completed![/green]\n")


@app.command()
def note_create(content: str, title: Optional[str] = None, tags: Optional[str] = None):
    """Create a new note"""
    tag_list = tags.split(",") if tags else []

    with console.status("Creating note..."):
        result = api_request(
            "POST",
            "/api/v1/notes",
            json_data={"title": title, "content": content, "tags": tag_list}
        )

    console.print(f"[green]✓ Note created![/green]\n")
    console.print(f"  ID: {result.get('id')}")
    if title:
        console.print(f"  Title: {result.get('title')}")
    console.print(f"  Tags: {', '.join(result.get('tags', []))}\n")


@app.command()
def note_list():
    """List notes"""
    with console.status("Loading notes..."):
        result = api_request(
            "GET",
            "/api/v1/notes"
        )

    notes = result.get("notes", [])

    if not notes:
        console.print("[yellow]No notes found.[/yellow]")
        return

    for note in notes[:10]:  # Show first 10
        title = note.get("title") or "Untitled"
        console.print(f"\n[cyan]{title}[/cyan]")
        console.print(f"  {note['content'][:100]}...")
        if note.get("tags"):
            console.print(f"  Tags: {', '.join(note['tags'])}")


@app.command()
def reminder_create(task_id: str, when: str):
    """Create a reminder"""
    # Parse when string (simplified)
    from datetime import datetime, timedelta

    if when == "tomorrow":
        trigger_time = (datetime.now() + timedelta(days=1)).isoformat()
    else:
        trigger_time = when

    with console.status("Creating reminder..."):
        result = api_request(
            "POST",
            "/api/v1/reminders",
            json_data={"task_id": task_id, "next_trigger": trigger_time}
        )

    console.print(f"[green]✓ Reminder set![/green]\n")
    console.print(f"  Task ID: {result.get('task_id')}")
    console.print(f"  Trigger: {result.get('next_trigger')}\n")


@app.command()
def reminder_list():
    """List reminders"""
    with console.status("Loading reminders..."):
        result = api_request(
            "GET",
            "/api/v1/reminders"
        )

    reminders = result.get("reminders", [])

    if not reminders:
        console.print("[yellow]No reminders found.[/yellow]")
        return

    table = Table(title="Upcoming Reminders")
    table.add_column("ID", style="cyan", width=8)
    table.add_column("Task ID", style="white", width=8)
    table.add_column("Trigger", style="yellow")
    table.add_column("Active", style="green")

    for reminder in reminders:
        table.add_row(
            reminder["id"][:8],
            reminder["task_id"][:8],
            reminder["next_trigger"][:10],
            "Yes" if reminder["is_active"] else "No"
        )

    console.print(table)


@app.command()
def health():
    """Check API health"""
    try:
        result = api_request("GET", "/api/v1/health")
        console.print(f"[green]✓ API is healthy[/green]")
        console.print(f"  Status: {result.get('status')}")
        console.print(f"  Version: {result.get('version')}")
    except:
        console.print("[red]✗ API is not responding[/red]")


@app.callback()
def main():
    """Personal AI Assistant CLI Tool"""
    pass


if __name__ == "__main__":
    app()
