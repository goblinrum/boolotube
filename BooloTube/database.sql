-- -- Initialize the projects table
-- CREATE TABLE IF NOT EXISTS projects (
--     uuid TEXT PRIMARY KEY,
--     my_reaction_url TEXT NOT NULL,
--     original_video_url TEXT NOT NULL,
--     createdAt DATETIME DEFAULT CURRENT_TIMESTAMP
-- );

-- -- Initialize the timestamps table
-- CREATE TABLE IF NOT EXISTS timestamp_map (
--     uuid TEXT PRIMARY KEY,
--     project_id TEXT,
--     start_time_my_reaction INTEGER,
--     end_time_my_reaction INTEGER,
--     start_time_original INTEGER,
--     end_time_original INTEGER,
--     FOREIGN KEY(project_id) REFERENCES projects(uuid)
-- );


-- Postgres Command
-- Initialize the projects table
CREATE TABLE IF NOT EXISTS projects (
    uuid TEXT PRIMARY KEY,
    my_reaction_url TEXT NOT NULL,
    original_video_url TEXT NOT NULL,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Initialize the timestamps table
CREATE TABLE IF NOT EXISTS timestamp_map (
    uuid TEXT PRIMARY KEY,
    project_id TEXT,
    start_time_my_reaction INTEGER,
    end_time_my_reaction INTEGER,
    start_time_original INTEGER,
    end_time_original INTEGER,
    FOREIGN KEY(project_id) REFERENCES projects(uuid)
);