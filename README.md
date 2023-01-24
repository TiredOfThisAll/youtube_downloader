# youtube_downloader
There is an app to download videos from youtube.
Available commands: 

    /changefolder(downloads in project folder by default)
    /login if u want to download age-restricted content
    /converttompr3
    /exit
    
Requirements:
1. youtube_dl package
2. If you want to convert downloaded videos to mp3 you have to download FFmpeg
Youtube authorization guide:
Login into your youtube account and go to youtube.com. Then press f12 and find rows HSID, SID, SSID. Copy them into "my_cookie.txt" file and run application with /login command.
