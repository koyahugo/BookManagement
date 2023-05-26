import tkinter as tk

class BookApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame:tk.Frame = None
        self.switch_frame(MainPage)

    def switch_frame(self, frame_class:tk.Frame):
        new_frame:tk.Frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class MainPage(tk.Frame):
    def __init__(self, master: BookApp):
        self.master:BookApp = master
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
        self.master.switch_frame(UserPage)

    def book_list(self):
        print("図書一覧がクリックされました")
        self.master.switch_frame(BookListPage)

    def borrow(self):
        print("貸出がクリックされました")
        self.master.switch_frame(BookListPage)

    def quit(self):
        print("終了がクリックされました")

class UserPage(tk.Frame):
    def __init__(self,master:BookApp):
        self.master:BookApp = master
        tk.Frame.__init__(self, master)
        tk.Button(self,text="メインページに戻る",command=lambda: master.switch_frame(MainPage)).pack()

class BookListPage(tk.Frame):
    def __init__(self,master:BookApp):
        self.master:BookApp = master
        tk.Frame.__init__(self, master)
        tk.Button(self,text="メインページに戻る",command=lambda: master.switch_frame(MainPage)).pack()

class BorrowPage(tk.Frame):
    def __init__(self, master:BookApp):
        self.master:BookApp = master
        tk.Frame.__init__(self,master)
        tk.Button(self,text="メインページに戻る",command=lambda: master.switch_frame(MainPage)).pack()


if __name__ == "__main__":
    app = BookApp()
    app.mainloop()
