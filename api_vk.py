import vk_api
from config import ACCESS_KEY

session = vk_api.VkApi(token=ACCESS_KEY)

def get_user_status(user_id):
    status = session.method('status.get', {'user_id': user_id})
    return status


def get_user_photos_saved(owner_id):
    photos = session.method('photos.get', {'owner_id': owner_id, 'album_id': 'saved', 'count': 10, 'rev': 1})

    return photos


a = get_user_photos_saved(223134565)

photo_list = [i['sizes'][-1]['url'] for i in a['items']]

# print(photo_list)

