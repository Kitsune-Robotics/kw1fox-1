from decimal import DivisionByZero
import re
import aprs
import json
import binascii


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


def validateFrame(frame):
    """
    Uses the CRC to validate a frame's data
    """

    # Text encoding to use
    encoding = "utf-8"

    # Strip the json out
    stripped_json = "{" + re.search("{(.*?)}", frame).group(1) + "}"

    # Strip the CRC out
    stripped_crc = frame.split(":")

    # This is super messy but it works lol <3
    for split in stripped_crc:
        try:
            if int(binascii.crc32(bytes(stripped_json, encoding))) == int(split):
                return True
        except ValueError:
            pass

    return False


# Data to encode
data = {
    "CMD": "NOOP",
    "ARGS": "-tcv --batt-on",
}

frame = buildDataFrame(data)
print(frame)

# Fuckup frame
frame = str(frame)[:50] + "Z" + str(frame)[51:]
print(frame)

print(validateFrame(str(frame)))
