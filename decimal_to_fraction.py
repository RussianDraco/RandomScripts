print("Input decimal...")
in_dec = float(input(">"))

def fully_int(sd):
    sdl = list(sd)
    pp = sdl.index(".")
    afterp = sdl[pp + 1:]
    for x in afterp:
        if x != "0":
            return False
    return True

#basic implementation lacking some specific/accurate fractions

s_d = str(in_dec)

while not fully_int(s_d):
    pp = list(s_d).index(".") + 1
    s_d = s_d.replace(".", "")
    s_d = s_d[:pp] + "." + s_d[pp:]

while s_d[-1] == 0:
    s_d = s_d[:-1]

s_d = int(s_d.replace(".", ""))

