from rxconfig import config
from fastapi import APIRouter, HTTPException, Request
import uuid
import json
import psycopg

def connect_db():
    return psycopg.connect(config.db_url)

async def create_project(req: Request):
    data=json.loads(await req.body())
    my_reaction_url=data['my_reaction_url']
    original_video_url=data['original_video_url'] 
    if not all([my_reaction_url, original_video_url]):
        raise HTTPException(status_code=400, detail="Both reaction and original video URLs are required.")
    if my_reaction_url==original_video_url:
        raise HTTPException(status_code=400, detail="Reaction and original video URLs can't be the same.")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT uuid, my_reaction_url, original_video_url, createdAt FROM projects WHERE my_reaction_url=%s AND original_video_url=%s", (my_reaction_url, original_video_url,))
    project = cursor.fetchone()
    if project:
        raise HTTPException(status_code=400, detail="Project with my_reaction_url and original_video_url already exists.")
    cursor.execute("SELECT uuid, my_reaction_url, original_video_url, createdAt FROM projects WHERE my_reaction_url=%s AND original_video_url=%s", (original_video_url, my_reaction_url,))
    project = cursor.fetchone()
    if project:
        raise HTTPException(status_code=400, detail="Project with my_reaction_url and original_video_url already exists.")
    project_id = str(uuid.uuid4())
    cursor.execute("INSERT INTO projects (uuid, my_reaction_url, original_video_url) VALUES (%s, %s, %s)", (project_id, my_reaction_url, original_video_url))
    conn.commit()
    conn.close()

    return {"message": "Project created successfully", "project_id": project_id}

def get_project(id: str):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT uuid, my_reaction_url, original_video_url, createdAt FROM projects WHERE uuid=%s", (id,))
    project = cursor.fetchone()

    if project:
        return {
            "uuid": project[0],
            "my_reaction_url": project[1],
            "original_video_url": project[2],
            "createdAt": project[3]
        }
    else:
        raise HTTPException(status_code=404, detail="Project not found.")

project_router = APIRouter()
project_router.add_api_route("/project", create_project, methods=["POST"])
project_router.add_api_route("/project/{id}", get_project, methods=["GET"])