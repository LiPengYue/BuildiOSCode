import tkinter as tk
from tkinter import ttk




def createWindow():
    def switch_text(event):
        selected_tab = tab_control.index(tab_control.select())
        for i, frame in enumerate(frames):
            if i == selected_tab:
                frame.tkraise()

    # 创建主窗口
    root = tk.Tk()
    root.title("多文本切换")

    # 创建目录标题栏
    tab_control = ttk.Notebook(root)
    frames = []

    for i in range(1, 3):  # 创建两个目录页面
        frame = ttk.Frame(tab_control)
        frames.append(frame)
        tab_control.add(frame, text=f"目录{i}")

    tab_control.pack(expand=1, fill="both")

    # 创建Label和Text组件
    text_widgets = []

    for i, frame in enumerate(frames):
        label = tk.Label(frame, text=f"文本{i + 1}标签")
        label.grid(row=0, column=0, sticky="w")  # 左对齐

        text_widget = tk.Text(frame, state="normal",height=1)
        text_widget.grid(row=0, column=1, sticky="nsew")  # 填充整个Frame
        text_widget.insert(tk.END, f"这是文本{i + 1}")

        extra_text_widget = tk.Text(frame, state="normal")
        extra_text_widget.grid(row=2, column=0, columnspan=2, sticky="nsew")  # 第一行添加额外的Text
        extra_text_widget.insert(tk.END, f"这是额外的文本{i + 1}")


        text_widgets.append(text_widget)

    # 切换标题栏事件
    tab_control.bind("<<NotebookTabChanged>>", switch_text)

    # 设置行和列的权重以使文本框和标签随窗口大小变化
    for frame in frames:
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(0, weight=1)

    # 启动Tkinter主循环
    root.mainloop()

if __name__ == '__main__':
   createWindow()
    # createNav()