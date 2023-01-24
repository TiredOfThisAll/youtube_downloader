from __future__ import unicode_literals
import youtube_dl
import sqlite3
from os import path

from validate_link import check_valid_link_youtube
from my_logger import MyLogger
from repository import Repository
from process_cookie import cook_redy


DATABASE_PATH = 'D:/PycharmProjects/youtube_download_playlist/my.db'
SAVE_PATH = ''
FINISHED = False


def my_hook(d):
    if d['status'] == 'finished':
        filename = d['filename']
        if SAVE_PATH in filename:
            filename = filename.replace(SAVE_PATH, '')
        print(f'The file {filename} was downloaded now converting...')
        logger.info(f'The file {filename} was downloaded')
        global FINISHED
        FINISHED = True


logger = MyLogger()

repository = Repository(sqlite3.connect(DATABASE_PATH))
repository.create_schema()
repository.commit()

ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
    'ignoreerrors': True,
    'no_warnings': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
    'logger': logger,
    'progress_hooks': [my_hook],
}

print("""There is an app to download music from youtube.
    Available commands: /exit
    /changefolder(downloads in project folder by default)
    /login if u want to download age-restricted content
    /converttompr3""")

try:
    while True:
        url = input('Type url you want to download: ')

        if url.startswith('/exit'):
            exit()
        elif url.startswith('/changefolder'):
            SAVE_PATH = input('Type path here: ')
            continue
        elif url.startswith('/login'):
            cook_redy('my_cookie.txt')
            ydl_opts['cookiefile'] = 'cook_rdy.txt'
            continue
        elif url.startswith('/converttomp3'):
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }]
        error = check_valid_link_youtube(url, logger, repository)
        if error == 'Invalid link or video unavailable':
            print(error + ' URL: ' + url)
            logger.info(error + ' URL: ' + url)
            continue
        if error == 'There is no new songs to be downloaded':
            print(error + ' URL: ' + url)
            logger.info(error + ' URL: ' + url)
            continue
        if error == 'Unexpected Error':
            print(error)
            logger.error(error)
            continue

        video_info = error

        for i in range(len(video_info)):
            if SAVE_PATH:
                ydl_opts['outtmpl'] = path.join(SAVE_PATH, video_info[i]['title'] + '.mp3')
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_info[i]['webpage_url']])

        if FINISHED:
            for i in range(len(video_info)):
                repository.insert_downloaded_music(video_info[i]['title'], video_info[i]['webpage_url'])
                repository.commit()
            FINISHED = False
except Exception as e:
    logger.error(e)
