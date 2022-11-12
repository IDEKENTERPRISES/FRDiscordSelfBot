import json
import discord
from discord.ext import tasks
import requests
from threading import Event, Thread


discordBotToken = '' # Insert discord selfbot token

inviteLink = "" # Insert invite link
frequency = 5 # seconds (The higher this is the higher the chance of getting the bot banned)

selfBot = discord.Client()


def call_repeatedly(interval, func, *args):
    stopped = Event()
    def loop():
        while not stopped.wait(interval):
            func(*args)
    Thread(target=loop).start()    
    return stopped.set

def checkFriends():
    headers = {
        'authority': 'discord.com',
        'accept': '*/*',
        'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8',
        'authorization': discordBotToken,
        'referer': 'https://discord.com/channels/@me',
        'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.34',
    }

    try:
        response = requests.get('https://discord.com/api/v9/users/@me/relationships', headers=headers)
        response = json.loads(response.content)
        for user in response:
            if user["type"] == 3:
                requests.put('https://discord.com/api/v9/users/@me/relationships/' + user["id"], headers=headers, json={})
                friendDM = requests.post('https://discord.com/api/v9/users/@me/channels', headers=headers, json={'recipients': [user["id"]]})
                dmID = json.loads(friendDM.content)["id"]
                print(dmID)
                requests.post('https://discord.com/api/v9/channels/'+dmID+'/messages', headers=headers, json={'content': inviteLink, 'tts': False})
    except:
        print("An error occured when trying to respond to friend requests.")

@selfBot.event
async def on_ready():
    print(f'We have logged in as {selfBot.user}')
    checkFriends()
    call_repeatedly(frequency, checkFriends)
    

    
selfBot.run(discordBotToken)