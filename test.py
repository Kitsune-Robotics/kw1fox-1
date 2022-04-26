import aprs

frame = aprs.parse_frame("W2GMD>APRS:>Hello World!")

a = aprs.TCP(b"W2GMD", b"12345")
a.start()

a.send(frame)
