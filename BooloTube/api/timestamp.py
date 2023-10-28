from rxconfig import config
from fastapi import APIRouter, HTTPException, Request
import uuid
import json
import psycopg

def connect_db():
    return psycopg.connect(config.db_url)

async def create_timestamp(req: Request):
    data=json.loads(await req.body())
    project_id=data['project_id']
    start_time_my_reaction=int(data['start_time_my_reaction'])
    end_time_my_reaction=int(data['end_time_my_reaction'])
    start_time_original=int(data['start_time_original'])
    end_time_original=int(data['end_time_original'])
    if start_time_my_reaction > end_time_my_reaction or start_time_original > end_time_original:
        raise HTTPException(status_code=400, detail="Start time cannot be after end time.")
    if (end_time_my_reaction - start_time_my_reaction) != (end_time_original - start_time_original):
        raise HTTPException(status_code=400, detail="Time difference between start and end should be the same for both reaction and original.")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT uuid 
        FROM timestamp_map 
        WHERE project_id = %s AND 
        start_time_my_reaction = %s AND 
        end_time_my_reaction = %s AND 
        start_time_original = %s AND 
        end_time_original = %s""",
        (project_id, start_time_my_reaction, end_time_my_reaction, start_time_original, end_time_original)
    )
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="This timestamp mapping already exists for the project.")

    cursor.execute(
        """SELECT start_time_my_reaction, end_time_my_reaction, start_time_original, end_time_original 
        FROM timestamp_map 
        WHERE project_id = %s""",
        (project_id,)
    )
    existing_timestamps = cursor.fetchall()
    for existing in existing_timestamps:
        if not (end_time_my_reaction <= existing[0] or start_time_my_reaction >= existing[1] or end_time_original <= existing[2] or start_time_original >= existing[3]):
            raise HTTPException(status_code=400, detail="Overlapping timestamps detected.")
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