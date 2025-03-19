# coding_utils/analyst.py
import ast
import re
from typing import Any, Dict, List, Optional
from collections import defaultdict

def create_file_handler(env, filename: str, content: str, subdir: Optional[str] = None) -> Dict[str, Any]:
    try:
        file_path = env._get_file_path(filename, subdir)
        with open(file_path, 'w') as f:
            f.write(content)
        return {
            "success": True,
            "message": f"File created successfully: {file_path}",
            "file_path": file_path
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def analyze_task_handler(env, task_description: str) -> Dict[str, Any]:
    try:
        keywords = {
            'implementation': ['implement', 'create', 'develop', 'build', 'code'],
            'testing': ['test', 'verify', 'validate', 'check', 'assert'],
            'optimization': ['optimize', 'improve', 'enhance', 'speed up', 'efficient'],
            'debugging': ['debug', 'fix', 'resolve', 'error', 'issue'],
            'documentation': ['document', 'explain', 'describe', 'comment', 'clarify']
        }
        
        task_lower = task_description.lower()
        task_aspects = defaultdict(int)
        
        for aspect, words in keywords.items():
            for word in words:
                task_aspects[aspect] += len(re.findall(r'\b' + word + r'\b', task_lower))
                
        complexity_score = sum(task_aspects.values()) / len(keywords)
        
        return {
            "success": True,
            "task_aspects": dict(task_aspects),
            "complexity_score": complexity_score,
            "primary_focus": max(task_aspects.items(), key=lambda x: x[1])[0]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def assign_roles_handler(env, task_analysis: Dict[str, Any], available_roles: List[str]) -> Dict[str, Any]:
    try:
        task_aspects = task_analysis.get("task_aspects", {})
        primary_focus = task_analysis.get("primary_focus", "")
        
        role_priorities = {
            'implementation': ['developer', 'architect', 'reviewer'],
            'testing': ['tester', 'qa_engineer', 'developer'],
            'optimization': ['performance_engineer', 'developer', 'architect'],
            'debugging': ['debugger', 'developer', 'tester'],
            'documentation': ['technical_writer', 'developer', 'reviewer']
        }
        
        assigned_roles = []
        if primary_focus in role_priorities:
            for role in role_priorities[primary_focus]:
                if role in available_roles and role not in assigned_roles:
                    assigned_roles.append(role)
                    
        remaining_roles = [r for r in available_roles if r not in assigned_roles]
        assigned_roles.extend(remaining_roles)
        
        return {
            "success": True,
            "assigned_roles": assigned_roles,
            "role_priorities": {
                aspect: roles for aspect, roles in role_priorities.items()
                if aspect in task_aspects and task_aspects[aspect] > 0
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def decompose_task_handler(env, task_description: str, assigned_roles: List[str]) -> Dict[str, Any]:
    try:
        subtasks = []
        role_tasks = defaultdict(list)
        
        task_lines = [line.strip() for line in task_description.split('\n') if line.strip()]
        current_subtask = []
        
        for line in task_lines:
            if line.startswith(('#', '-', '*')) or len(current_subtask) >= 3:
                if current_subtask:
                    subtasks.append(' '.join(current_subtask))
                current_subtask = [line.lstrip('#-* ')]
            else:
                current_subtask.append(line)
                
        if current_subtask:
            subtasks.append(' '.join(current_subtask))
            
        for i, subtask in enumerate(subtasks):
            role_index = i % len(assigned_roles)
            role = assigned_roles[role_index]
            role_tasks[role].append({
                "subtask_id": i + 1,
                "description": subtask,
                "status": "pending"
            })
            
        return {
            "success": True,
            "subtasks": subtasks,
            "role_assignments": dict(role_tasks),
            "total_subtasks": len(subtasks)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def track_progress_handler(env, task_decomposition: Dict[str, Any], completed_subtasks: List[int]) -> Dict[str, Any]:
    try:
        total_subtasks = task_decomposition.get("total_subtasks", 0)
        role_assignments = task_decomposition.get("role_assignments", {})
        
        progress_by_role = {}
        for role, tasks in role_assignments.items():
            role_completed = sum(1 for task in tasks if task["subtask_id"] in completed_subtasks)
            progress_by_role[role] = {
                "completed": role_completed,
                "total": len(tasks),
                "percentage": (role_completed / len(tasks)) * 100 if tasks else 0
            }
            
        overall_progress = {
            "completed_subtasks": len(completed_subtasks),
            "total_subtasks": total_subtasks,
            "completion_percentage": (len(completed_subtasks) / total_subtasks * 100) if total_subtasks else 0
        }
        
        return {
            "success": True,
            "progress_by_role": progress_by_role,
            "overall_progress": overall_progress,
            "remaining_subtasks": total_subtasks - len(completed_subtasks)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def register_analyst_actions(env):
    env.register_action(
        "create_file",
        handler=lambda **kwargs: create_file_handler(env, **kwargs),
        description={
            "type": "function",
            "function": {
                "name": "create_file",
                "description": "Creates a new file in the workspace with specified content",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filename": {"type": "string", "description": "Name of the file to create"},
                        "content": {"type": "string", "description": "Content to write to the file"},
                        "subdir": {"type": "string", "description": "Optional subdirectory within workspace"}
                    },
                    "required": ["filename", "content"]
                }
            }
        }
    )

    env.register_action(
        "analyze_task",
        handler=lambda **kwargs: analyze_task_handler(env, **kwargs),
        description={
            "type": "function",
            "function": {
                "name": "analyze_task",
                "description": "Analyzes task description to identify key aspects and complexity",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_description": {
                            "type": "string",
                            "description": "Description of the task to analyze"
                        }
                    },
                    "required": ["task_description"]
                }
            }
        }
    )

    env.register_action(
        "assign_roles",
        handler=lambda **kwargs: assign_roles_handler(env, **kwargs),
        description={
            "type": "function",
            "function": {
                "name": "assign_roles",
                "description": "Assigns roles based on task analysis",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_analysis": {
                            "type": "object",
                            "description": "Analysis result from analyze_task"
                        },
                        "available_roles": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of available roles"
                        }
                    },
                    "required": ["task_analysis", "available_roles"]
                }
            }
        }
    )

    env.register_action(
        "decompose_task",
        handler=lambda **kwargs: decompose_task_handler(env, **kwargs),
        description={
            "type": "function",
            "function": {
                "name": "decompose_task",
                "description": "Breaks down task into subtasks and assigns to roles",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_description": {
                            "type": "string",
                            "description": "Description of the task to decompose"
                        },
                        "assigned_roles": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of assigned roles"
                        }
                    },
                    "required": ["task_description", "assigned_roles"]
                }
            }
        }
    )

    env.register_action(
        "track_progress",
        handler=lambda **kwargs: track_progress_handler(env, **kwargs),
        description={
            "type": "function",
            "function": {
                "name": "track_progress",
                "description": "Tracks progress of task completion by role",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_decomposition": {
                            "type": "object",
                            "description": "Task decomposition result"
                        },
                        "completed_subtasks": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "description": "List of completed subtask IDs"
                        }
                    },
                    "required": ["task_decomposition", "completed_subtasks"]
                }
            }
        }
    )