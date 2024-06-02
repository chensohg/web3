import pyautogui as pg
import re,time,datetime
import schedule
import subprocess
import psutil

feedcodeIdx=0
succeedtimes=0
failedtimes=0

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

def autoclick():
    global succeedtimes
    global failedtimes

    pg.click(x=1134, y=501)#close success dialog,不管有没有点一下，防止点不了
    time.sleep(1)

    print('click stage 1')
    pg.click(x=788, y=463)#send
    time.sleep(3)

    pg.click(x=1405, y=288)#>
    time.sleep(1)

    pg.click(x=1405, y=332)#usdc
    time.sleep(1)

    pg.click(x=1394, y=403)#address
    time.sleep(1)

    pg.click(x=1301, y=267)#address
    time.sleep(1)

    pg.click(x=549, y=521)#amount
    time.sleep(1)
    pg.typewrite('0.01',0.05)#没有间隔时间，容易乱序
    time.sleep(1)

    print('click stage 2')
    pg.click(x=901, y=976)#buttom send
    time.sleep(15)#show gas

    pg.click(x=909, y=708)#gas dialog send
    time.sleep(20)

    #pg.click(x=909, y=648)#VERIFY 有时候是自动的
    #time.sleep(10)
    print('click stage 3')

    pix=pg.screenshot().getpixel((1786, 520))
    while pix[0]+pix[1]+pix[2]<350:
        pg.click(x=1786, y=520)#jam
        time.sleep(1)
        failedtimes=failedtimes-1
        print('hit histroy')
        pix=pg.screenshot().getpixel((1786, 520))

    pix=pg.screenshot().getpixel((1828, 560))
    if pix[0]+pix[1]+pix[2]>350:#white
        pg.click(x=1179,y=427)#close gas dialog
        failedtimes=failedtimes+1
        time.sleep(1)
        pg.click(x=507,y=212)#back
        print('hit failed:%d'%(pix[0]+pix[1]+pix[2]))
        return
    else:
        #print('hit succeed')
        pg.click(x=1828, y=560)#metamask
        time.sleep(15)

    print('click stage 4')
    pix=pg.screenshot().getpixel((835,645))
    if pix[0]+pix[1]+pix[2]<100:
        succeedtimes=succeedtimes+1
        pg.click(x=1134, y=501)#close
    else:
        failedtimes=failedtimes+1
        pg.click(x=507,y=212)#back


def job():
    time.sleep(5)
    while succeedtimes<100 and failedtimes<10:
        autoclick()
        time.sleep(10)
        print(time.strftime("%a %b %d %H:%M:%S %Y",time.localtime()))
        print("succees:%d;failed:%d"%(succeedtimes,failedtimes))


def close_chrome_process():
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == 'chrome.exe':
            process.kill()

def start():
    #close_chrome_process()

    pg.hotkey('win', 'd')
    time.sleep(5)
    #call chrome
    # 假设你的exe文件名为example.exe，位于当前目录下
    exe_path = "C:/Users/Administrator/AppData/Local/Google/Chrome/Application/chrome.exe"
    
    # 使用subprocess.run来调用exe文件
    result = subprocess.run([exe_path], capture_output=True, text=True)
    time.sleep(10)
    #enter url
    pg.tripleClick(443,62)
    url='https://pioneer.particle.network/zh-CN/point'
    pg.typewrite(url,0.05)
    pg.press('enter')
    time.sleep(20)
    #click walllet
    pg.click(1857,974)
    time.sleep(10)
    pg.click(1518,318)
    time.sleep(5)


if __name__ == '__main__':
    user_input = input("查看坐标请输入1:")
    if user_input=='1':
        get_mouse_positon()
    elif user_input=='2':
        #job()
        start()
    else:        
        schedule.every().day.at("14:09").do(job)
        
        while True:
            schedule.run_pending()
            time.sleep(10)