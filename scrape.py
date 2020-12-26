import requests
from bs4 import BeautifulSoup
import lxml
from io import StringIO
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

agendaList = []
source = requests.get('https://destinyhosted.com/agenda_publish.cfm?id=56691').text
soup = BeautifulSoup(source, 'lxml')

agendas = soup.find('table', {'id':'list'}).select('tbody > tr')
for num, item in enumerate(agendas, start=0):
  link = 'https://destinyhosted.com/' + agendas[num].findChild("a")['href']
  title = strip_tags(str(agendas[num].findChild('td').find_next_sibling('td')))
  agendaList.append({ 'title': title, 'link': link})

print(agendaList)
