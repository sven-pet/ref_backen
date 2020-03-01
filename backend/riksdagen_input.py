from riksdagen import Riksdagen
from redis import Redis
import json

def main():
  print("Hello World!")
  fill_data_base()

def fill_data_base():
    r = Riksdagen()
    redis = Redis()
    agendor = r.get_kalender()
    for agenda in agendor['kalenderlista']['kalender']:
        if str(agenda['XRDDATA']).count('}'):
            documents = str(agenda['XRDDATA']).split('}')[0].replace('dok_id{','').split(',')
        else:
            documents = []
        descriptions = str(agenda['DESCRIPTION'][1]).split('\\n\\n')
        for description in descriptions:
            description = description.replace('\\n','')
            description = description.replace('\\','')
        agenda_dict = {
            "End":agenda['DTEND'],
            "Start":agenda['DTSTART'],
            "Created":agenda['CREATED'],
            "Documents":str(documents),
            "Description": str(descriptions)
        }
        redis.set(agenda['UID'], json.dumps(agenda_dict))
        result=redis.get(agenda['UID'])
        redis.lpush('Agendor', agenda['UID'])

        for document_id in documents:
            redis.lpush(agenda['UID']+"-docs", document_id)
            document = r.get_documents(document_id)['dokumentlista']['dokument'][0]
            redis.set(document_id, json.dumps(document))
            

    result_2 = redis.lrange('Agendor',0,redis.llen('Agendor'))
    return
  
if __name__== "__main__":
  main()

print("Guru99")
