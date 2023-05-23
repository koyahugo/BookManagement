import tkinter as tk

class BookApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Start page", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Go to page one",command=lambda: master.switch_frame(MainPage)).pack()

class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Page one", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Go to start page",command=lambda: master.switch_frame(StartPage)).pack()

class MainPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #self.grid(sticky="nsew")
        self.create_widgets()

    def create_widgets(self):
        tk.Button(self, text="ユーザー登録", font=('Helvetica', 18),
                  command=self.user_registration).grid(row=0, column=0, sticky="nsew")
        tk.Button(self, text="図書一覧", font=('Helvetica', 18),
                  command=self.book_list).grid(row=1, column=0, sticky="nsew")
        tk.Button(self, text="貸出", font=('Helvetica', 18),
                  command=self.borrow).grid(row=2, column=0, sticky="nsew")
        tk.Button(self, text="終了", font=('Helvetica', 18),
                  command=self.quit).grid(row=3, column=0, sticky="nsew")

    def user_registration(self):
        print("ユーザー登録がクリックされました")

    def book_list(self):
        print("図書一覧がクリックされました")

    def borrow(self):
        print("貸出がクリックされました")

    def quit(self):
        print("終了がクリックされました")




if __name__ == "__main__":
    app = BookApp()
    app.mainloop()
