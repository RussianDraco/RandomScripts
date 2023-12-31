class Hashmap:
    def __init__(self, length):
        self.length = length
        self.holder = [[] for x in range(length)]

    def hash_key(self, v):
        return sum([ord(x) for x in list(v)]) % self.length

    def addValue(self, key, val):
        k = self.hash_key(key)
        v = self.holder[k]

        if self.holder[k] == []:
            self.holder[k] = [key, val]
        else:
            o = k
            tryr = False

            while v != []:
                k+=1
                if k == o: return None
                try:
                    v = self.holder[k]
                except IndexError:
                    if not tryr:
                        tryr = True
                        k = 0
                        v = self.holder[k]
                    else:
                        print("No space left in array")
                        return None
            self.holder[k] = [key, val]

    def getValue(self, key):
        k = self.hash_key(key)
        o = k
        v = self.holder[k]

        if v[0] == key:
            return v[1]
        
        tryr = False

        while v[0] != key:
            k+=1
            if k == o: return None
            try:
                v = self.holder[k]
            except IndexError:
                if not tryr:
                    tryr = True
                    k = 0
                    v = self.holder[k]
                else:
                    return None
        return v[1]
    
    def printMap(self):
        for x in self.holder:
            print(str(x))