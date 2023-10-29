import base36

TIME2000 = 946684800000


def genid(time):
    num = time-TIME2000
    return base36.dumps(num)