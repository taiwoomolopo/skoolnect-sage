from app.prompts.teacher_mode import TEACHER_MODE
from app.prompts.parent_mode import PARENT_MODE

def get_role_prompt(role):
    if role == "teacher":
        return TEACHER_MODE
    elif role == "parent":
        return PARENT_MODE
    else:
        return ""