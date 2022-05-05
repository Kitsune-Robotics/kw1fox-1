"""
Collection of Robot Streamer Specific stuff.

And imported mess, mostly imported mess.
"""

import json

import robotstreamer_utils.robot_util as robot_util

"""
From https://github.com/robotstreamer/robotstreamer/blob/2f89d9acbca949ab0a9e2f8229da8c2cc1ffb26b/send_video.py#L155
"""


def getVideoEndpoint(apiServer="http://api.robotstreamer.com:8080", camera_id=0):
    url = f"{apiServer}/v1/get_endpoint/jsmpeg_video_capture/{camera_id}"
    response = robot_util.getWithRetry(url)
    return json.loads(response)
