from bs4 import BeautifulSoup
import urllib.request

class VPlan:
    def __init__(self, name, url):
        self.website = self.gethtml(url)
        self.name = name
        self.grades = self.getGrades()

    def gethtml(self, url):
        soup = ''
        if url and len(url) > 3:
            with urllib.request.urlopen(url) as f:
                plan = f.read()
            soup = BeautifulSoup(plan, 'html.parser')

        return soup

    def getGrades(self):
        grades = []
        if self.website:
            grade_nodes = self.website.select('.v-klasse')

            for grade in grade_nodes:
                grades.append(grade.text)

            print(grades)

        return grades

