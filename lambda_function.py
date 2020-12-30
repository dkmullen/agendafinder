import requests
from bs4 import BeautifulSoup
import lxml
from io import StringIO
from html.parser import HTMLParser
import json

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

def lambda_handler(event, context):

    agendaDict = {}
    source = requests.get('https://destinyhosted.com/agenda_publish.cfm?id=56691').text
    soup = BeautifulSoup(source, 'html.parser')

    agendas = soup.find('table', {'id':'list'}).select('tbody > tr')
    for num, item in enumerate(agendas, start=0):
        d = str(agendas[num].findChild('a'))
        date = strip_tags(d)
        link = 'https://destinyhosted.com/' + agendas[num].findChild("a")['href']
        title = strip_tags(str(agendas[num].findChild('td').find_next_sibling('td')))
        tempDict = {num: {'title': title, 'date': date, 'link': link}}
        agendaDict.update(tempDict)

    print(json.dumps(agendaDict))
    return({
        'statusCode': 200,
        'body': json.dumps(agendaDict) 
    })
        
        


