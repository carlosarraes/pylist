from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")

last_id = 0
tasks = []


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/tasks")
async def get_tasks(request: Request):
    return templates.TemplateResponse(
        "components/tasks.html", {"request": request, "tasks": tasks}
    )


@app.post("/tasks")
async def add_task(request: Request):
    global last_id
    form_data = await request.form()
    print(form_data)
    task = form_data["task"]
    last_id += 1
    tasks.append({"id": last_id, "task": task, "status": False})

    print(tasks[-1])
    return templates.TemplateResponse(
        "components/task.html", {"request": request, "task": tasks[-1]}
    )


@app.delete("/tasks/{task_id}")
async def delete_task(request: Request, task_id: int):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]

    return templates.TemplateResponse(
        "components/deleted_task.html", {"request": request, "tasks": tasks}
    )
