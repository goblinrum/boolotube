from fastapi import APIRouter, HTTPException, Request
import sqlite3
import uuid
import json
import psycopg

DB_URL = "postgresql://rainbwshep:0UQ7NEw-2djpNiRL2frQFw@boolo1-3695.g95.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full"

def connect_db():
    # return sqlite3.connect("boolotube.db")
    return psycopg.connect(DB_URL)

async def create_project(req: Request):
    data=json.loads(await req.body())
    my_reaction_url=data['my_reaction_url']
    original_video_url=data['original_video_url']
    if not all([my_reaction_url, original_video_url]):
        raise HTTPException(status_code=400, detail="Both reaction and original video URLs are required.")

    conn = connect_db()
    cursor = conn.cursor()
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