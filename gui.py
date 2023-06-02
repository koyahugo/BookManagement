import tkinter as tk
import csv
from users import Users
from books import Books

class BookApp(tk.Tk):
    def __init__(self, users_class:Users):
        self.users_class:Users = users_class
        self.books_class:Books = self.users_class.retunr_books_class()
        tk.Tk.__init__(self)
        self.title("図書管理アプリ")
        self.geometry("800x600")
        self.font = ('Helvetica', 18)
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
        tk.Button(self, text="ユーザー登録", font=self.master.font,
                  command=self.user_registration).grid(row=0, column=0, sticky="nsew")
        tk.Button(self, text="図書登録", font=self.master.font,
                  command=self.book_registration).grid(row=1, column=0, sticky="nsew")
        tk.Button(self, text="図書一覧", font=self.master.font,
                  command=self.book_list).grid(row=2, column=0, sticky="nsew")
        tk.Button(self, text="貸出", font=self.master.font,
                  command=self.borrow).grid(row=3, column=0, sticky="nsew")
        tk.Button(self, text="終了", font=self.master.font,
                  command=self.quit).grid(row=4, column=0, sticky="nsew")

    def user_registration(self):
        print("ユーザー登録がクリックされました")
        self.master.switch_frame(UserPage)

    def book_registration(self):
        print("図書登録がクリックされました")
        self.master.switch_frame(AddBookPage)

    def book_list(self):
        print("図書一覧がクリックされました")
        self.master.switch_frame(BookListPage)

    def borrow(self):
        print("貸出がクリックされました")
        self.master.switch_frame(BorrowPage)

    def quit(self):
        print("終了がクリックされました")
        self.master.destroy()

class UserPage(tk.Frame):
    def __init__(self,master:BookApp):
        self.master:BookApp = master
        super().__init__()
        label = tk.Label(self, font=self.master.font, text="学籍番号")
        label.grid(row=1, column=1)
        ID_text = tk.StringVar(self)
        tk.Entry(
            self,
            font=self.master.font,
            textvariable=ID_text
        ).grid(row=1, column=2)

        tk.Button(self, text="前へ",font=self.master.font,
                  command=lambda:master.switch_frame(MainPage)).grid(row=3, column=1)
        tk.Button(self, text="次へ",font=self.master.font,
                  command=lambda:self.nextpage_Button(ID_text.get())).grid(row=3, column=3)
    
    def nextpage_Button(self, student_id):
        #ここにUser処理を書く
        self.master.users_class.add_user(student_id=student_id)
        self.master.users_class.save_users()
        #User処理が成功したら次の画面へ進む
        self.master.switch_frame(UserPage2)

class UserPage2(UserPage):
    def __init__(self, master:BookApp):
        self.master:BookApp = master
        tk.Frame.__init__(self, master)
        label_1 = tk.Label(self,text="ユーザー登録が完了しました", font=self.master.font)
        label_1.grid(row=1, column=1)
        topbtn = tk.Button(self,text="メインメニューへ戻る", font=self.master.font, command=lambda:master.switch_frame(MainPage))
        topbtn.grid(row=2, column=1)

class AddBookPage(tk.Frame):
    def __init__(self,master:BookApp):
        self.master:BookApp = master
        super().__init__()
        label = tk.Label(self, font=self.master.font, text="ISBN")
        label.grid(row=1, column=1)
        ISBN_text = tk.StringVar(self)
        tk.Entry(
            self,
            font=self.master.font,
            textvariable=ISBN_text
        ).grid(row=1, column=2)
        
        tk.Button(self, text="前へ",font=self.master.font,
                  command=lambda:master.switch_frame(MainPage)).grid(row=3, column=1)
        tk.Button(self, text="次へ",font=self.master.font,
                  command=lambda:self.nextpage_Button(ISBN_text.get())).grid(row=3, column=3)
    
    def nextpage_Button(self,isbn:str):
        self.master.books_class.add_books(isbn)
        self.master.books_class.save_books()
        self.master.switch_frame(AddBookPage2)

class AddBookPage2(AddBookPage):
    def __init__(self, master:BookApp):
        self.master:BookApp = master
        tk.Frame.__init__(self, master)
        label_1 = tk.Label(self,text="書籍登録が完了しました", font=self.master.font)
        label_1.grid(row=1, column=1)
        topbtn = tk.Button(self,text="メインメニューへ戻る", font=self.master.font, command=lambda:master.switch_frame(MainPage))
        topbtn.grid(row=2, column=1)


class BookListPage(tk.Frame):
    def __init__(self,master:BookApp):
        self.master:BookApp = master
        tk.Frame.__init__(self, master)
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Textウィジェットの作成
        text_widget = tk.Text(self, wrap=tk.NONE, yscrollcommand=scrollbar.set)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH)

        # ScrollbarにTextウィジェットを連動させる
        scrollbar.config(command=text_widget.yview)
        
        for key, value in self.master.books_class.books.items():
            book_info = value.return_info_dic()["title"]
            text_widget.insert(tk.END, f"ISBN: {key}, タイトル: {book_info}\n")
        
        tk.Button(self, font=self.master.font,text="メインページに戻る", 
                  command=lambda: master.switch_frame(MainPage)).pack()
    
    def create_widgets(self):
        pass

class BorrowPage(tk.Frame):
    def __init__(self,master:BookApp):
        self.master:BookApp = master
        super().__init__()
        tk.Label(self, font=self.master.font, text="学籍番号").grid(row=1, column=1)
        tk.Label(self, font=self.master.font, text="ISBN").grid(row=2, column=1)
        ID_text = tk.StringVar(self)
        ISBN_text = tk.StringVar(self)
        tk.Entry(
            self,
            font=self.master.font,
            textvariable=ID_text
        ).grid(row=1, column=2)
        tk.Entry(
            self,
            font=self.master.font,
            textvariable=ISBN_text
        ).grid(row=2, column=2)
        mode = tk.StringVar(value="貸出")
        tk.Radiobutton(self,text="貸出",font=self.master.font,
                       value="貸出",variable=mode).grid(row=3, column=1)
        tk.Radiobutton(self,text="返却",font=self.master.font,
                       value="返却",variable=mode).grid(row=3, column=3)


        tk.Button(self, text="前へ",font=self.master.font,
                  command=lambda:master.switch_frame(MainPage)).grid(row=4, column=1)
        tk.Button(self, text="次へ",font=self.master.font,
                  command=lambda:self.nextpage_Button(ID_text.get(),ISBN_text.get(),mode.get())).grid(row=4, column=3)
    
    def nextpage_Button(self, student_id, isbn, mode):
        #ここにUser処理を書く
        if mode == "貸出":
            self.master.users_class.borrow_book(student_id=student_id,isbn=isbn)
        elif mode == "返却":
            self.master.users_class.return_book(student_id=student_id,isbn=isbn)
        #User処理が成功したら次の画面へ進む
        self.master.switch_frame(BorrowPage2)

class BorrowPage2(BorrowPage):
    def __init__(self, master:BookApp):
        self.master:BookApp = master
        tk.Frame.__init__(self, master)
        label_1 = tk.Label(self,text="本の貸出・返却が完了しました", font=self.master.font)
        label_1.grid(row=1, column=1)
        topbtn = tk.Button(self,text="メインメニューへ戻る", font=self.master.font, command=lambda:master.switch_frame(MainPage))
        topbtn.grid(row=2, column=1)
