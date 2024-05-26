import discord
import os
import requests
import tkinter as tk
from tkinter import messagebox
import tracemalloc
from threading import Thread
import hmac, base64, struct, hashlib, time, pyotp
import time
import datetime
import google.generativeai as genai


bot = discord.Bot(intents=discord.Intents.all())



totp = pyotp.TOTP(os.environ['Authenticator_key'])



equrl = ''
data = requests.get(equrl)
data_json = data.json()
eq = data_json['records']['Earthquake']



GMT = datetime.timezone(datetime.timedelta(hours=8))
start_time = time.time()



genai.configure(api_key=os.environ["GOOGLE_AI_KEY"])
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)
chat = model.start_chat(history=[])






class MyGUI:
    def __init__(self, root ):
        self.root = root
        self.root.title('Discord Bot GUI')
        self.root.geometry('960x540')
        
        
        current_time_label = tk.StringVar()
        runtime_label = tk.StringVar()
        sendchannel = tk.StringVar()
        message = tk.StringVar()
        
        
        canvas = tk.Canvas(root, width=960, height=540)
        canvas.create_line(0, 45, 958, 45, width=3)
        canvas.create_line(860, 0, 860 , 45, width=3)
        canvas.create_line(956, 0, 956 , 45, width=3)
        canvas.create_rectangle(860, 60, 956, 400, width=3)


        
        botopen = tk.StringVar()
        botopen.set("Bot:off      ") 


        
        aiopen = tk.StringVar()
        aiopen.set("AI:off      ") 


        
        mylabel = tk.Label(root, text="●",font=('Arial',20))
        mylabel1 = tk.Label(root, textvariable=botopen, font=('Arial',20))
        mylabel2 = tk.Label(root, textvariable=aiopen, font=('Arial',20))
        mylabel3 = tk.Label(root, textvariable=current_time_label, font=('Arial', 20))
        mylabel4 = tk.Label(root, text="run time", font=('Arial', 14))
        mylabel5 = tk.Label(root, textvariable=runtime_label, font=('Arial', 10))
        

        
        
        

        

        

        
        def showTime():
            now = datetime.datetime.now(tz=GMT).strftime('%H:%M') 
            current_time_label.set(now)  
            root.after(1000, showTime)

        def update_runtime():
            elapsed_time = time.time() - start_time  
            minutes, seconds = divmod(elapsed_time, 60)
            hours, minutes = divmod(minutes, 60)
            runtime_str = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
            runtime_label.set(runtime_str)
            root.after(1000, update_runtime)  

        

        
        @bot.event
        async def on_ready():
            activity = discord.Activity(
                type=discord.ActivityType.playing,  
                name="AI bot"  
            )
            await bot.change_presence(activity=activity)
            print(f"「{bot.user}」已登入")
            botopen.set("Bot:on     ")
            response = chat.send_message("你是一台Discord 機器人，你有一些設定，請勿違反設定"
                                         "如果有人問你是誰，以完整的句子告訴他你的名字叫AIBot,並加上一些自我介紹。"
                                         "如果你收到語意與伺服器有幾人?相近，輸出'member'。"
                                         "以上加上引號的文字輸出前後不可以加入任何文字。"
                                         "確認此設定後輸出'設定完畢'。")
            print(response.text)
            aiopen.set("AI:on     ")
            
        async def send():  # Updated send function to accept message argument
            if text1.get(1.0, 'end-1c') != None: # Check if message is not empty
                channel = bot.get_channel(int(sendchannel.get()))
                if channel is not None:
                    message=text1.get(1.0, 'end-1c')
                    await channel.send(message)
                else:
                    btn_showerror = tk.Button(root, text='showerror')
                    btn_showerror.pack()
            else:
                print("No message to send")  # Optional: Handle case when message is empty


        @bot.event
        async def on_message(message):
            if message.author == bot.user:
              return

            if message.content.startswith("!") or message.content.startswith("！"):
              response = "ERROR"

              response = chat.send_message(message.content[1:])
              if response.text == "member":
                member_count = len(message.channel.guild.members)
                await message.channel.send(f"伺服器人數：{member_count} 人")

              else:
                await message.channel.send(response.text)  




        @bot.command()
        async def earthquake(ctx):
            i = eq[0]
            loc = i['EarthquakeInfo']['Epicenter']['Location']
            val = i['EarthquakeInfo']['EarthquakeMagnitude']['MagnitudeValue']
            dep = i['EarthquakeInfo']['FocalDepth']
            eq_time = i['EarthquakeInfo']['OriginTime']
            img = i['ReportImageURI']
            msg = f'{loc}，芮氏規模 {val} 級，深度 {dep} 公里，發生時間 {eq_time}'
            await ctx.respond(msg)
            await ctx.respond(img)
        

        @bot.command()
        async def text(ctx,pin:str, message:str, 頻道id=None):
          code = totp.now()
          if totp.verify(pin):
            if 頻道id is not None:
              channel = bot.get_channel(int(頻道id))
              await channel.send(message)
            else:
              await ctx.send(message)
          else:
            await ctx.respond("驗證碼錯誤")

        entry1 = tk.Entry(root, textvariable=sendchannel,width=70)
        text1 = tk.Text(root, height=5)        
        Button1 = tk.Button(root,text='send',width=5,height=2, command=send,font=('Arial', 20,'bold'))


        
        canvas.place(x=0, y=0)

        mylabel.place(x=10, y=0)
        mylabel1.place(x=50, y=2)
        mylabel2.place(x=190, y=2)
        mylabel3.place(x=865, y=2)
        mylabel4.place(x=865, y=70)
        mylabel5.place(x=865, y=100)
        Button1.place(x=720, y=450)
        entry1.place(x=100, y=420)
        text1.place(x=100, y=450)


        



        
        showTime()
        update_runtime()

def run_tkinter():
    root = tk.Tk()
    gui = MyGUI(root)
    root.mainloop()
    

if __name__ == "__main__":

    tkinter_thread = Thread(target=run_tkinter)
    tkinter_thread.start()


    #bot.run(os.environ['bot_token']) 





