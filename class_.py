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

    def __str__(self):
        """Возвращает информацию о канале (название канала)"""
        return f"Youtube-канал: {self.title}"

    def __add__(self, other):
        """Суммирует количество подписчиков"""
        return int(self.subs_count) + int(other.subs_count)

    def __gt__(self, other):
        """Сравнивает количество подписчиков"""
        if isinstance(other, YouTubechennel):
            return int(self.subs_count) > int(other.subs_count)

    @property
    def channel_id(self):
        """Получение id канала"""
        return self.__ch_id

    @staticmethod
    def get_service():
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


class Video:

    def __init__(self, video_id):
        """Инициализация атрибутов класса"""
        self.video_id = video_id
        self.youtube = YouTubechennel.get_service()
        self.video = self.youtube.videos().list(id=self.video_id, part='snippet,statistics').execute()
        self.video_title = self.video['items'][0]['snippet']['title']  # название видео
        self.view_count = self.video['items'][0]['statistics']['viewCount']  # количество просмотров
        self.like_count = self.video['items'][0]['statistics']['likeCount']  # количество лайков

    def __str__(self) -> str:
        """Возвращает информацию о видео (название видео)"""
        return self.video_title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

        self.playlists = self.youtube.playlists().list(id=self.playlist_id, part='snippet').execute()
        self.playlist_title = self.playlists['items'][0]['snippet']['title']  # название видео

    def __str__(self) -> str:
        """Возвращает информацию о видео по шаблону: 'название_видео (название_плейлиста)'"""
        return f"{self.video_title} ({self.playlist_title})"
