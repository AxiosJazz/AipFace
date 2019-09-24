"""
调用百度AIP接口
实现人脸识别以及颜值打分
使用tkinter模块
设计简单的GUI界面（很简陋）
"""
from tkinter import *
from tkinter import filedialog # 实现路径选择
from PIL import Image, ImageTk # 实现在tkinter中显示图片
from aip import AipFace # 百度AIP接口
import base64

# 窗口对象
class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        pass

    #初始化窗口对象
    def init_window(self):
        self.master.title("AipFace")
        self.pack(fill=BOTH, expand=1)

        # 实例化一个Menu对象，这个在主窗体添加一个菜单
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # 创建File菜单，下面有Save和Exit两个子菜单
        file = Menu(menu)
        file.add_command(label='Select', command=self.selectPath)
        file.add_command(label='Exit', command=self.client_exit)
        menu.add_cascade(label='File', menu=file)

        # 创建Edit菜单，下面有一个Undo菜单
        edit = Menu(menu)
        edit.add_command(label='Undo')
        edit.add_command(label='Show Image', command=self.showImg)
        edit.add_command(label='Show Result', command=self.showResult)
        menu.add_cascade(label='Edit', menu=edit)
        pass

    # 选择图片文件
    def selectPath(_):
        global path_
        path_ = filedialog.askopenfilename()
        pass

    # 退出
    def client_exit(self):
        exit()
        pass

    # 显示图片
    def showImg(self):
        load = Image.open(path_)
        # 重新设定图片大小
        load.thumbnail((250, 250))
        render = ImageTk.PhotoImage(load)

        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)
        pass

    # 显示图片识别结果
    def showResult(self):
        # 填入百度API信息
        APP_ID = ''
        API_KEY = ''
        SECRET_KEY = ''

        aipFace = AipFace(APP_ID, API_KEY, SECRET_KEY)

        # 使用base64重新编码图片
        def get_file_content(filePath):
            with open(filePath, 'rb') as fp:
                content = base64.b64encode(fp.read())
                return content.decode('utf-8')
            pass

        imageType = "BASE64"

        options = {}
        options["face_field"] = "age,gender,beauty"

        result = aipFace.detect(get_file_content(path_), imageType, options)

        sex = result['result']['face_list'][0]['gender']['type']
        age = result['result']['face_list'][0]['age']
        beauty = result['result']['face_list'][0]['beauty']

        # 使用标签显示结果
        Label(root, text="sex: " + sex).place(x=260, y=30)
        Label(root, text="age: " + str(age)).place(x=260, y=60)
        Label(root, text="beauty: " + str(beauty)).place(x=260, y=90)
        pass

    pass

root = Tk()
root.geometry("400x300")
AIP = Window(root)
root.mainloop()