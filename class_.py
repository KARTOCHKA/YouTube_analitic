from googleapiclient.discovery import build
from dotenv import load_dotenv
from datetime import timedelta
from abc import ABC, abstractmethod
import os
import json
import datetime
import isodate as isodate


class MixinLog(ABC):
    def __init__(self):
        """Получение данных о ютуб-канале по его ID и ключу"""
        load_dotenv()
        api_key: str = os.getenv('YT_API_KEY')  # получение ключа из файла .env
        self.youtube = build('youtube', 'v3', developerKey=api_key)

    @abstractmethod
    def __str__(self):
        pass


class YouTubechennel(MixinLog):
    def __init__(self, ch_id):
        self.__ch_id = ch_id
        super().__init__()
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


class Video(MixinLog):

    def __init__(self, video_id):
        """Инициализация атрибутов класса"""
        self.video_id = video_id
        super().__init__()
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


class PlayList(MixinLog):

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        """Получение данных о плейлисте по ID и ключу ютуб-канала"""
        super().__init__()
        self.playlists_data = self.youtube.playlists().list(id=self.playlist_id, part='snippet').execute()
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id, part='contentDetails',
                                                                 maxResults=50).execute()
        self.playlist_title = self.playlists_data['items'][0]['snippet']['title']  # название плейлиста
        self.playlist_url = f"https://www.youtube.com/playlist?list={self.playlist_id}"  # url плейлиста

    @property
    def total_duration(self) -> datetime.timedelta:
        """Возвращает суммарную длительность плейлиста """
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        video_response = self.youtube.videos().list(part='contentDetails, statistics', id=','.join(video_ids)).execute()
        total_duration = timedelta()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self) -> str:
        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        video_response = self.youtube.videos().list(part='snippet,statistics', id=','.join(video_ids)).execute()
        best_video = None
        max_likes = 0
        for video in video_response['items']:
            if isinstance(int(video['statistics']['likeCount']), int):
                if int(video['statistics']['likeCount']) > max_likes:
                    best_video = video
                    max_likes = int(video['statistics']['likeCount'])
        return f'https://youtu.be/{best_video["id"]}'

    def __str__(self) -> str:
        """Возвращает информацию о плейлисте в формате: название - ссылка на плейлист)"""
        return f'{self.playlist_title} - {self.playlist_url}'
