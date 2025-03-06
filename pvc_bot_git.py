import sys
import os
import threading  # 用來同時運行 Flask 和 Discord Bot
from flask import Flask
from responses123 import responses, responses2, responses3, responsesyan
from responsesGT import responsesG2, responsesP
#import nextcord as discord
import discord
from discord import app_commands
from discord.ext import commands
import random
import time
import requests
import asyncio

OCR_API_URL = 'https://api.ocr.space/parse/image'
OCR_API_KEY = 'K84485044288957'

# Flask 伺服器
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is active!", 200  # 確保返回 HTTP 200 狀態碼

def run_flask():
    port = int(os.environ.get("PORT", 5000))  # 讓 Render 取得 PORT 環境變數
    app.run(host='0.0.0.0', port=port)

# 啟用所需的 intents
intents = discord.Intents.default()
intents.message_content = True
intents.message_content = True
intents.members = True  # 需要讀取成員資訊

bot = commands.Bot(command_prefix="!", intents=intents)  # Initialize the bot instance

# 從環境變數讀取 DISCORD_TOKEN
TOKEN = os.environ.get("DISCORD_TOKEN")

@bot.event
async def on_ready():
    try:
        # 將斜線指令同步到伺服器
        slash = await bot.tree.sync()
        print(f"目前登入身份 --> {bot.user}", flush=True)
        print(f"載入 {len(slash)} 個斜線指令", flush=True)
    except Exception as e:
        print(f"Error syncing commands: {e}", flush=True)


# 创建一个字典来存储冷却状态
cooldowns = {}

###################################################

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # 防止 bot 自己回應自己的消息


    user_id = message.author.id

    # 檢查冷卻時間
    if user_id in cooldowns and time.time() - cooldowns[user_id] <= 0:
        return

    # 设置冷却时间2秒
    cooldowns[user_id] = time.time() + 1

    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
                
                # 等待 2 秒確保 Discord URL 可存取
                await asyncio.sleep(2)

                image_url = attachment.url
                response = requests.post(
                    OCR_API_URL,
                    data={
                        'apikey': OCR_API_KEY,
                        'url': image_url,
                        'language': 'cht',  # 修正為 'cht'（繁體中文）
                        'isOverlayRequired': False
                    }
                )

                result = response.json()
                print("API 回應結果:", result)  # Debug 用

                if 'ParsedResults' in result and len(result['ParsedResults']) > 0:
                    parsed_text = result['ParsedResults'][0]['ParsedText']
                    if parsed_text.strip():
                        await message.reply(f'{parsed_text}')

    if message.content == "!吃啥":

        # 隨機選擇一個回應
        response = random.choice(responses)
        # 引用輸入指令的人
        user = message.author
        await message.channel.send(f"{user.mention} {response}")

    if message.content == "!今日":

        # 隨機選擇一個回應
        response2 = random.choice(responses2)
        # 引用輸入指令的人
        user = message.author
        await message.channel.send(f"{user.mention} ||{response2}||")

    if message.content == "!Labrat":

        # 隨機選擇一個回應
        response3 = random.choice(responses3)
        # 引用輸入指令的人
        user = message.author
        await message.channel.send(f"{user.mention} 你說的對，但這就是最可愛的Labrat \n {response3}")


    if message.content == "!研究生":

        # 隨機選擇一個回應
        responseyan = random.choice(responsesyan)
        # 引用輸入指令的人
        user = message.author
        await message.channel.send(f"{user.mention} {responseyan}")

    await bot.process_commands(message)  # 確保其他指令仍然能夠正常工作




# 創建 /leg 指令，並為其添加自動補全
@bot.tree.command(name="雞腿語錄", description="搜尋語錄名稱")
@app_commands.describe(quote_name="輸入語錄名稱")
async def leg(interaction: discord.Interaction, quote_name: str):
    # 如果用戶輸入 "隨機"，則隨機返回一張圖片
    if quote_name == "隨機":
        random_image = random.choice(list(responsesG2.values()))
        await interaction.response.send_message(f"隨機語錄: {random_image}")
    else:
        # 根據輸入的圖片名稱搜尋並返回
        image_url = responsesG2.get(quote_name, None)
        
        if image_url:
            await interaction.response.send_message(f"雞腿語錄: {image_url}")
        else:
            await interaction.response.send_message("未找到對應的語錄，請再試一次！")

# 設置自動補全為異步函數，這裡是為 quote_name 參數提供補全選項
@leg.autocomplete("quote_name")
async def autocomplete_quote_name(interaction: discord.Interaction, current: str):
    # 根據用戶輸入進行過濾，並返回匹配的結果
    return [
        app_commands.Choice(name=name, value=name)
        for name in responsesG2.keys() if current.lower() in name.lower()
    ][:25]  # 顯示最多25個匹配的選項



# 創建 /PIC 指令，並為其添加自動補全
@bot.tree.command(name="圖", description="搜尋圖片名稱")
@app_commands.describe(image_name="輸入圖片名稱")
async def pic(interaction: discord.Interaction, image_name: str):
    # 如果用戶輸入 "隨機"，則隨機返回一張圖片
    if image_name == "隨機":
        random_image = random.choice(list(responsesP.values()))
        await interaction.response.send_message(f"{random_image}")
    else:
        # 根據輸入的圖片名稱搜尋並返回
        image_url = responsesP.get(image_name, None)
        
        if image_url:
            await interaction.response.send_message(f"{image_url}")
        else:
            await interaction.response.send_message("未找到對應的圖片名稱，請再試一次！")

# 設置自動補全為異步函數，這裡是為 image_name 參數提供補全選項
@pic.autocomplete("image_name")
async def autocomplete_image_name(interaction: discord.Interaction, current: str):
    # 根據用戶輸入進行過濾，並返回匹配的結果
    return [
        app_commands.Choice(name=name, value=name)
        for name in responsesP.keys() if current.lower() in name.lower()
    ][:25]  # 顯示最多25個匹配的選項

# 註冊斜線指令 /吃啥
@bot.tree.command(name="吃啥", description="不知道吃啥？讓我來幫你選！")
async def eat_what(interaction: discord.Interaction):
    choice = random.choice(responses)  # 隨機選擇一個選項
    await interaction.response.send_message(choice)

# 註冊斜線指令 /研究生
@bot.tree.command(name="研究生", description="給研究生一點暖心言語")
async def researcher(interaction: discord.Interaction):
    choice = random.choice(responsesyan)  # 隨機選擇一個選項
    await interaction.response.send_message(choice)

# 註冊斜線指令 /水豚
@bot.tree.command(name="水豚", description="看看療育水豚吧")
async def researcher(interaction: discord.Interaction):
    choice = random.choice(responses3)  # 隨機選擇一個選項
    await interaction.response.send_message(choice)

# 使用執行緒讓 Flask 和 Discord Bot 同時運行
if __name__ == "__main__":
    sys.stdout.flush()
    flask_thread = threading.Thread(target=run_flask)  # Flask 背景執行
    flask_thread.start()

    bot.run(TOKEN)  # 啟動 Discord Bot
