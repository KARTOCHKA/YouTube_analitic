from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import json


class YouTubechennel:
    def __init__(self, ch_id):
        load_dotenv()
        api_key: str = os.getenv('API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.__ch_id = ch_id
        self.chennel = self.youtube.channels().list(id=ch_id, part='snippet,statistics').execute()
        self.title = self.chennel['items'][0]["snippet"]["title"]  # название канала
        self.desc = self.chennel['items'][0]["snippet"]["description"]  # описание
        self.url = "https://www.youtube.com/" + self.__ch_id  # ссылка на канал
        self.subs_count = self.chennel['items'][0]["statistics"]["subscriberCount"]  # кол-во подписчиков
        self.video_count = self.chennel['items'][0]["statistics"]["videoCount"]  # кол-во видео
        self.view_count = self.chennel['items'][0]["statistics"]["viewCount"]  # кол-во просмотров

    def print_info(self):
        channel = self.youtube.channels().list(id=self.__ch_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @property
    def channel_id(self) -> str:
        """Получение id канала"""
        return self.__ch_id

    @staticmethod
    def get_service() -> object:
        """Возвращает объект для работы с API ютуба"""
        load_dotenv()
        api_key: str = os.getenv('API_KEY')  # получение ключа из файла .env
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, name_json):
        """Сохраняет информацию по каналу, хранящуюся в атрибутах экземпляра класса в json-файл"""
        with open(name_json, 'w', encoding='UTF=8') as file:
            data = {
                'id': self.__ch_id, 'title': self.title, 'description': self.desc, 'url': self.url,
                'subscriber_count': self.subs_count, 'video_count': self.video_count,
                'view_count': self.view_count
            }
            return json.dump(data, file, indent=2, ensure_ascii=False)