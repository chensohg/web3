import pyautogui as pg
import asyncio
import re,time,datetime
import random
from telethon import TelegramClient, events
import python_socks
import winsound

feedcodeIdx=0
api_id = 21571782  # 您的 API ID
api_hash = 'd573619f5e0d452384d0be04eb8ae526'  # 您的 API HASH
chat_ids=['verdacitygroup','VerdaCity_Group','Verda_City_VN','verdacity_IndoXchange']
words={'exchange','response'}

class App:
    id=0
    enable=False
    refx=0
    refy=0
    success=0
    failed=0
    lastTime=0

    def __init__(self,id,enable,refx,refy,success=0,failed=0):
        self.id=id
        self.enable=enable
        self.refx=refx
        self.refy=refy
        self.success=success
        self.failed=failed

    def print(self):
        print('%d--Succcess:%d,Failed:%d'%(self.id,self.success,self.failed))

def get_mouse_positon():
    screen_width, screen_height = pg.size()
    # 获取屏幕宽高
    print("屏幕宽度:", screen_width)
    print("屏幕高度:", screen_height)
    time.sleep(3) # 准备时间
    print('开始获取鼠标位置')
    try:
        while True:
            # Get and print the mouse coordinates.
            x, y = pg.position()
            positionStr = '鼠标坐标点（X,Y）为：{},{}'.format(str(x).rjust(4), str(y).rjust(4))
            pix = pg.screenshot().getpixel((x, y)) # 获取鼠标所在屏幕点的RGB颜色
            positionStr += ' RGB:(' + str(pix[0]).rjust(3) + ',' + str(pix[1]).rjust(3) + ',' + str(pix[2]).rjust(
                3) + ')'
            print(positionStr)
            time.sleep(1) # 停顿时间
    except:
        print('获取鼠标位置失败')

def autoclick(app:App,code):
    pg.click(x=app.refx, y=app.refy)
    time.sleep(0.2)
    usethebox_x=784
    usethebox_y=48
    #判断上一次的结果
    if app.lastTime>0:
        pix=pg.screenshot().getpixel((usethebox_x,usethebox_y))
        if 255*3-pix[0]-pix[1]-pix[2]>100:
            app.success=app.success+1
            if app.success>=15:
                app.enable=False
        else:
            app.failed=app.failed+1
            if app.failed>=10:
                app.enable=False
                print('Client %d Fail too many times'%app.id)
        app.print()
        diff=time.time()-app.lastTime
        if diff<5:
            print('(1)%f'%diff)
            time.sleep(5)
    #点击use the box
    pg.click(x=usethebox_x, y=usethebox_y)
    time.sleep(0.3)
    #输入code
    pg.tripleClick(x=usethebox_x, y=218)
    time.sleep(0.2)
    pg.write(code)
    time.sleep(0.2)
    #点击submit
    pg.click(x=usethebox_x, y=308)
    app.lastTime=time.time()


def tryCodes(codes,apps):
    global feedcodeIdx
    count=0
    maxTry=0
    random.shuffle(codes)

    for code in codes:
        if (not len(code) == 8) or (code.lower() in words):
            continue

        flag=False
        count=count+1
        for i in range(len(apps)):
            if apps[feedcodeIdx].enable:
                flag=True
                break
            feedcodeIdx=(feedcodeIdx+1)%len(apps)

        if flag:
            winsound.Beep(400,400)
            autoclick(apps[feedcodeIdx],code)
            print('client:%d-%s'%(feedcodeIdx+1,code))
            feedcodeIdx=(feedcodeIdx+1)%len(apps)
        else:
            print('========Finish 4 clients=========')
            exit(0)#没有enable了

        maxTry=maxTry+1
        if maxTry>=4:
            break

    if count>0:
        print('=================')


if __name__ == '__main__':
    user_input = input("查看坐标请输入1:")
    if user_input=='1':
        get_mouse_positon()
    else:
        app1=App(1,True,300,18)
        app2=App(2,True,490,18)
        app3=App(3,True,680,18)
        app4=App(4,True,870,18)
        apps=[app1,app2,app3,app4]
        opt_time=[0 for i in range(len(apps))]

        client = TelegramClient('session_name', api_id, api_hash,timeout=10,proxy=(python_socks.ProxyType.HTTP,'127.0.0.1',17890))
        @client.on(events.NewMessage(chats=chat_ids))
        async def my_event_handler(event):
            if event.message.message:  # 确保消息不为空
                try:
                    diff=time.time()-event.message.date.timestamp()
                    if diff>60:
                        print('give up:%s' % event.message.message)
                        return
                    #print('(0)%f'%diff)

                    split_text = re.split(r'\s+', event.message.message)
                    if event.message.message.lower().find('box')>=0:#带box
                        tryCodes(split_text,apps)
                    else:
                        #全是box code
                        flag=1
                        for code in split_text:
                            if not re.match(r'[0-9a-zA-Z]{8}',code):
                                flag=0
                                break
                        if flag:
                            tryCodes(split_text,apps)
                except Exception as e:
                    print(str(e))

        client.start()
        print('Listening...')
        client.run_until_disconnected()

