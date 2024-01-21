from tkinter import *
from tkinterdnd2 import DND_FILES, TkinterDnD



def createNav():

    def show_text1():
        text1.grid(row=1, column=0, columnspan=2, sticky="nsew")
        text2.grid_remove()

    def show_text2():
        text2.grid(row=1, column=0, columnspan=2, sticky="nsew")
        text1.grid_remove()

    root = Tk()
    root.title("导航栏切换Text")

    # 创建一个Frame作为父控件
    frame = Frame(root)
    frame.pack(padx=10, pady=10)

    # 导航栏按钮1
    btn1 = Button(frame, text="Text 1", command=show_text1)
    btn1.grid(row=0, column=0)

    # 导航栏按钮2
    btn2 = Button(frame, text="Text 2", command=show_text2)
    btn2.grid(row=0, column=1)

    # 创建Text1，并使用grid()方法将其放置在第1行、第1列
    global text1
    text1 = Text(frame, wrap=WORD, padx=5, pady=5)
    text1.grid(row=1, column=0, columnspan=2, sticky="nsew")

    # 创建Text2，并使用grid()方法将其放置在第1行、第1列
    global text2
    text2 = Text(frame, wrap=WORD, padx=5, pady=5)
    text2.grid(row=1, column=0, columnspan=2, sticky="nsew")
    text2.grid_remove()  # 隐藏Text2初始时

    root.mainloop()

class ConfigApp:

    def handle_drop(event, text_widget):
        files = event.data
        if files:
            if files[0] == "{" and files[-1] == "}":
                files = files[1:-1]
            file_directory = files  # 只处理第一个拖拽的文件
            text_widget.delete(1.0, END)
            text_widget.insert(END, file_directory)


    def createLabelAndText(self, root: Widget, label_text: str,frameBG:str,textHeight:int):

        def on_parent_resize(event):
            new_height = max(1, event.height // 2)  # 父视图高度的一半，至少为1
            frame.grid_rowconfigure(1, weight=1)
            text_below.config(height=new_height)

        if isinstance(frameBG,str) == False:
            frameBG = '#FFFFFF'

        frame = Frame(root,bg=frameBG)
        frame.pack(padx=0, pady=0,fill=BOTH,expand=True)

        # 创建Label，并使用grid()方法将其放置在第1行、第1列，设置宽度自适应文字宽度
        label = Label(frame, text=label_text, anchor=E,font=('微软雅黑', 15),bg=frame['bg'],width=0)
        label.grid(row=0, column=0, sticky="nsew")

        # 创建Text，并使用grid()方法将其放置在第1行、第2列
        text = Text(frame, wrap=WORD,height=10,font=('微软雅黑', 15),bg=frame['bg'], padx=5, pady=5)
        text.grid(row=0, column=1, sticky="nsew")

        # 创建下方的Text，并使用grid()方法将其放置在第2行、第1列，设置columnspan=2，使其跨越两列
        text_below = Text(frame, wrap=WORD,font=('微软雅黑', 15),height=textHeight)
        text_below.grid(row=1, column=0, columnspan=2, sticky="nsew")

        text.drop_target_register(DND_FILES)
        text.dnd_bind('<<Drop>>', lambda event: handle_drop(event, text))

        # 设置父视图的大小改变事件处理函数，使下方的Text随父视图高度改变而改变
        root.bind("<Configure>", on_parent_resize)

        # 设置第一行的高度固定
        frame.grid_rowconfigure(0, minsize=50)
        # 设置第一行的列权重，使得Text在垂直方向上居中
        frame.grid_rowconfigure(0, weight=1)

        # 设置网格的行和列权重，使第二行的Text可以随父视图高度改变而改变
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(1, weight=1)



    def create(self):
        print('')

    def createWindow(self):


        def deff():
            print('asdgasdgdasdgas')

        win = TkinterDnD.Tk()
        win.title("xib代码生成工具")
        win.config(bg="pink")
        # win.geometry('380x270')
        # 窗口不允许改变
        # win.resizable(0, 0)
        win.iconbitmap('./python.png')

        # 创建一个水平方向的 panedwindow，并添加到主窗口中，默认为水平方向
        p_window1 = PanedWindow(orient=VERTICAL, showhandle=True,width=1000)
        p_window1.pack(fill=BOTH, expand=1)

        top_Frame = Frame(p_window1
                          , highlightbackground="black"
                          , highlightthickness=1
                          , bg='#FAFAFA'
                          , bd=3)

        self.createLabelAndText(top_Frame,'文件名配置：','#B0C4DE',1)
        p_window1.add(top_Frame)

        top_Frame1 = Frame(p_window1
                          , highlightbackground="black"
                          , highlightthickness=1
                          , bg='#FAFAFA'
                          , bd=3)

        self.createLabelAndText(top_Frame1, 'color配置：', '#B0C4DE', 1)
        p_window1.add(top_Frame1)

        top_Frame2 = Frame(p_window1
                           , highlightbackground="black"
                           , highlightthickness=1
                           , bg='#FAFAFA'
                           , bd=3)

        self.createLabelAndText(top_Frame2, 'font配置：', '#B0C4DE', 1)
        p_window1.add(top_Frame2)

        win.mainloop()


if __name__ == '__main__':
    ConfigApp().createWindow()
    # createNav()