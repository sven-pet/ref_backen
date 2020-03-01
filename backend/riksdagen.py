import requests
import json

class Riksdagen (object):
    def get_kalender(self):

        url = "http://data.riksdagen.se/kalender"
        payload = {'akt': 'vo', 'utformat': 'json'}
        r = requests.get(url, params=payload)
        return json.loads(r.content)

    def get_documents(self, document_id):

        url = "http://data.riksdagen.se/dokumentlista/"
        payload = {'sok': document_id,'utformat': 'json'}
        r = requests.get(url, params=payload)
        return json.loads(r.content)

'''class Meeting(object):

    def __init__(self, agenda):
        descriptions = str(agenda['DESCRIPTION'][1]).split('\\n\\n')

        for description in descriptions:
            description = str(description).replace('\\n', ' ')

        self.uid = agenda['UID']
        self.desc = description
        if str(agenda['XRDDATA']).count('}'):
            self.data = str(agenda['XRDDATA']).split('}')[0].replace('dok_id{','').split(',')
        else:
            self.data = []
        self.start = agenda['DTSTART']
        self.end = agenda['DTEND']
        self.dict = {
            "Start": self.start,
            "End": self.end,
            "Documents": self.data,
            "Desc": self.desc,

        }

    def to_string(self):
        print('**********************************************')
        print('')
        print('Start {}'.format(self.start))
        print('')
        print('End {}'.format(self.end))
        print('')
        print('Documents {}'.format(self.data))
        print('')
        for description in self.desc:
            print (description)
        print('')
        print('**********************************************')'''