# This is the Linkedin Part
import json

js = open('sample.json').read()
data = json.loads(js)

BoardDirectors_Parsed = {}
BoD = data["BoardDirectors"].split("\n")
i = -3
r = 0
for x in range(len(BoD)):
    i = i + 3
    r = i + 3
    print(i, r)
    part = BoD[i:r]
    try:
        BoardDirectors_Parsed["Name", i] = part[0].split(",")[0]
        BoardDirectors_Parsed["Age", i] = part[0].split(",")[1]
        BoardDirectors_Parsed["Title", i] = part[1].split("Since")[0]
        BoardDirectors_Parsed["Since", i] = part[1].split("Since")[1][2:]
        BoardDirectors_Parsed["Description", i] = part[2].split("Since")[0]
    except:
        break

data["BoardDirectors_Parsed"] = BoardDirectors_Parsed

