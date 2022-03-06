import configparser
import os
import sys
from tkinter import *


class gui:
    def __init__(self, master):
        self.mywindows = master
        self.password = StringVar()
        self.username = StringVar()
        self.saveuser = StringVar()
        self.autologin = StringVar()
        corrent_dir = os.path.dirname(os.path.realpath(sys.argv[0])) + os.sep
        self.configfile = os.path.join(corrent_dir, 'config.ini')
        self.readconfig()
        self.createpage()

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
        config.set('config', 'saveuser', '')
        config.set('config', 'autologin', '')
        config.write(open(self.configfile, 'w'))

    def login(self):
        pass
    def changeconfig(self):
        pass
    def createpage(self):
        frame = Frame(self.mywindows, width=320, height=380, pady=20, padx=20)
        frame.place(x=0, y=0)

        frame1 = Frame(frame, width=280, height=240)
        frame1.place(x=0, y=0)

        frame2 = Frame(frame1, width=208, height=49)
        frame2.place(x=36, y=0)

        canvas1 = Canvas(self.mywindows, width=25, height=25)
        image_file1 = PhotoImage(file='Images/qrcode.gif')
        image1 = canvas1.create_image(15, 0, anchor='n', image=image_file1)
        canvas1.place(x=285, y=10)

        canvas2 = Canvas(frame2, width=208, height=49)
        image_file2 = PhotoImage(file='Images/校园网认证登录.png')
        image2 = canvas2.create_image(104, 0, anchor='n', image=image_file2)
        canvas2.place(x=0, y=0)

        frame3 = Frame(frame1, width=280, height=30)
        frame3.place(x=0, y=49)

        label1 = Label(frame3, text='', padx=5, pady=5)
        label1.place(x=140, y=15, anchor='center')
        frame4 = Frame(frame1, width=280, height=170)
        frame4.place(x=0, y=79)

        frame5 = Frame(frame4, width=280, height=44, borderwidth=1, relief='solid')
        frame5.place(x=0, y=0)
        loginimg3 = PhotoImage(file='Images/loginimg.png')
        canvas3 = Canvas(frame5, width=42, height=38)
        image3 = canvas3.create_image(21, 0, anchor='n', image=loginimg3)
        canvas3.place(x=0, y=0)

        entry1 = Entry(frame5, textvariable=self.username, font=('Arial', 17))
        entry1.place(x=43, y=0, width=235, height=40)

        frame6 = Frame(frame4, width=280, height=44, borderwidth=1, relief='solid', highlightcolor='#00ffff')
        frame6.place(x=0, y=46)

        loginimg4 = PhotoImage(file='Images/loginimg.png')
        canvas4 = Canvas(frame6, width=42, height=38)
        image4 = canvas4.create_image(21, 0, anchor='n', image=loginimg4)
        canvas4.place(x=0, y=0)

        entry2 = Entry(frame6, textvariable=self.password, font=('Arial', 17), show='*')
        entry2.place(x=43, y=0, width=235, height=40)

        b1 = Button(frame4, text='连接', width=35, height=2, command=self.login, borderwidth=1,
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
