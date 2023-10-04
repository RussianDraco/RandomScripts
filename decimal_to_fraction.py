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

nof10 = 0

while not fully_int(s_d):
    pp = list(s_d).index(".") + 1
    s_d = s_d.replace(".", "")
    s_d = s_d[:pp] + "." + s_d[pp:]
    nof10+=1

while s_d[-1] == 0:
    s_d = s_d[:-1]

s_d = int(s_d.replace(".", ""))

numer = s_d
demon = 10 ** nof10

for x in range(numer//2 + 1, 1, -1):
    if numer % x == 0 and demon % x == 0:
        numer /= x
        demon /= x

dash_num = max(len(list(str(int(numer)))), len(list(str(int(demon)))))

print((dash_num - len(list(str(int(numer)))))//2 * " " + str(int(numer)))
print(dash_num * "—")
print(int(demon))