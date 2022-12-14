import random
from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests


with open("tokenAPI_VK.txt", "r") as file_object:
    token_vk = file_object.read().strip()

class VkApiClient:
    def __init__(self, token_vk: str, api_version: str, base_url: str = "https://api.vk.com/"):
        self.token_vk = token_vk
        self.api_version = api_version
        self.base_url = base_url

    def general_params(self):
        return {
            "access_token": self.token_vk,
            "v": self.api_version,
            "offset": 10,
            "count": 5
        }

    def get_user_info(self, user_ids: str):
        params = {
            "user_ids": user_ids,
            "fields": 'sex, bdate, relation, title, has_photo'
        }
        return requests.get(f"{self.base_url}/method/users.get",
                            params={**params, **self.general_params()}).json()['response']

    def user_seach_friend(self, list_of_parameters: list):
        params = {
            "relation": 6,
            "sex": list_of_parameters[0],
            "title": list_of_parameters[1],
            "age_from": list_of_parameters[2],
            "age_to": list_of_parameters[3],
            "has_photo": 1,
            "fields": "photo_max_orig"
        }
        res = requests.get(f"{self.base_url}/method/users.search", params={**params, **self.general_params()}).json()[
            'response']['items']
        return res


with open(file="token_gr.txt", mode='r') as file_object:
    token = file_object.read().strip()

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
list_of_parameters = []
vk_client = VkApiClient(token_vk=token_vk, api_version="5.131")


def get_name(user_id: int):
    data = vk.method("users.get", {"user_ids": user_id})[0]
    return f"{data['first_name']} {data['last_name']}"

def get_sex(user_id: int):
    for key, value in info_user[0].items():
        if key == 'sex':
           sex_user=value
    if sex_user == 1:
        sex_user = 2
    elif sex_user == 2:
        sex_user = 1
    return sex_user



def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), })

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        request = event.text.lower()
        if "????" in request:
            name = event.user_id
            full_name = get_name(name)
            info_user = vk_client.get_user_info(name)
            sex = get_sex(name)
            list_of_parameters.append(sex)

            write_msg(event.user_id, f"????????????, {full_name}! ?????????????????? ?? ????????????!")
            for key, value in info_user[0].items():
                if key == 'relation' and (value == '2', '3', '4', '7', '8'):
                    write_msg(event.user_id, f'????-????-????, {full_name}, ?? ???????? ?????? ???????? ????????! ?????????? ???? ???????? ????????????!')
                else:
                    write_msg(event.user_id, '???????????? ??????????, ?????? ?????????? ???????????? ????????????')
                    for event in longpoll.listen():
                        if event.type == VkEventType.MESSAGE_NEW:
                            if event.to_me:
                                request = event.text.lower()
                                list_of_parameters.append(request)

                                write_msg(event.user_id, '???????????? ??????????????, ???? (2 ??????????)')
                                for event in longpoll.listen():
                                    if event.type == VkEventType.MESSAGE_NEW:
                                        if event.to_me:
                                            request = event.text.lower()
                                            list_of_parameters.append(request)

                                            write_msg(event.user_id, '???????????? ??????????????, ???? (2 ??????????)')
                                            for event in longpoll.listen():
                                                if event.type == VkEventType.MESSAGE_NEW:
                                                    if event.to_me:
                                                        request = event.text.lower()
                                                        list_of_parameters.append(request)
                                                        print(list_of_parameters)
                                                        write_msg(event.user_id, f'?????? ')
                                                        res=vk_client.user_seach_friend(list_of_parameters=list_of_parameters)
                                                        for user in res:
                                                            write_msg(event.user_id, f"{user['last_name']} {user['first_name']} https://vk.com/id{user['id']},  {user['photo_max_orig']}")


        else:
            write_msg(event.user_id, '???????????? ??????????????????????????????, ?????????? ???????????????? ??????????????????!')

pprint(user_seach_friend(list_of_parametrs))
