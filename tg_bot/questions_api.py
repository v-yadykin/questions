import requests
import settings


headers = dict(Authorization='Token ' + settings.QUESTIONS_API_TOKEN)
base_url = settings.QUESTIONS_API_URL


def login(tg_login, tg_name):
    r = requests.get(base_url+'user/', params={'search': tg_login}, headers=headers)
    r.raise_for_status()

    objects = r.json()
    if len(objects) != 0:
        return objects[0]

    r = requests.post(
        base_url+'user/', json=dict(tg_login=tg_login, tg_name=tg_name), headers = headers
    )
    r.raise_for_status()

    return r.json()

def send_question(user_id, text):
    r = requests.post(
        base_url+'question/', json=dict(user=user_id, text=text), headers=headers
    )
    r.raise_for_status()

    return r.json()

def get_resources(question_id, batch_start=0, batch_size=5):
    data = dict(question_id=question_id, batch_start=batch_start, batch_size=batch_size)
    r = requests.post(base_url+'resource/', json=data, headers=headers)
    r.raise_for_status()
    
    return r.json()
