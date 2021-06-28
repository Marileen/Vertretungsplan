from bs4 import BeautifulSoup
import urllib.request


class VGrade:
    def __init__(self, name, info):
        self.name = name
        self.info = info

    def __str__(self):
        return self.name + ': ' + self.info


# Beispiel Schule mit Website VPlan ist https://gms-kellinghusen.de/vertretungsplan.html
# da Ferien sind und der Plan dann leer ist, haben wir die Seite temporär und mit Einträgen angereichtert gehostet unter
# http://schmeckerly.de/kellinghusen/vertretungsplan
# todo: prefill DB with schools on app init (or provide dump)
class VPlan:
    def __init__(self, name, url):
        self.website = self.gethtml(url)
        self.name = name
        self.gradeList = self.getGradeList()
        self.grades = self.getGradeObjects()

    def gethtml(self, url):
        soup = ''
        if url and len(url) > 3:
            with urllib.request.urlopen(url) as f:
                plan = f.read()
            soup = BeautifulSoup(plan, 'html.parser')

        return soup

    def getGradeList(self):
        grades = []
        if self.website:
            grade_nodes = self.website.select('.v-klasse')

            for grade in grade_nodes:
                grades.append(grade.text)

            print(grades)

        return grades

    def getGradeObjects(self):
        gradeObjects = []
        if self.website:
            rows = self.website.select('.v-row')

            for row in rows:
                node = row.select('.v-klasse')
                if node:
                    infos = row.select('.v-stunde')
                    infotext = ''
                    for std, info in enumerate(infos):
                        if len(info.text) > 0:
                            infotext += '=> ' + str(std+1) + '. Stunde: ' + info.text + ' '
                    gradeObj = VGrade(node[0].text, infotext)
                    gradeObjects.append(gradeObj)
                    print(gradeObjects)

        return gradeObjects

