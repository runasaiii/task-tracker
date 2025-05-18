from flask import Blueprint, request, jsonify, abort
from .models import Task
from . import db
from datetime import datetime

task_bp = Blueprint('tasks', __name__)

def parse_date(date_str):
    if date_str:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            abort(400, description="Неверный формат даты, используйте YYYY-MM-DD")
    return None

@task_bp.route("/", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@task_bp.route("/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict())

@task_bp.route("/", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data.get("title"):
        abort(400, description="Поле 'title' обязательно")
    
    due_date = None
    if data.get("due_date"):
        try:
            due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()
        except ValueError:
            abort(400, description="Неверный формат даты. Используй YYYY-MM-DD")
    
    task = Task(
        title=data["title"],
        description=data.get("description"),
        due_date=due_date,
        status=data.get("status", "pending")
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@task_bp.route("/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()

    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    
    if "due_date" in data:
        if data["due_date"]:
            try:
                task.due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()
            except ValueError:
                abort(400, description="Неверный формат даты. Используй YYYY-MM-DD")
        else:
            task.due_date = None
    
    task.status = data.get("status", task.status)

    db.session.commit()
    return jsonify(task.to_dict())

@task_bp.route("/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Задача удалена"})
