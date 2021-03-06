import re
import aprs
import json
import binascii

from io import StringIO

"""
Frame tools used to build and validate frames.

The robot should have a copy of this library as well.
"""


def buildDataFrame(data: dict):
    """
    Constructs a new data frame
    """

    # Text encoding to use
    encoding = "utf-8"

    # Payload
    payload = bytes(json.dumps(data), encoding)
    payloadCRC = bytes(str(binascii.crc32(payload)), encoding)

    # Deliminate and package crc with payload
    delim = bytes(":", encoding)
    fmt_payload = payload + delim + payloadCRC + delim

    # Construct frame
    dataFrame = aprs.PositionFrame(
        source=b"KW1FOX-1",
        destination=b"KW1FOX-3",
        path=["WIDE1-1"],
        table=b"/",
        symbol=b"`",
        lat=43.167720,
        lng=-71.557380,
        ambiguity=0,
        comment=fmt_payload,
    )

    return dataFrame


def validateDataFrame(frame, partial_frame=False):
    """
    Uses the CRC to validate a frame's data

    Returns the stripped json (if valid) and a valid bool
    ex: ({}, True)
    """

    # Text encoding to use
    encoding = "utf-8"

    # Strip the json out
    stripped_json = "{" + re.search("{(.*?)}", str(frame)).group(1) + "}"

    # Convert the stripped json to a dict
    stripped_dict = json.load(StringIO(stripped_json))

    # Strip the CRC out
    stripped_crc = str(frame).split(":")

    # This is super messy but it works lol <3
    for split in stripped_crc:
        try:
            if int(binascii.crc32(bytes(stripped_json, encoding))) == int(split):
                return (stripped_dict, True)
        except ValueError:
            pass

    if not partial_frame:
        return ({}, False)
    else:
        return (stripped_dict, False)
