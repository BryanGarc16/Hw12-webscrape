from bs4 import BeautifulSoup

file_path = "C:\\Users\\bgarc\\PycharmProjects\\webscrape 11-3-25\\data\\Class Schedules.html"

with open(file_path) as file:
    text = file.read()
    soup = BeautifulSoup(text, "html.parser")


table = soup.find("table", class_="dataentrytable") #if not found, returns NoneType

professorDict = {}
validCourseRows = [23,16]



count = 0

#for in person box #20 = instructor, box #15 = enrolled
#for pure online box #14 = instructor, box #9 = enrolled

for row in table.find_all("tr"):
    columns = row.find_all("td")
    values = [column.text for column in columns]





    if values[0] == "In Progress" or values[0] == "Completed":
        if len(values) == 23:
            if values[20] == "":
               continue
            if values[20] not in professorDict:
                professorDict[values[20]] = int(values[15])
            else:
                professorDict[values[20]] += int(values[15])

        if len(values) == 16:
            if values[14] not in professorDict:
                if values[14] == "":
                    continue
                professorDict[values[14]] = int(values[9])
            else:
                professorDict[values[14]] += int(values[9])



sortedProfessors = sorted(professorDict.items(), key=lambda x: x[1], reverse=True)
print(sortedProfessors)

for professor, num in sortedProfessors:
    print(f"{professor}: {num}")

