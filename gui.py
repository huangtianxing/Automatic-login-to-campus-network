import tkinter

from loginweb import readconfig, is_internet, write_log, login


def connect():
    username, password = readconfig()
    # if is_internet():
    #     l5.configure(text='Network connection is ok!')
    if username == '' or password == '':
        l5.configure(text='No username or password!')
    else:
        l5.configure(text='No network, connecting!')


mywindows = tkinter.Tk()
mywindows.title('connect compus network')
mywindows.geometry('400x360')

canvas = tkinter.Canvas(mywindows, width=400, height=135, bg='green')
canvas.pack(side = 'top')
tkinter.Label(mywindows, text='Wellcome',font=('Arial', 16)).pack()
tkinter.Label(mywindows, text='User name:', font=('Arial', 14)).place(x=15, y=175)
tkinter.Label(mywindows, text='password:', font=('Arial', 14)).place(x=15, y=215)
username, password = readconfig()
l3 = tkinter.Label(mywindows, text=username, font=('Arial', 14))
l3.place(x=125, y=175)
l4 = tkinter.Label(mywindows, text=username, font=('Arial', 14))
l4.place(x=125, y=215)
b1 = tkinter.Button(mywindows, text='连接', command = connect)
b1.place(x=10, y=245)
l5 = tkinter.Label(mywindows, text='')
l5.place(x=200, y=300)

mywindows.mainloop()
