import requests
from datetime import datetime

# date = datetime.today().strftime('%Y-%m-%d') # aktuelles Tagesdatum
date = '2021-06-11' # Testdatum

url = 'http://kgbe.de.w010c7c5.kasserver.com/Joomla/files/vplan/' +date +'.pdf'

r = requests.get(url)

print(r.status_code)  # prüfen, ob Datei vorhanden ist

if r.status_code == 200:

    if url.find('/'):
        filename = url.rsplit('/', 1)[1]
    open(filename, 'wb').write(r.content)
    print('Datei ' +filename +' heruntergeladen')
else:
    print('Kein aktueller Vertretungsplan vorhanden')
