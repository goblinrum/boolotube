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
  end_time_original: Integer,
}
```
### Endpoints
`POST /project`
- Creates a new project. Requires the 2 videos to be present
- Body:
- ```
    my_reaction_url: String,
    original_video_url: String,
  ```

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
# Welcome to Reflex!

This is the base Reflex template - installed when you run `reflex init`.

If you want to use a different template, pass the `--template` flag to `reflex init`.
For example, if you want a more basic starting point, you can run:

```bash
reflex init --template blank
```

## About this Template

This template has the following directory structure:

```bash
├── README.md
├── assets
├── rxconfig.py
└── {your_app}
    ├── __init__.py
    ├── components
    │   ├── __init__.py
    │   └── sidebar.py
    ├── pages
    │   ├── __init__.py
    │   ├── dashboard.py
    │   ├── index.py
    │   └── settings.py
    ├── state.py
    ├── styles.py
    ├── templates
    │   ├── __init__.py
    │   └── template.py
    └── {your_app}.py
```

See the [Project Structure docs](https://reflex.dev/docs/getting-started/project-structure/) for more information on general Reflex project structure.

### Adding Pages

In this template, the pages in your app are defined in `{your_app}/pages/`.
Each page is a function that returns a Reflex component.
For example, to edit this page you can modify `{your_app}/pages/index.py`.
See the [pages docs](https://reflex.dev/docs/components/pages/) for more information on pages.

In this template, instead of using `rx.add_page` or the `@rx.page` decorator,
we use the `@template` decorator from `{your_app}/templates/template.py`.

To add a new page:

1. Add a new file in `{your_app}/pages/`. We recommend using one file per page, but you can also group pages in a single file.
2. Add a new function with the `@template` decorator, which takes the same arguments as `@rx.page`.
3. Import the page in your `{your_app}/pages/__init__.py` file and it will automatically be added to the app.


### Adding Components

In order to keep your code organized, we recommend putting components that are
used across multiple pages in the `{your_app}/components/` directory.

In this template, we have a sidebar component in `{your_app}/components/sidebar.py`.

### Adding State

In this template, we define the base state of the app in `{your_app}/state.py`.
The base state is useful for general app state that is used across multiple pages.

In this template, the base state handles the toggle for the sidebar.

As your app grows, we recommend using [substates](https://reflex.dev/docs/state/substates/)
to organize your state. You can either define substates in their own files, or if the state is
specific to a page, you can define it in the page file itself.
