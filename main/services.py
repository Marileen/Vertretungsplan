import urllib.request
from datetime import datetime


def filedownload():

    # date = datetime.today().strftime('%Y-%m-%d') # aktuelles Tagesdatum
    date = '2021-06-11'  # Testdatum

    url = 'http://kgbe.de.w010c7c5.kasserver.com/Joomla/files/vplan/' + date + '.pdf'

    with urllib.request.urlopen(url) as f:
        pdf = f.read()

    if url.find('/'):
        filename = 'downloads/' + url.rsplit('/', 1)[1]
    open(filename, 'wb').write(pdf)
    print('Datei ' + filename + ' heruntergeladen')
