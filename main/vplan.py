from bs4 import BeautifulSoup
import urllib.request


# Beispiel Schule mit Website VPlan ist https://gms-kellinghusen.de/vertretungsplan.html
# da Ferien sind und der Plan dann leer ist, haben wir die Seite temporär und mit Einträgen angereichtert gehostet unter
# http://schmeckerly.de/kellinghusen/vertretungsplan
class VPlan:
    def __init__(self, name, url):
        self.website = self.gethtml(url)
        self.name = name
        self.gradeList = self.get_grade_list()
        self.grades = self.get_grade_objects()

    def gethtml(self, url):
        soup = ''
        if url and len(url) > 3:
            with urllib.request.urlopen(url) as f:
                plan = f.read()
            soup = BeautifulSoup(plan, 'html.parser')

        return soup

    def get_grade_list(self):
        grades = []
        if self.website:
            grade_nodes = self.website.select('.v-klasse')

            for grade in grade_nodes:
                grades.append(grade.text)

        return grades

    def get_grade_objects(self):
        grade_dict = {}
        if self.website:
            rows = self.website.select('.v-row')

            for row in rows:
                node = row.select('.v-klasse')
                if node:
                    infos = row.select('.v-stunde')
                    infotext = ''
                    for std, info in enumerate(infos):
                        # only add grade if it has an info
                        if len(info.text) > 0:
                            infotext += '=> ' + str(std+1) + '. Stunde: ' + info.text + ' '
                            grade_dict[node[0].text] = infotext

        return grade_dict
