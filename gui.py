import tkinter as tk
import csv
from users import Users
from books import Books

class BookApp(tk.Tk):
    def __init__(self, users_class:Users):
        self.users_class:Users = users_class
        self.books_class:Books = self.users_class.retunr_books_class()
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
        self.master.destroy()

def nextpage():
    with open('ID.csv', 'a')as f:
        writer = csv.writer(f)
        writer.writerow()

class UserPage(tk.Frame):
    def __init__(self,master:BookApp):
        self.master:BookApp = master
        super().__init__()
        label = tk.Label(self, text="学籍番号")
        label.grid(row=1, column=1)
        ID_text = tk.StringVar(self)
        tk.Entry(
            self,
            textvariable=ID_text
        ).grid(row=1, column=2)

        tk.Button(self, text="前へ", command=lambda:master.switch_frame(MainPage)).grid(row=3, column=1)
        tk.Button(self, text="次へ", command=lambda:self.nextpage_Button(ID_text.get())).grid(row=3, column=3)
    
    def nextpage_Button(self, student_id):
        #ここにUser処理を書く
        self.master.users_class.add_user(student_id=student_id)
        #User処理が成功したら次の画面へ進む
        self.master.switch_frame(UserPage2)

class UserPage2(UserPage):
    def __init__(self, master:BookApp):
        self.master:BookApp = master
        tk.Frame.__init__(self, master)
        label_1 = tk.Label(self,text="ユーザー登録が完了しました")
        label_1.grid(row=1, column=1)
        topbtn = tk.Button(self,text="メインメニューへ戻る", command=lambda:master.switch_frame(MainPage))
        topbtn.grid(row=2, column=1)
        

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
    app = BookApp(Users(Books))
    app.mainloop()
