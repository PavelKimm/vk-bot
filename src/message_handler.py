from datetime import datetime
from src import config
from src import vkapi
import os
import importlib
import requests
import json


def load_modules():
    files = os.listdir("./commands")
    modules = filter(lambda x: x.endswith('.py'), files)
    for m in modules:
        importlib.import_module("commands." + m[0:-3])


def make_request(message):
    request_url = config.rasa_url + "/model/parse"
    json_data = {'text': message}
    response = requests.post(request_url, json=json_data)
    if response.status_code >= 300:
        raise Exception(f'Requests error. {response.status_code}.\nMessage: {response.text}')
    return response


def create_answer(data, token):
    load_modules()
    user_id = data['user_id']
    message = data['body']
    response = make_request(message)
    json_response = json.loads(response.text)
    intent, entities = extract_data_from_json(json_response)

    if intent == "work_logging":
        if entities:
            try:
                a = log_time(intent, entities)
                vkapi.send_message(user_id, token, a)
            except:
                print('failed')
                vkapi.send_message(user_id, token, "не все entities распознаны")
                print(entities)
        else:
            vkapi.send_message(user_id, token, "entities не распознаны")
    else:
        vkapi.send_message(user_id, token, "Команда не распознана")


def extract_data_from_json(json_response):
    intent = json_response['intent']['name']
    entities = None
    if intent:
        try:
            entities = {entity['entity']: entity['value'] for entity in json_response['entities']}
        except KeyError:
            print('failed')
    return intent, entities


def log_time(intent, entities):
    if intent == "work_logging":
        host = config.JIRA['host']
        user = config.JIRA['master']
        request_url = f"https://{host}/rest/api/latest/issue/{entities['issue_name'].upper()}/worklog"

        try:
            comment = entities['comment']
        except:
            return "комментарий не распознан"

        try:
            time_spent = entities['spent_time']
        except:
            return "затраченное время не распознано"

        datetime_obj = datetime.now()
        logging_time = datetime_obj.strftime("%Y-%m-%dT%H:%M:00.000+0700")
        started = logging_time

        json_data = {
            'comment': comment,
            'timeSpent': time_spent,
            'started': started
        }
        request = requests.post(url=request_url, json=json_data, auth=user)

        if request.status_code >= 300:
            raise Exception(f'Requests error. {request.status_code}.\nMessage: {request.text}')

        return f"[{time_spent}] с комментарием [{comment}] в задачу " \
               f"[{entities['issue_name']}] успешно залогированы ({str(datetime_obj)[:16]})"
