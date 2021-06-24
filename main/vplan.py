from bs4 import BeautifulSoup
import urllib.request

class VPlan:
    def __init__(self, name, url):
        self.website = self.gethtml('https://gms-kellinghusen.de/vertretungsplan.html')
        self.name = name
        self.grades = self.getGrades()

    def gethtml(self, url):
        # url = 'https://gms-kellinghusen.de/vertretungsplan.html'

        with urllib.request.urlopen(url) as f:
            plan = f.read()

        soup = BeautifulSoup(plan, 'html.parser')
        return soup

    def getGrades(self):

        grades = []
        grade_nodes = self.website.select('.v-klasse')

        for grade in grade_nodes:
            grades.append(grade.text)

        print(grades)

        return grades

