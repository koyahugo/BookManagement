# 必要なモジュールをインポート
import urllib.request
import json
import os

# Google Books APIを使用して本の情報を取得するクラス
class BookAPI():
    # staticmethodデコレータを使用し、このメソッドをインスタンス化せずに使用できるようにします。
    @staticmethod
    def get_book_info(isbn) -> dict:
        # Google Books APIを使って、指定されたISBNの本の情報を取得
        with urllib.request.urlopen(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}") as response:
            if response.status == 200:  # 応答が成功した場合
                # 応答をJSON形式に変換
                result = json.loads(response.read())
                # 'items'キーが存在するか確認
                if 'items' in result:
                    book_info = result['items'][0]
                    self_link = book_info.get('selfLink')
                    # 'volumeInfo'キーが存在するか確認
                    if 'volumeInfo' in book_info:
                        volume_info = book_info['volumeInfo']
                        # 本の詳細情報を取得
                        title = volume_info.get('title')
                        authors = volume_info.get('authors', [])
                        publisher = volume_info.get('publisher')
                        published_date = volume_info.get('publishedDate')
                        # 本の詳細情報を辞書として返す
                        return {'title': title, 'authors': authors, 'publisher': publisher, 'published_date': published_date, 'url':self_link, 'isbn':isbn}
        # 本の情報が取得できなかった場合はNoneを返す
        return None

class BookError(Exception):
    pass

# 本を表現するクラス
class Book():
    # 初期化メソッド
    def __init__(self, isbn:str, book_info:dict=None) -> None:
        # ISBNのチェック
        if not self.check_isbn(isbn):
            raise ValueError("Invalid ISBN.")
        self.isbn:str = isbn
        # 本の情報が指定されていない場合、APIを使用して取得
        self.book_info:dict = book_info if book_info is not None else BookAPI.get_book_info(isbn)
        self.available:bool = True

    def disable_book(self):
        self.available = False
    def active_book(self):
        self.available = True

    # ISBNの妥当性をチェックするメソッド
    def check_isbn(self, isbn) -> bool:
        # ISBNが13桁または10桁の場合のチェック
        if len(isbn) == 13:
            return self.is_valid_isbn13(isbn)
        elif len(isbn) == 10:
            return self.is_valid_isbn10(isbn)
        else:
            return False

    # ISBN-13の妥当性をチェックするメソッド
    def is_valid_isbn13(self, isbn:str) -> bool:
        # ISBN-13は13桁の数字である必要がある
        if len(isbn) != 13 or not isbn.isdigit():
            return False
        # チェックディジットの計算
        total = 0
        for i in range(12):
            if i % 2 == 0:
                total += int(isbn[i])
            else:
                total += 3 * int(isbn[i])
        check_digit = (10 - total % 10) % 10
        return check_digit == int(isbn[-1])

    # ISBN-10の妥当性をチェックするメソッド
    def is_valid_isbn10(self, isbn:str) -> bool:
        # ISBN-10は最初の9桁は数字、最後の1桁は数字またはX
        if len(isbn) != 10 or not isbn[:9].isdigit() or not (isbn[-1].isdigit() or isbn[-1] in 'Xx'):
            return False
        # チェックディジットの計算
        total = 0
        for i in range(9):
            total += int(isbn[i]) * (10 - i)
        check_digit = 11 - total % 11
        if check_digit == 11:
            check_digit = '0'
        elif check_digit == 10:
            check_digit = 'X'
        else:
            check_digit = str(check_digit)
        return check_digit == isbn[-1].upper()

    # 本の情報を辞書形式で返すメソッド
    def return_info_dic(self) -> dict[str,str]:
        return self.book_info

    # 本の情報を表示するメソッド
    def show_info(self):
        print(f"Title: {self.book_info.get('title')}")
        print(f"Isbn: {self.isbn}")
        print(f"Authors: {', '.join(self.book_info.get('authors', []))}")
        print(f"Publisher: {self.book_info.get('publisher')}")
        print(f"Published Date: {self.book_info.get('published_date')}\n")

class BooksError(Exception):
    pass

# 複数の本を管理するクラス
class Books():
    # 初期化メソッド
    def __init__(self):
        self.books:dict[str,Book] = {}  # ISBNをキーとした本の辞書

    # 本の情報をJSONファイルとして保存するメソッド
    def save_books(self):
        for isbn, book in self.books.items():
            with open(f'./books/{isbn}.json', 'w') as f:
                json.dump(book.return_info_dic(), f, indent=4)

    # JSONファイルから本の情報を読み込むメソッド
    def load_books(self):
        os.makedirs("books", exist_ok=True)
        for filename in os.listdir("./books"):
            if filename.endswith(".json"):
                isbn = filename[:-5]
                with open(f"./books/{filename}", 'r') as f:
                    book_info = json.load(f)
                book = Book(isbn,book_info)
                self.books[isbn] = book

    # 新たに本を追加するメソッド
    def add_books(self, isbn):
        self.books[isbn] = Book(isbn)

    # 本を削除するメソッド
    def remove_books(self, isbn):
        if isbn in self.books:
            del self.books[isbn]
            if os.path.exists(f'{isbn}.json'):
                os.remove(f'{isbn}.json')

    # 全ての本の情報を表示するメソッド
    def show_allbooks_info(self):
        for book in self.books.values():
            book.show_info()

    # 指定したISBNの本の情報を表示するメソッド
    def show_book_info(self,isbn:str):
        # getメソッドを使用して、指定されたISBNが存在しない場合にNoneを返すようにします。
        book = self.books.get(isbn)
        if book is None:
            raise BooksError("This book does not exist!")
        else:
            return book

    def does_book_exist(self, isbn):
        if isbn in self.books:
            return True
        else:
            False

    def borrow_book(self,isbn):
        if self.does_book_exist(isbn):
            if self.books[isbn].available:
                self.books[isbn].disable_book()
            else:
                raise BooksError("This book is not available.")
        else:
            raise BooksError("This book does not exist!")

    def return_book(self,isbn):
        if  self.does_book_exist(isbn):
            if self.books[isbn].available == False:
                self.books[isbn].active_book()
            else:
                raise BookError("This book has not been borrowed.")
        else:
            raise BooksError("This book does not exist!")

"""
class User:
    def __init__(self, student_id:str):
        self.student_id:str = student_id
        self.borrowed_books:list[str] = []

    def borrow_book(self,books: Books, isbn : str):
        try:
            books.borrow_book(isbn)
            self.borrowed_books.append(isbn)
            print(f"{self.student_id}が{isbn}を借りました")
            print(f"{isbn}のじょうほうは{books.show_book_info(isbn)}")
        except BooksError as a:
            print(a)

    def return_book(self, books: Books, isbn: str):
        try:
            books.return_book(isbn)
            self.borrowed_books.remove(isbn)
            print(f"{self.student_id}が{isbn}を返しました")
            print(f"{isbn}のじょうほうは{books.show_book_info(isbn)}")
        except BooksError as a:
            print(a)

    def show_borrowed_books(self):
        # ユーザーが現在借りている全ての本を表示します。
        print(f"User {self.student_id} has borrowed these books:")
        print(self.borrowed_books)
"""
