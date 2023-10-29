import httpx
import reflex as rx
from BooloTube.templates import template
from BooloTube.state import State
import json
from typing import Optional, Dict, Any
import httpx
from fastapi import Request


class ViewerState(State):

    project: Dict[str, Any] = {}
    my_reaction_url = ""
    original_video_url = ""

    stored_project_id = rx.LocalStorage(name="project_id")
    stored_my_reaction_url = rx.LocalStorage(name="my_reaction_url")
    stored_original_video_url = rx.LocalStorage(name="original_video_url")

    @rx.background
    async def fetch_project(self):
        rx.clear_local_storage()
        project_id = self.project_id
        print("project_id", project_id)
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://localhost:8000/project/{project_id}")
            if response.status_code == 200:
                async with self:
                    self.project = response.json()
                    self.my_reaction_url = self.project['my_reaction_url'].replace(
                        "www.", "")
                    self.original_video_url = self.project['original_video_url'].replace(
                        "www.", "")
                    self.stored_project_id = project_id
                    self.stored_my_reaction_url = self.my_reaction_url
                    self.stored_original_video_url = self.original_video_url
                yield


@template(route="/viewer/[q]", title="Viewer", on_load=ViewerState.fetch_project)
def viewer() -> rx.Component:
    return video_container()
    # timestamps_list(timestamps)


def iframe_component(src: str, width: str = "100%", height: str = "100%") -> rx.Component:
    return rx.html(f'<iframe src="{src}" width="{width}" height="{height}"></iframe>')


def video_container() -> rx.Component:
    # return rx.hstack(
    #     rx.box(
    #         element="iframe",
    #         # src = ViewerState.my_reaction_url + "?enablejsapi=1&origin=http://localhost:3000", # +  rx.Var.create("window.location.href", _var_is_local=True),
    #         # width = "420",
    #         # height = "600",
    #         id = "my-reaction-video",
    #     ),
        # return rx.video(
        #     # element="iframe",
        #     url = ViewerState.original_video_url + "?enablejsapi=1&origin=http://localhost:3000", # + rx.Var.create("window.location.href", _var_is_local=True),
        #     width = "420",
        #     height = "600",
        #     id = "original-video",
        # )
    html_content = f"""
        <!DOCTYPE html>
        <html>
        <style>
            /* Inline block method */
            #player1, #player2 {{
                display: inline-block;
                width: 48%; /* or any desired width, just ensure they fit side by side */
                vertical-align: top; /* this will align the tops of the divs if they have different content heights */
                border: 1px solid black; /* optional, just to visualize the divs */
                box-sizing: border-box; /* to ensure the border width is included in the total width */
            }}
        </style>

        <body>
            <!-- 1. The <iframe> (and video player) will replace this <div> tag and place the divs side by side-->
            <div id="player1"></div>
            <div id="player2"></div>


            <script>
                var tag = document.createElement('script');

                tag.src = "https://www.youtube.com/iframe_api";
                var firstScriptTag = document.getElementsByTagName('script')[0];
                firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
                
                var project_id;
                var my_reaction;
                var original_video;
                var timestamps = [];

                var player1;
                var player2;

                function onYouTubeIframeAPIReady() {{
                    var localStorageCheckInterval = setInterval(function() {{
                        project_id = localStorage.getItem('project_id');
                        my_reaction = localStorage.getItem('my_reaction_url');
                        original_video = localStorage.getItem('original_video_url');

                        if (project_id && my_reaction && original_video) {{
                            clearInterval(localStorageCheckInterval); // clear the interval
                            my_reaction = my_reaction.split('v=')[1];
                            original_video = original_video.split('v=')[1];
                            
                            // now that we have the necessary data, proceed with initializing the YouTube player
                            createPlayers();
                        }}
                    }}, 500);
                    function createPlayers() {{
                        clearInterval(localStorageCheckInterval);
                        player1 = new YT.Player('player1', {{
                            height: '390',
                            width: '640',
                            videoId: my_reaction,
                            playerVars: {{
                                'playsinline': 1
                            }},
                            events: {{
                                'onReady': onPlayerReady,
                                'onStateChange': onPlayerStateChange
                            }}
                        }});
                        player2 = new YT.Player('player2', {{
                            height: '390',
                            width: '640',
                            videoId: original_video,
                            playerVars: {{
                                'playsinline': 1
                            }},
                        }});
                    }}
                }}

                function onPlayerReady(event) {{
                    fetchTimestamps();
                    event.target.playVideo();
                }}

                function fetchTimestamps() {{
                    fetch(`http://localhost:8000/timestamps/${{project_id}}`)
                        .then(response => response.json())
                        .then(data => {{
                            timestamps = data.result;
                            localStorage.clear();
                        }})
                        .catch(error => {{
                            console.error('Error fetching timestamps:', error);
                        }});
                }}

                function onPlayerStateChange(event) {{
                    let activeTimestamp = null;
                    let seen = false;
                    const buffer = 1;
                    const seekBuffer = 1;
                    let lastSeekTime = 0;

                    setInterval(function () {{
                        let currentTime = player1.getCurrentTime();

                        if (player1.getPlayerState() === 2) {{
                            player2.pauseVideo();
                            return;
                        }}

                        let currentTimestamp = timestamps.find(ts => currentTime > ts.start_time_my_reaction - buffer && currentTime < ts.end_time_my_reaction + buffer);

                        if (currentTimestamp) {{
                            if (activeTimestamp !== currentTimestamp) {{
                                seen = false;
                                activeTimestamp = currentTimestamp;
                            }}

                            let start2 = activeTimestamp.start_time_original;
                            let end2 = activeTimestamp.end_time_original;

                            if (!seen) {{
                                player2.seekTo(start2);
                                player2.playVideo();
                                seen = true;
                                lastSeekTime = Date.now();
                            }} else {{
                                let expectedTime = start2 + (currentTime - activeTimestamp.start_time_my_reaction);
                                let drift = Math.abs(player2.getCurrentTime() - expectedTime);

                                if (drift > seekBuffer && Date.now() - lastSeekTime > 5000) {{
                                    player2.seekTo(expectedTime);
                                    lastSeekTime = Date.now();
                                }}
                            }}

                            if (currentTime > activeTimestamp.end_time_my_reaction + buffer || player2.getCurrentTime() > end2 + buffer) {{
                                player2.pauseVideo();
                                seen = false;
                            }}
                        }} else if (activeTimestamp) {{
                            player2.pauseVideo();
                            seen = false;
                            activeTimestamp = null;
                        }}
                    }}, 1000);
                }}
            </script>
        </body>

        </html>
    """
    return rx.cond((ViewerState.stored_project_id is not None), rx.html(html_content), rx.text("Loading...")) 


def timestamps_list(timestamps: list) -> rx.Component:
    return rx.ul(
        [rx.li(f'My Reaction: {ts["start_time_my_reaction"]} - {ts["end_time_my_reaction"]} maps to Original: {ts["start_time_original"]} - {ts["end_time_original"]}') for ts in timestamps]
    )
