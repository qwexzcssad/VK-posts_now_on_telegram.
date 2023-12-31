import time
from flask import Flask
import threading

# Решил добавить что от куда импортируется, чтобы было понятнее, сам запутался пока делал изменения
from config import community_ids, access_token, blacklist_file, downloaded_post
from downloading import get_latest_posts, download_media_from_posts
from downloading import downloaded_post_ids, downloaded_post_ids
from moderation import moderation, write_post_ids_to_file, read_downloaded_post_ids
from posting import perform_action_after_downloading

# Создаем сервер
app = Flask(__name__)

@app.route('/')
def home():
    return 'Kill urself!'
 
# Функция для поддержания сервера
def keep_alive():
    app.run(host='0.0.0.0', port=4000)

if __name__ == "__main__":
    # Запускаем функцию в отдельном потоке
    keep_alive_thread = threading.Thread(target=keep_alive)
    keep_alive_thread.start()

    while True:
        for community_id in community_ids:
            latest_posts = get_latest_posts(community_id, access_token)

            # Сохраняется только пост прошедший модерацию и не был скачен до этого
            for post in latest_posts:
                if moderation(post, blacklist_file):
                    downloaded_media = download_media_from_posts([post], "media", downloaded_post_ids, community_id)
                    perform_action_after_downloading(downloaded_media)
                    break

        # Айди сохраненных постов записываются в файл, чтобы не скачивались повторно
        new_post_ids = set(downloaded_post_ids) - read_downloaded_post_ids(downloaded_post)
        if new_post_ids:
            write_post_ids_to_file(new_post_ids, downloaded_post)

        time.sleep(60)