import configparser
import json
import os
import sys
import time
import tkinter

import requests

from loginweb import readconfig, is_internet, write_log, login


def login(username, password):
    # 定义post数据
    data = dict(qrCodeId='', username='', pwd='', validCode='', validCodeFlag='', ssid='', mac='', t='', wlanacname='',
                url='', nasip='', wlanuserip='')
    data['username'] = username
    data['pwd'] = password
    data['qrCodeId'] = '请输入编号'
    data['validCode'] = '验证码'
    data['validCodeFlag'] = 'false'
    try:
        first_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                      'like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47',
                        'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
        r = requests.get('http://www.baidu.com', headers=first_header)
        # print(r.headers)
        # print(r.request.headers)
    except:
        # print("r = requests.get('http://www.baidu.com') failed!")
        write_log("r = requests.get('http://www.baidu.com') failed!")
        return
    url = r.text.split('\'')[1]

    try:
        login = requests.get(url, headers=first_header)
    except:
        write_log("login = requests.get(url, headers=first_header) failed!")
        return

    attrlist = login.url.split('?')[-1].split('&')
    for i in range(0, len(attrlist)):
        key = attrlist[i].split('=')[0]
        value = attrlist[i].split('=')[1]
        if key in data.keys():
            data[key] = value

    header = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        # 'Content-Length': '451',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': '',
        'Host': '',
        'Origin': '',
        'Pragma': 'no-cache',
        'Referer': '',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.44',
        'X-Requested-With': 'XMLHttpRequest'

    }
    filecounter = 'failCounter=0'
    cookies = 'JSESSIONID=' + login.cookies.get_dict()['JSESSIONID'] + ': ' + filecounter
    header['Referer'] = login.url
    header['Cookie'] = cookies
    header['Host'] = login.url.split('/')[2]
    header['Origin'] = 'http://' + header['Host']

    loginurl = header['Origin'] + '/zportal/login/do'
    try:
        do = requests.post(loginurl, data=data, headers=header)
    except:
        print('login failed!')
        return
    datas = json.loads(do.text)
    if datas['result'] == 'success':
        # print('login success!')
        write_log('login success!')
    elif datas['result'] == 'online':
        # print(datas['message'])
        write_log(datas['message'])
    else:
        # print(datas['message'])
        write_log(datas['message'])


def readconfig():
    corrent_dir = os.path.dirname(os.path.realpath(sys.argv[0])) + os.sep
    configfile = os.path.join(corrent_dir, 'config.ini')
    config = configparser.ConfigParser()
    if not os.path.exists(configfile):
        createconfig(configfile)
    config.read(configfile, encoding="utf-8")
    username = config.get('user', 'username')
    password = config.get('user', 'password')
    saveuser = config.get('config', 'saveuser')
    autologin = config.get('config', 'autologin')
    return username, password, saveuser, autologin


def createconfig(configfile):
    config = configparser.ConfigParser()
    config.read(configfile, encoding="utf-8")
    config.add_section("user")
    config.set('user', 'username', '')
    config.set('user', 'password', '')
    config.add_section("config")
    config.set('config', 'saveuser', '')
    config.set('config', 'autologin', '')
    config.write(open(configfile, 'w'))


def changeconfig():
    corrent_dir = os.path.dirname(os.path.realpath(sys.argv[0])) + os.sep
    configfile = os.path.join(corrent_dir, 'config.ini')
    config = configparser.ConfigParser()
    if not os.path.exists(configfile):
        createconfig(configfile)
    config.read(configfile, encoding="utf-8")
    if CheckVar1.get == 1:
        config.set('config', 'saveuser', 'true')
    else:
        config.set('config', 'saveuser', 'false')
    if CheckVar2.get == 1:
        config.set('config', 'autologin', 'true')
    else:
        config.set('config', 'autologin', 'false')
    config.write(open(configfile, 'w'))


def gui(username='', password='', saveuser='', autologin=''):
    un = username
    pw = password
    su = saveuser
    al = autologin
    mywindows = tkinter.Tk()
    mywindows.title('connect compus network')
    mywindows.geometry('320x380')
    mywindows.resizable(0, 0)

    frame = tkinter.Frame(mywindows, width=320, height=380, pady=20, padx=20)
    frame.place(x=0, y=0)

    frame1 = tkinter.Frame(frame, width=280, height=240)
    frame1.place(x=0, y=0)

    frame2 = tkinter.Frame(frame1, width=208, height=49)
    frame2.place(x=36, y=0)

    canvas1 = tkinter.Canvas(mywindows, width=25, height=25)
    image_file1 = tkinter.PhotoImage(file='Images/qrcode.gif')
    image1 = canvas1.create_image(15, 0, anchor='n', image=image_file1)
    canvas1.place(x=285, y=10)

    canvas2 = tkinter.Canvas(frame2, width=208, height=49)
    image_file2 = tkinter.PhotoImage(file='Images/校园网认证登录.png')
    image2 = canvas2.create_image(104, 0, anchor='n', image=image_file2)
    canvas2.place(x=0, y=0)

    frame3 = tkinter.Frame(frame1, width=280, height=30)
    frame3.place(x=0, y=49)

    label1 = tkinter.Label(frame3, text='', padx=5, pady=5)
    label1.place(x=140, y=15, anchor='center')
    frame4 = tkinter.Frame(frame1, width=280, height=170)
    frame4.place(x=0, y=79)

    frame5 = tkinter.Frame(frame4, width=280, height=44, borderwidth=1, relief='solid')
    frame5.place(x=0, y=0)
    loginimg3 = tkinter.PhotoImage(file='Images/loginimg.png')
    canvas3 = tkinter.Canvas(frame5, width=42, height=38)
    image3 = canvas3.create_image(21, 0, anchor='n', image=loginimg3)
    canvas3.place(x=0, y=0)

    inputuser = tkinter.StringVar()
    inputpass = tkinter.StringVar()

    inputuser.set(un)
    inputpass.set(pw)
    entry1 = tkinter.Entry(frame5, textvariable=inputuser, font=('Arial', 17))
    entry1.place(x=43, y=0, width=235, height=40)

    frame6 = tkinter.Frame(frame4, width=280, height=44, borderwidth=1, relief='solid', highlightcolor='#00ffff')
    frame6.place(x=0, y=46)

    loginimg4 = tkinter.PhotoImage(file='Images/loginimg.png')
    canvas4 = tkinter.Canvas(frame6, width=42, height=38)
    image4 = canvas4.create_image(21, 0, anchor='n', image=loginimg4)
    canvas4.place(x=0, y=0)

    entry2 = tkinter.Entry(frame6, textvariable=inputpass, font=('Arial', 17), show='*')
    entry2.place(x=43, y=0, width=235, height=40)

    b1 = tkinter.Button(frame4, text='连接', width=35, height=2, command=login(inputuser, inputpass), borderwidth=1,
                        relief='solid', bg='#05a', fg='#fff')
    b1.place(x=140, y=135, anchor='center')

    CheckVar1 = tkinter.IntVar()
    CheckVar2 = tkinter.IntVar()
    # 设置三个复选框控件，使用variable参数来接收变量
    if su == 'true':
        CheckVar1.set(1)
    if al == 'true':
        CheckVar2.set(1)
    check1 = tkinter.Checkbutton(mywindows, text="记住密码", font=('宋体', 15, 'bold'), command=changeconfig, variable=CheckVar1, onvalue=1,
                                 offvalue=0)
    check2 = tkinter.Checkbutton(mywindows, text="自动登录", font=('宋体', 15, 'bold'), command=changeconfig, variable=CheckVar2, onvalue=1,
                                 offvalue=0)
    check1.place(x=10, y=340)
    check2.place(x=200, y=340)

    mywindows.mainloop()


if __name__ == '__main__':
    username, password, saveuser, autologin = readconfig()
    gui(username, password, saveuser, autologin)
