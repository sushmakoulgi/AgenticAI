def validate_task(task:str):
    if task is None or task.strip()=="":
        raise ValueError("Input is empty")
    task=task.strip()
    if len(task) > 5000:
        raise ValueError("Input is too Long")

    return task
