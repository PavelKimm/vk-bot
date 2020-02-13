from src import config
from src.models import User, Project
from src.flask_app import session
from datetime import datetime, timedelta
import vkapi
import requests
import json


def create_answer(data, token):
    user_id = data['user_id']
    message = data['body']
    response = make_request(message)
    json_response = json.loads(response.text)
    intent, entities = extract_data_from_json(json_response)

    define_and_execute_command(intent, entities, user_id, token)


def make_request(message):
    request_url = config.rasa_url + "/model/parse"
    json_data = {'text': message}
    response = requests.post(request_url, json=json_data)
    if response.status_code >= 300:
        raise Exception(f'Requests error. {response.status_code}.\nMessage: {response.text}')
    return response


def extract_data_from_json(json_response):
    intent = json_response['intent']['name']
    entities = None
    if intent:
        try:
            entities = {entity['entity']: entity['value'] for entity in json_response['entities']}
        except KeyError:
            print('ошибка извлечения данных')
    return intent, entities


def define_and_execute_command(intent, entities, user_id, token):
    host = session.query(Project).filter(Project.project_name == 'ssp').first()
    user = session.query(User) \
        .filter(User.project_name == host.project_name).filter(User.user_name == str(user_id)).first()

    if intent == "work_logging":
        if entities:
            try:
                answer = log_time(host, user, entities)
                vkapi.send_message(user_id, token, answer)
            except:
                vkapi.send_message(user_id, token, "не все entities распознаны")
                print(entities)
        else:
            vkapi.send_message(user_id, token, "entities не распознаны")
    elif intent == "get_my_tasks":
        start_date = datetime.now().date() - timedelta(days=30)
        jql = f'worklogAuthor = {user.login} AND worklogDate >= {start_date}'
        answer = get_my_tasks(host, user,
                              json_data={'jql': jql, 'startAt': 0, 'maxResults': 100, 'fields': ['summary', 'project']})
        vkapi.send_message(user_id, token, answer)
    else:
        vkapi.send_message(user_id, token, "Команда не распознана")


def get_my_tasks(host, user, json_data):
    request_url = f"https://{host.url}/rest/api/latest/search/"
    request = requests.post(url=request_url, json=json_data, auth=(user.login, user.password))
    if request.status_code >= 300:
        raise Exception(f'Requests error. {request.status_code}.\nMessage: {request.text}')
    task_count = request.json()['total']
    tasks = request.json()['issues']
    tasks_summary = ""
    for task in tasks:
        tasks_summary += f"{task['key']}: {task['fields']['summary']}\n"
    return f"Всего тасков: {task_count}\n{tasks_summary}"


def log_time(host, user, entities):
    login = user.login
    password = user.password
    request_url = f"https://{host.url}/rest/api/latest/issue/{entities['issue_name'].upper()}/worklog"

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
    request = requests.post(url=request_url, json=json_data, auth=(login, password))

    if request.status_code >= 300:
        raise Exception(f'Requests error. {request.status_code}.\nMessage: {request.text}')

    return f"[{time_spent}] с комментарием [{comment}] в задачу " \
           f"[{entities['issue_name']}] успешно залогированы ({str(datetime_obj)[:16]})"
