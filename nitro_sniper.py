try:
    from discord.ext import commands
    import time
    import datetime
    import requests
    import httpx
    import discord
    import re
    import platform
    import json
    import os
    from colorama import Fore, Back, Style
except ImportError:
    os.system('pip install httpx discord.py==1.7.3 requests')
    input()


intents = discord.Intents().all()
bot = commands.Bot(command_prefix='+', case_insensitive=True, self_bot=True, intents=intents)
codeRegex = re.compile("(discord.com/gifts/|discordapp.com/gifts/|discord.gift/)([a-zA-Z0-9]+)")

with open('config.json') as f:
    config = json.load(f)
    giveaway_sniper = config.get('giveaway_sniper')
    token = config.get('token')
    edelay = config.get("delay_enabled")
    delay = config.get("delay")
    giveaway_sniper = config.get('giveaway_sniper')
    webhooknotification = config.get('webhook_notification')
    webhook = config.get('webhook')
    botlist = config.get('bot_list')

def clear():
    if platform.platform().startswith('Windows') == True:
        return os.system('cls')
    else:
        return os.system('clear')

clear()

bot.remove_command('help')

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    print("---------------------------------------------------")

@bot.event
async def on_message(message):
    def GiveawayInfo(elapsed):
        print(
            f"{Fore.LIGHTBLACK_EX} Server: {Fore.WHITE}{message.guild}"
            f"\n{Fore.LIGHTBLACK_EX} Channel: {Fore.WHITE}{message.channel}"
            f"\n{Fore.LIGHTBLACK_EX} Elapsed: {Fore.WHITE}{elapsed}s"
            + Fore.RESET)
    def GiveawayDelayInfo():
        print(
            f"{Fore.LIGHTBLACK_EX} Server: {Fore.WHITE}{message.guild}"
            f"\n{Fore.LIGHTBLACK_EX} Channel: {Fore.WHITE}{message.channel}"
            + Fore.RESET)
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
                message_content = "No content"
                data = {
                        "embeds": [{
                            "title": "Nitro Claimed",
                            "description": f"**Message content**:\n {message_content}\n**Server**: `{message.guild}`\n**Channel**: `#{message.channel}`\n**Author**: `{message.author.name}`",
                            "url": message.jump_url,
                            "color": 3407667
                            }],
                            "username": f"Sniper | {bot.user.name}#{bot.user.discriminator}",
                            "avatar_url": str(bot.user.avatar_url)
                            }
                requests.post(webhook, json=data)
                time.sleep(26640)
            elif 'Unknown Gift Code' in str(result.content):
                print(Fore.RED+f"[>] We found a code but it was invalid!({code}, delay of {delay})")

    if message.content or message.embeds and message.guild:
        if giveaway_sniper:
            if message.author.id in botlist and not (f'@{bot.user.id}' in message.content or f'<@{bot.user.id}>' in message.content) and not ("Giveaway ended" in message.content or "Congratulations" in message.content):
                start = datetime.datetime.now()
                try:
                    if not edelay:
                        await message.add_reaction("🎉")
                        elapsed = datetime.datetime.now() - start
                        elapsed = f'{elapsed.seconds}.{elapsed.microseconds}'
                except discord.errors.Forbidden:
                    print(""
                          f"\n{Fore.RED}{time} - Couldn't React to Giveaway" + Fore.RESET)
                    GiveawayInfo(elapsed)
                if edelay:
                    print(""
                          f"\n{Fore.GREEN}{time} - Giveaway Found!" + Fore.RESET)
                    GiveawayDelayInfo()
                else:
                    print(""
                          f"\n{Fore.GREEN}{time} - Giveaway Sniped" + Fore.RESET)
                    GiveawayInfo(elapsed)
                try:
                    if edelay:
                        time.sleep(5)
                        try:
                            await message.add_reaction("🎉")
                        except:
                            print("Error adding reaction")
                        print("")
                        print(f"{Fore.GREEN}Giveaway Sniped")
                except discord.errors.Forbidden:
                    print(""
                          f"\n{Fore.RED}{time} - Couldn't React to Giveaway" + Fore.RESET)
                    GiveawayInfo(elapsed)
                if webhooknotification:
                    if message.content and message.embeds:
                        message_content = "`" + message.content.replace("`", "").replace("\\", "")[:500] + "`" + "\n" + "***Message Embed***: " + "`" + str(message.embeds[0].title) + "\n" + str(message.embeds[0].description).replace("`", "").replace("\\", "")[:500] + "`"
                    elif message.embeds and not message.content:
                        message_content = "Empty Message\n" + "***Message Embed***: " + "`" + str(message.embeds[0].title) + "\n" + str(message.embeds[0].description).replace("`", "").replace("\\", "")[:500] + "`"
                    elif message.content and not message.embeds:
                        message_content = "`" + message.content.replace("`", "").replace("\\", "")[:500] + "`"
                    else:
                        message_content = "No content"
                    data = {
                        "embeds": [{
                            "title": "Giveaway Joined!",
                            "description": f"**Message content**:\n {message_content}\n**Giveaway Server**: `{message.guild}`\n**Channel**: `#{message.channel}`\n**Bot**: `{message.author.name}`",
                            "url": message.jump_url,
                            "color": 3407667
                            }],
                            "username": f"Sniper | {bot.user.name}#{bot.user.discriminator}",
                            "avatar_url": str(bot.user.avatar_url)
                            }
                    requests.post(webhook, json=data)
        else:
            return
    if f'@{bot.user.id}' in message.content or f'<@{bot.user.id}>' in message.content:
        if giveaway_sniper:
            if message.author.id in botlist:
                print(""
                      f"\n{Fore.GREEN}{time} - Giveaway Won" + Fore.RESET)
                elapsed = "-"
                GiveawayInfo(elapsed)
                if webhooknotification:
                    if message.content and message.embeds:
                        message_content = "`" + message.content.replace("`", "").replace("\\", "")[:500] + "`" + "\n" + "***Message Embed***: " + "`" + str(message.embeds[0].title) + "\n" + str(message.embeds[0].description).replace("`", "").replace("\\", "")[:500] + "`"
                    elif message.embeds and not message.content:
                        message_content = "Empty Message\n" + "***Message Embed***: " + "`" + str(message.embeds[0].title) + "\n" + str(message.embeds[0].description).replace("`", "").replace("\\", "")[:500] + "`"
                    elif message.content and not message.embeds:
                        message_content = "`" + message.content.replace("`", "").replace("\\", "")[:500] + "`"
                    else:
                        message_content = "No content"
                    data = {
                        "embeds": [{
                            "title": "Giveaway Won!",
                            "description": f"**Message content**:\n {message_content}\n**Giveaway Server**: `{message.guild}`\n**Channel**: `#{message.channel}`",
                            "url": message.jump_url,
                            "color": 16732345
                            }],
                            "username": f"Sniper | {bot.user.name}#{bot.user.discriminator}",
                            "avatar_url": str(bot.user.avatar_url)
                            }
                    requests.post(webhook, json=data)
        else:
            return
    await bot.process_commands(message)

bot.run(token, bot=False)