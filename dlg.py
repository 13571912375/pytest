# coding:utf-8
# file: dlg.py

"""
Tkinter布局

pack 参数说明
fill -- x 横向填充（默认,各组件自上而下）， y竖向填充（各组件自左往右），both都填充
expand -- 1 父外框大小改变时，自动扩充大小，0为false
side -- left right top bottom 停靠在父组件的哪一边上
anchor -- 对齐方式

grid  参数说明
row -- 行号
rowspan -- 合并行
column -- 列号
columnspan -- 合并列
sticky -- 组件紧靠所在单元格的某一边角

grid填充（自动缩放）--同 pack的 expand属性
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
frame.grid(row=0, column=0, sticky="nsew")
"""


from Tkinter import *
from socket import *
from threading import *
from time import *

from datetime import *

__author__ = {'name': 'ldd',
              'mail': 'ldd@126.com',
              'blog': 'http://www.cnblogs.com/',
              'QQ': '12345678',
              'created': '2016-09-11'}

flag = 0
mutex = Lock()


class scrollTxtArea:
    def __init__(self, root):
        frame = Frame(root)
        frame.pack()
        self.textPad(frame)
        return

    def textPad(self, frame):
        # add a frame and put a text area into it
        textPad = Frame(frame)
        self.text = Text(textPad, height=20, width=60)

        # add a vertical scroll bar to the text area
        scroll = Scrollbar(textPad)
        self.text.configure(yscrollcommand=scroll.set)

        # pack everything
        self.text.pack(side=LEFT)
        scroll.pack(side=RIGHT, fill=Y)
        textPad.pack(side=TOP)
        return


class window:
    """docstring for ClassName"""
    def __init__(self):
        self.dlg = Tk()

        """menu setup"""
        menu = Menu(self.dlg)
        menu_sub = Menu(menu, tearoff=0)
        menu_sub.add_command(label="about...", command=self.menu_func_about)
        menu_sub.add_separator()
        menu_sub.add_command(label="quit...", command=self.menu_func_quit)
        menu.add_cascade(label="system...", menu=menu_sub)

        menu_sub = Menu(menu, tearoff=0)
        menu_sub.add_command(label="test1", command=self.menu_func_test1)
        menu_sub.add_separator()
        menu_sub.add_command(label="test2", command=self.menu_func_test2)
        menu.add_cascade(label="test...", menu=menu_sub)

        self.dlg.config(menu=menu)

        """ctrl setup"""
        self.label_recv = Label(self.dlg, text='recv')
        self.label_recv.pack()

        self.txt_box_recv = Text(self.dlg)
        self.txt_box_recv.pack()

        self.label_send = Label(self.dlg, text='send')
        self.label_send.pack()

        self.val_s = StringVar()
        self.txt_box_send = Entry(self.dlg, textvariable=self.val_s)
        self.txt_box_send.pack()

        self.val_btn = 0
        self.button_recv = Button(self.dlg, text='recv', command=self.on_recv)
        self.button_recv.pack(fill=X)

        self.button_send = Button(self.dlg, text='send', command=self.on_send)
        self.button_send.pack(fill=X)

        self.button_quit = Button(self.dlg, text='quit', command=self.on_quit)
        self.button_quit.pack(fill=X)

        """socket setup"""
        self.s = socket(AF_INET, SOCK_DGRAM)  # self.s.setblocking(False)
        self.s.settimeout(0.1)

        host = ""
        port = 9999
        self.s.bind((host, port))

        self.val_btn_r = 0
        self.val_btn_s = 0

    def on_recv(self):
        global flag

        if self.val_btn_r:
            self.val_btn_r = 0
        else:
            self.val_btn_r = 1
            """thread"""
            self.t = Thread(target=self.thread_function, args=(flag,))
            self.t.start()

        if mutex.acquire(1):
            flag = self.val_btn_r
            mutex.release()

    def thread_function(self, flag_q):
        self.txt_box_recv.insert(INSERT, 'thread start!' + '\n')
        global flag
        q = 0
        while True:
            if mutex.acquire(1):
                q = flag
                mutex.release()

            if not q:
                break

            try:
                buff, addr = self.s.recvfrom(1024)
            except:
                continue

            if buff:
                now = datetime.now()
                tm = now.strftime("%Y-%m-%d %H:%M:%S")
                self.txt_box_recv.insert(
                    INSERT, tm+' recv '+buff.decode('utf-8') + ' flag = '+str(flag) + ' from'+repr(addr)+'\n')
            else:
                sleep(0.1)
                continue
        self.txt_box_recv.insert(INSERT, 'thread quit!' + '\n')
        return

    def proc_send(self):
        host = "192.168.1.220"
        port = 8080
        addr = (host, port)
        data = self.val_s.get()
        self.s.sendto(data.encode('utf-8'), addr)

    def on_send(self):
        if self.val_btn_s:
            self.val_btn_s = 0
        else:
            self.val_btn_s = 1
            tm = Timer(5, self.proc_send)
            tm.start()

    def on_quit(self):
        if self.val_btn_r:
            messagebox.showinfo('info', 'recv still running!')
            return

        self.s.close()
        self.dlg.quit()

    def menu_func_about(self):
        messagebox.showinfo("info", "my test")

    def menu_func_quit(self):
        self.on_quit()

    def menu_func_test1(self):
        pass

    def menu_func_test2(self):
        pass

    def loop_main(self):
        self.dlg.title("netassis")
        # self.dlg.minsize(640, 480)
        # self.dlg.maxsize(640, 480)
        self.dlg.mainloop()

if __name__ == '__main__':
    win = window()
    win.loop_main()
