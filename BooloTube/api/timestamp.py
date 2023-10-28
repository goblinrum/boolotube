from fastapi import APIRouter, HTTPException, Request
import sqlite3
import uuid
import json
import psycopg

DB_URL = "postgresql://rainbwshep:0UQ7NEw-2djpNiRL2frQFw@boolo1-3695.g95.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full"

def connect_db():
    return psycopg.connect(DB_URL)

    # return sqlite3.connect("boolotube.db")

async def create_timestamp(req: Request):
    data=json.loads(await req.body())
    project_id=data['project_id']
    start_time_my_reaction=data['start_time_my_reaction']
    end_time_my_reaction=data['end_time_my_reaction']
    start_time_original=data['start_time_original']
    end_time_original=data['end_time_original']
    if start_time_my_reaction > end_time_my_reaction or start_time_original > end_time_original:
        raise HTTPException(status_code=400, detail="Start time cannot be after end time.")

    conn = connect_db()
    cursor = conn.cursor()
    timestamp_id = str(uuid.uuid4())
    cursor.execute(
        """INSERT INTO timestamp_map 
        (uuid, project_id, start_time_my_reaction, end_time_my_reaction, start_time_original, end_time_original) 
        VALUES (%s, %s, %s, %s, %s, %s)""",
        (timestamp_id, project_id, start_time_my_reaction, end_time_my_reaction, start_time_original, end_time_original)
    )
    conn.commit()
    conn.close()

    return {"message": "Timestamp created successfully", "timestamp_id": timestamp_id}

def get_timestamp(id: str):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""SELECT uuid, project_id, start_time_my_reaction, end_time_my_reaction, start_time_original, end_time_original 
                      FROM timestamp_map WHERE uuid=%s""", (id,))
    timestamp = cursor.fetchone()

    if timestamp:
        return {
            "uuid": timestamp[0],
            "project_id": timestamp[1],
            "start_time_my_reaction": timestamp[2],
            "end_time_my_reaction": timestamp[3],
            "start_time_original": timestamp[4],
            "end_time_original": timestamp[5]
        }
    else:
        raise HTTPException(status_code=404, detail="Timestamp not found.")

def delete_timestamp(id: str):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM timestamp_map WHERE uuid=%s", (id,))
    conn.commit()
    deleted_count = cursor.rowcount
    conn.close()

    if deleted_count:
        return {"message": "Timestamp deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Timestamp not found.")

timestamp_router = APIRouter()
timestamp_router.add_api_route("/timestamp", create_timestamp, methods=["POST"])
timestamp_router.add_api_route("/timestamp/{id}", get_timestamp, methods=["GET"])
timestamp_router.add_api_route("/timestamp/{id}", delete_timestamp, methods=["DELETE"])