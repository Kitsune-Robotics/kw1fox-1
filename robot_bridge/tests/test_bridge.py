from tools.frametools import buildDataFrame, validateDataFrame


# Common sample data
data = {
    "CMD": "NOOP",
    "ARGS": "-tcv --batt-on",
}


def test_validate_good_frame():
    frame = buildDataFrame(data)

    assert validateDataFrame(frame)[1] == True


def test_validate_good_frame_data():
    frame = buildDataFrame(data)

    assert validateDataFrame(frame)[0] == data


def test_validate_bad_frame():
    frame = buildDataFrame(data)

    # Damage frame
    frame = str(frame)[:50] + "Z" + str(frame)[51:]

    assert validateDataFrame(frame)[1] == False
