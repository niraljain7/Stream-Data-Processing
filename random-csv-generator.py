import random

f = open("random.csv", "w")

for i in range(5000):
    f.write(str(random.randrange(0, 500, 3)))
    f.write(",")

f.write(str(random.randrange(20, 50, 3)))
f.close()
