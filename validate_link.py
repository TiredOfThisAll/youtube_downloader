import yt_dlp as youtube_dl


ydl_opts = {
    'quiet': True,
    'ignoreerrors': True
}


def retrieve_video_info(url, login=''):
    if login:
        ydl_opts['cookiefile'] = 'cook_rdy.txt'
    info = youtube_dl.YoutubeDL(ydl_opts).extract_info(url, download=False)
    if info.get('_type') == 'playlist':
        return info.get('entries')
    return [info]


def check_valid_link_youtube(url, logger, repository, login=''):
    try:
        new_songs = []
        already_downloaded_songs = repository.get_list_of_downloaded_music()

        video_info = retrieve_video_info(url, login)
        for i in range(len(video_info)):
            if video_info[i]['title'] not in already_downloaded_songs:
                new_songs.append(video_info[i])
        if new_songs:
            print(f'Found {len(new_songs)} new songs to download')
            return new_songs
        return 'There is no new songs to be downloaded'

    except youtube_dl.DownloadError as e:
        logger.warning(e.args[0])
        return 'Invalid link or video unavailable'
    except Exception as e:
        logger.error(e)
        return 'Unexpected Error'
