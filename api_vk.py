import vk_api
from vk_api import ApiError

from config import ACCESS_KEY

session = vk_api.VkApi(token=ACCESS_KEY)


# Статус пользователя
def get_user_status(vk_id = 223134565):
    try:
        status = session.method('status.get', {'user_id': vk_id})
        return status
    except ApiError as e:
        if e.code == 200:
            return None



# Аватарка пользователя

def get_user_avatar(vk_id=223134565):
    avatar = session.method('photos.get', {'user_id': vk_id, 'album_id': 'profile'})
    return avatar

# print(get_user_avatar())




# Сохраненки пользователя
def get_user_photos_saved(vk_id = 223134565):
    try:
        photos = session.method('photos.get', {'owner_id': vk_id, 'album_id': 'saved', 'count': 10, 'rev': 1})
        photo_list = [i['sizes'][-1]['url'] for i in photos['items']]
        return photo_list
    except ApiError as e:
        if e.code == 200:
            return None


# print(get_user_photos_saved())



