import string

s = open("Database.txt", "r+")
for line in s.readlines():
    x = line.split("|")
    size = len(x)
    print(size)
s.close()
