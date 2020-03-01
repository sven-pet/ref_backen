# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
import requests
from flask import Flask
import os
import pika
import threading
from riksdagen import Riksdagen
from riksdagen import Meeting
import redis

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

def rabbit():
    connection = pika.BlockingConnection( pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_consume( queue='hello', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def fill_data_base():
    r = Riksdagen()
    agendor = r.get_kalender()
    meetings = []
    for agenda in agendor['kalenderlista']['kalender']:
        meeting = Meeting(agenda)
        meeting.to_string()
        meetings.append(Meeting(agenda))
    
    for meeting in meetings:
        documents = meeting.data
        for document in documents:
            doc = r.get_documents(document)

    return str(meetings)

@app.route('/')
def hello():
    '''if os.environ.get('GAE_ENV') == 'standard':
        db_user = 'ymudhkn
        npw'
        db_password = 'qDySVjUhRFH8F89ACkRy5NomIM2BelGo'
        db_name = 'riksdagen'
        host = 'balarama.db.elephantsql.com'
        cnx = psycopg2.connect(user=db_user, password=db_password,
                              host=host, database=db_name)
    else:
        db_user = 'root'
        db_password = 'qwer1234'
        db_name = 'referendum'
        db_connection_name = 'referendum'
        host = 'balarama.db.elephantsql.com'
        cnx = psycopg2.connect(user=db_user, password=db_password,
                              host=host, database=db_name)
    result = ""
    with cnx.cursor() as cursor:
        cursor.execute('SELECT * FROM account;')
        result = cursor.fetchall()
    cnx.close()'''
    return str("hello")

@app.route('/fill_database')
def fill_database():
    return fill_data_base()


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    x = threading.Thread(target=rabbit, args=(), daemon=True)
    x.start()
    app.run(host='127.0.0.1', port=8080, debug=True)
    

# [END gae_python37_app]
