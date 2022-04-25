import aprs
import json
import binascii


data = {
    "CMD": "NOOP",
    "ARGS": "-tcvz --batt-on",
}


payload = bytes(json.dumps(data), "utf-8")
payloadCRC = bytes(str(binascii.crc32(payload)), "utf-8")

fmt_payload = payload + bytes(":", "utf-8") + payloadCRC


testFrame = aprs.PositionFrame(
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


print(testFrame)
