import string

s = open("Database.txt", "r+")
for line in s.readlines():
    print(line)
s.close()
