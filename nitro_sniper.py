try:
    from discord.ext import commands
    import time
    import httpx
    import discord
    import re
    import platform
    import os
    from colorama import Fore, Back, Style
except ImportError:
    os.system('pip install httpx discord.py==1.7.3')
    input()


intents = discord.Intents().all()
bot = commands.Bot(command_prefix='+', case_insensitive=True, self_bot=True, intents=intents)
codeRegex = re.compile("(discord.com/gifts/|discordapp.com/gifts/|discord.gift/)([a-zA-Z0-9]+)")

def clear():
    if platform.platform().startswith('Windows') == True:
        return os.system('cls')
    else:
        return os.system('clear')

token = input("Please enter your token for redeem nitro:")
clear()

bot.remove_command('help')

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    print("---------------------------------------------------")

@bot.event
async def on_message(message):
    if codeRegex.search(message.content):
        code = codeRegex.search(message.content).group(2)
        start_time = time.time()
        async with httpx.AsyncClient() as client:
            result = await client.post(
            'https://discordapp.com/api/v6/entitlements/gift-codes/' + code + '/redeem',
            headers={'authorization': token, 'user-agent': 'Mozilla/5.0'})
            delay = (time.time() - start_time)
            if 'This gift has been redeemed already' in str(result.content):
                print(Fore.YELLOW+f"[>] We found a code but it was redeemed already({code}, delay of {delay})")
            elif 'nitro' in str(result.content):
                print(Fore.GREEN+f"[>] We found a code and claimed it!({code}, delay of {delay})")
                time.sleep(26640)
            elif 'Unknown Gift Code' in str(result.content):
                print(Fore.RED+f"[>] We found a code but it was invalid!({code}, delay of {delay})")

bot.run(token, bot=False)