from googleapiclient.discovery import build
from dotenv import load_dotenv
import os, json


class YouTubechennel:
    def __init__(self, ch_id):
        load_dotenv()
        api_key: str = os.getenv('API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.ch_id = ch_id
        self.chennel = self.youtube.channels().list(id=ch_id, part='snippet,statistics').execute()
        self.title = self.chennel['items'][0]["snippet"]["title"]  # название канала
        self.desc = self.chennel['items'][0]["snippet"]["description"]  # описание
        self.url = "https://www.youtube.com/" + self.ch_id  # ссылка на канал
        self.subs_count = self.chennel['items'][0]["statistics"]["subscriberCount"]  # кол-во подписчиков
        self.video_count = self.chennel['items'][0]["statistics"]["videoCount"]  # кол-во видео
        self.view_count = self.chennel['items'][0]["statistics"]["viewCount"]  # кол-во просмотров

    def print_info(self):
        channel = self.youtube.channels().list(id=self.ch_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))


vdud = YouTubechennel("UCqzgQIvvti_uZMoBxmxaihw")
vdud.print_info()
