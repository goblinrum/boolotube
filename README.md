# boolotube

boolotube is very boolo

it is an application that allows reaction video creators to release youtube content without worrying about DMCA infringement

the way it works is:

1. the creator records their reaction to the video without including the DMCA/OG content
2. the creator uses this application to map of timestamps from the reaction video to the OG content
   - for example, let's say I record my reaction video
   - I start reacting to the video at timestamp 1:21 on my reaction video
   - I map it to 0:00 of the video I'm reacting to
3. I upload the reaction video to youtube (or any other side with video embeds) and link the corresponding project created from this app
4. when watching the video, the OG content should pop up alongside my reaction at 1:21

## API Functionality
### Models
```
project: {
  uuid: UUID
  my_reaction_url: String,
  original_video_url: String,
  createdAt: Time,
  mapped_timestamps: [Object]
}

timestamp_map: {
  uuid: UUID
  start_time_my_reaction: Integer (seconds from start)
  end_time_my_reaction: Integer,
  start_time_original: Integer,
  end_time_originak: Integer,
}
```
### Endpoints
`POST /project`
- Creates a new project. Requires the 2 videos to be present

`GET /project/:id`
- Gets the project given the ID
- Serves as the "permalink" to the project
- Returns both links, generates embeds for both
- Gets the list of matching timestamps

`POST /timestamp`
- Body:
- ```
  project_id: UUID
  start_time_my_reaction: Integer,
  end_time_my_reaction: Integer,
  start_time_original: Integer,
  end_time_originak: Integer,
  ```
- Creates a new timestamp attached to the corresponding object
- Does a few quick validations to check that the timestamps are logically correct

`GET /timestamp/:id`
- Optionally can be just a foreign key to project and the query returns all the nested data
- Gets relevant info about the timestamps

`DELETE /timestamp/:id`
- Deletes the timestamp object that holds the corresponding mapping

### Frontend

### Viewer interface
Simple 2 pane interface that contains 2 video embeds. Use something like [this](https://developers.google.com/youtube/iframe_api_reference) to determine the video playtime and play the original video given the mappings.

### Creator interface
Simple form to fill in the fields to create a new project. Once a project is created, allow the user in the current session only to add timestamps (for simplicity). Feel free to make a simple auth system to make each field editable. 
