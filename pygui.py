import configparser
import json
import os
import sys
import urllib
from tkinter import *
from urllib.request import urlopen

import requests


class gui:
    def __init__(self, master):
        self.mywindows = master
        self.message = StringVar()
        self.password = StringVar()
        self.username = StringVar()
        self.saveuser = StringVar()
        self.autologin = StringVar()
        corrent_dir = os.path.dirname(os.path.realpath(sys.argv[0])) + os.sep
        self.configfile = os.path.join(corrent_dir, 'config.ini')
        self.readconfig()
        self.createpage()
        if self.autologin.get() == 'true':
            self.connect()

    def readconfig(self):
        config = configparser.ConfigParser()
        if not os.path.exists(self.configfile):
            self.createconfig()
        config.read(self.configfile, encoding="utf-8")
        self.username.set(config.get('user', 'username'))
        self.password.set(config.get('user', 'password'))
        self.saveuser.set(config.get('config', 'saveuser'))
        self.autologin.set(config.get('config', 'autologin'))

    def createconfig(self):
        config = configparser.ConfigParser()
        config.read(self.configfile, encoding="utf-8")
        config.add_section("user")
        config.set('user', 'username', '')
        config.set('user', 'password', '')
        config.add_section("config")
        config.set('config', 'saveuser', 'false')
        config.set('config', 'autologin', 'false')
        config.write(open(self.configfile, 'w'))

    def is_internet(self):
        """
        Query internet using python
        :return:
        """
        try:
            urlopen('https://www.baidu.com', timeout=1)
            return True
        except urllib.error.URLError as Error:
            return False

    def connect(self):
        if self.is_internet():
            self.message.set('Network connection is ok!')
        elif self.username.get() == '' or self.password.get() == '':
            self.message.set('No username or password!')
            # print('no network!')
        else:
            self.message.set('No network, connecting!')
            self.login()

    def login(self):
        # 定义post数据
        data = dict(qrCodeId='', username='', pwd='', validCode='', validCodeFlag='', ssid='', mac='', t='',
                    wlanacname='',
                    url='', nasip='', wlanuserip='')
        data['username'] = self.username.get()
        data['pwd'] = self.password.get()
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
            self.message.set("request www.baidu.com failed!")
            return
        url = r.text.split('\'')[1]

        try:
            login = requests.get(url, headers=first_header)
        except:
            self.message.set("request access page failed!")
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
            self.message.set('login success!')
        elif datas['result'] == 'online':
            # print(datas['message'])
            self.message.set(datas['message'])
        else:
            # print(datas['message'])
            self.message.set(datas['message'])
    def changeconfig(self):
        config = configparser.ConfigParser()
        config.read(self.configfile, encoding="utf-8")
        if self.saveuser.get() == 'true':
            config.set('user', 'username', self.username.get())
            config.set('user', 'password', self.password.get())
        else:
            config.set('user', 'username', '')
            config.set('user', 'password', '')
        config.set('config', 'saveuser', self.saveuser.get())
        config.set('config', 'autologin', self.autologin.get())
        config.write(open(self.configfile, 'w'))
    def createpage(self):
        frame = Frame(self.mywindows, width=320, height=380, pady=20, padx=20)
        frame.place(x=0, y=0)

        frame1 = Frame(frame, width=280, height=240)
        frame1.place(x=0, y=0)

        frame2 = Frame(frame1, width=208, height=49)
        frame2.place(x=36, y=0)

        canvas1 = Canvas(self.mywindows, width=25, height=25)
        canvas1.image_file1 = PhotoImage(file='Images/qrcode.gif')
        image1 = canvas1.create_image(15, 0, anchor='n', image=canvas1.image_file1)
        canvas1.place(x=285, y=10)

        canvas2 = Canvas(frame2, width=208, height=49)
        canvas2.image_file2 = PhotoImage(file='Images/校园网认证登录.png')
        image2 = canvas2.create_image(104, 0, anchor='n', image=canvas2.image_file2)
        canvas2.place(x=0, y=0)

        frame3 = Frame(frame1, width=280, height=30)
        frame3.place(x=0, y=49)

        label1 = Label(frame3, textvariable=self.message, padx=5, pady=5)
        label1.place(x=140, y=15, anchor='center')
        frame4 = Frame(frame1, width=280, height=170)
        frame4.place(x=0, y=79)

        frame5 = Frame(frame4, width=280, height=44, borderwidth=1, relief='solid')
        frame5.place(x=0, y=0)
        canvas3 = Canvas(frame5, width=42, height=38)
        canvas3.loginimg3 = PhotoImage(file='Images/username.gif')

        image3 = canvas3.create_image(21, 0, anchor='n', image=canvas3.loginimg3)
        canvas3.place(x=0, y=0)

        entry1 = Entry(frame5, textvariable=self.username, font=('Arial', 17))
        entry1.place(x=43, y=0, width=235, height=40)

        frame6 = Frame(frame4, width=280, height=44, borderwidth=1, relief='solid', highlightcolor='#00ffff')
        frame6.place(x=0, y=46)
        canvas4 = Canvas(frame6, width=42, height=38)
        canvas4.loginimg4 = PhotoImage(file='Images/password.gif')

        image4 = canvas4.create_image(21, 0, anchor='n', image=canvas4.loginimg4)
        canvas4.place(x=0, y=0)

        entry2 = Entry(frame6, textvariable=self.password, font=('Arial', 17), show='*')
        entry2.place(x=43, y=0, width=235, height=40)

        b1 = Button(frame4, text='连接', width=35, height=2, command=self.connect, borderwidth=1,
                    relief='solid', bg='#05a', fg='#fff')
        b1.place(x=140, y=135, anchor='center')

        check1 = Checkbutton(self.mywindows, text="记住密码", font=('宋体', 15, 'bold'), command=self.changeconfig,
                             variable=self.saveuser, onvalue='true',
                             offvalue='false')
        check2 = Checkbutton(self.mywindows, text="自动登录", font=('宋体', 15, 'bold'), command=self.changeconfig,
                             variable=self.autologin, onvalue='true',
                             offvalue='false')
        check1.place(x=10, y=340)
        check2.place(x=200, y=340)


if __name__ == '__main__':
    root = Tk()
    root.title('connect compus network')
    root.geometry('320x380')
    root.resizable(0, 0)
    gui(root)
    root.mainloop()
