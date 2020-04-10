import os
import pytube
import config
from moviepy.editor import *
from telethon import TelegramClient, events, Button
import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',level=logging.WARNING)

api_id = config.api_id
api_hash = config.api_hash
bot_token = config.bot_token

def Download(url):
    # download a song from a given url
    yt = pytube.YouTube(url).streams.filter().all()[0]
    print('Downloading {}'.format(yt.title))
    yt.download(filename='song')
    video = VideoFileClip('song.mp4')
    video.audio.write_audiofile(yt.title+'.mp3')
    print('done!')
    return yt.title

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@bot.on(events.NewMessage(pattern='/start'))
async def handler(event):
    async with bot.conversation(event.chat, timeout=None) as conv:
        await conv.send_message('Hi I will download any youtube audio file you wish in mp3 format')
        while True:
                await conv.send_message('Please choose one of the buttons', buttons=[Button.text('Download a song',resize=True), Button.text('Download a playlist')])
                ans = await conv.get_response()
                if ans.text == 'Download a song':
                    try:
                        await conv.send_message('Please send me a youtube link to the song')
                        link = await conv.get_response()
                        await conv.send_message('Downloading... this may take some time')
                        link = link.text
                        title = Download(str(link))
                        await conv.send_file(title+'.mp3')
                        os.remove(title+'.mp3')
                        os.remove('song.mp4')
                    except Exception as e:
                        print(e)
                        await conv.send_message("error... please make sure you insert a correct url")
                elif ans.text == "Download a playlist":
                    try:
                        await conv.send_message('Please send me a youtube link to the playlist')
                        link = await conv.get_response()
                        await conv.send_message('Downloading... this may take some time')
                        link = link.text
                        pl = pytube.Playlist(link)
                        pl.download_all('playlists/')
                        for song in os.listdir('playlists/'):
                            old_file = os.path.join('playlists', song)
                            new_file = os.path.join('playlists', song[1:])
                            os.rename(old_file, new_file)
                        for song in os.listdir('playlists/'):
                            print(song)
                            video = VideoFileClip('playlists/'+song)
                            video.audio.write_audiofile('playlists/'+song.replace(".mp4","")+'.mp3')
                            await conv.send_file('playlists/'+song.replace(".mp4","")+'.mp3')
                            os.remove('playlists/'+song.replace(".mp4","")+'.mp3')
                            os.remove('playlists/'+song)
                    except Exception as e:
                        print(e)
                        await conv.send_message("error... please make sure you insert a correct url")
bot.run_until_disconnected()
