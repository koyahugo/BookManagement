import urllib.request
import json
import os

class Book():
    def __init__(self, isbn, book_info=None) -> None:
        if not self.check_isbn(isbn):
            raise ValueError("Invalid ISBN.")
        self.isbn = isbn
        self.book_url = None
        self.book_info = book_info
        self.update_info()
        self.available = True

    def update_info(self):
        if self.book_info == None:
            self.book_url = self.get_book_url(self.isbn)
            #辞書
            #タイトル、著者、出版社、出版日、url、isbn
            self.book_info = self.get_book_info(self.book_url)

    def return_info_dic(self):
        return self.book_info
    def show_info(self):
        # 本の情報を表示します。この情報は、タイトル、著者、出版社、出版日を含みます。
        print(f"Title: {self.book_info.get('title')}")
        print(f"Authors: {', '.join(self.book_info.get('authors', []))}")
        print(f"Publisher: {self.book_info.get('publisher')}")
        print(f"Published Date: {self.book_info.get('published_date')}\n")

    def get_book_url(self, isbn):
        # Google Books APIを使って、指定したISBNの本のリンクを取得
        with urllib.request.urlopen(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}") as response:
            # レスポンスが200（成功）の場合
            if response.status == 200:
                # レスポンスをJSONとして読み込む
                result = json.loads(response.read())
                if 'items' in result:
                    book_info = result['items'][0]
                    # Google Booksのリンクを取得（存在しない場合はNone）
                    self_link = book_info.get('selfLink')
                    print(self_link)
                    return self_link
        return None

    def get_book_info(self, book_url):
        # Google Books APIを使って、指定したURLの書籍情報を取得
        if book_url:
            with urllib.request.urlopen(f"{book_url}") as response:
                # レスポンスが200（成功）の場合
                if response.status == 200:
                    # レスポンスをJSONとして読み込む
                    result = json.loads(response.read())
                    # 検索結果が存在するか確認
                    if 'volumeInfo' in result:
                        volume_info = result['volumeInfo']
                        if volume_info:
                            # 書籍のタイトル、著者、出版社、出版日を取得（存在しない場合はNone）
                            title = volume_info.get('title')
                            authors = volume_info.get('authors', [])
                            publisher = volume_info.get('publisher')
                            published_date = volume_info.get('publishedDate')
                            # 各情報を辞書として返す
                            return {'title': title, 'authors': authors, 'publisher': publisher, 'published_date': published_date, 'url':book_url, 'isbn':self.isbn}

    def check_isbn(self,isbn):
        if len(isbn) == 13:
            return self.is_valid_isbn13(isbn)
        elif len(isbn) == 10:
            return self.is_valid_isbn10(isbn)
        else:
            return False
    @staticmethod
    def is_valid_isbn13(isbn):
        # ISBNが13桁で、かつ数字であることをチェックします
        if len(isbn) != 13 or not isbn.isdigit():
            return False

        total = 0
        for i in range(12):  # 最初の12桁について反復します
            if i % 2 == 0:  # 奇数位置の数字の場合
                total += int(isbn[i])
            else:  # 偶数位置の数字の場合
                total += 3 * int(isbn[i])

        # チェックデジットを計算します
        check_digit = (10 - total % 10) % 10

        # チェックデジットがISBNの最後の数字と一致するかどうかをチェックします
        return check_digit == int(isbn[-1])
    @staticmethod
    def is_valid_isbn10(isbn):
        # ISBNが10桁で、最初の9桁が数字であり、最後の桁が数字または'X'であることをチェックします
        if len(isbn) != 10 or not isbn[:9].isdigit() or not (isbn[-1].isdigit() or isbn[-1] in 'Xx'):
            return False

        total = 0
        for i in range(9):  # 最初の9桁について反復します
            total += int(isbn[i]) * (10 - i)

        # チェックデジットを計算します
        check_digit = 11 - total % 11
        if check_digit == 11:
            check_digit = '0'
        elif check_digit == 10:
            check_digit = 'X'
        else:
            check_digit = str(check_digit)

        # チェックデジットがISBNの最後の数字と一致するかどうかをチェックします
        return check_digit == isbn[-1].upper()

class Books():
    def __init__(self):
        # booksという名の辞書を初期化します。キーはISBN、値はBookオブジェクトです。
        self.books = {}

    def save_books(self):
        # 全ての書籍情報をJSONファイルとして保存します。
        # それぞれの書籍情報は、そのISBNを名前とするファイルに保存されます。
        for i in self.books:
            print(i)
            print((self.books[i]).return_info_dic())
            with open(f'{i}.json', 'w') as f:
                json.dump((self.books[i]).return_info_dic(), f, indent=4)

    def load_books(self):
        # 現在のディレクトリ内の全てのJSONファイルをロードします。
        # それぞれのJSONファイルは、その名前（拡張子を除く）をISBNとする書籍の情報とします。
        for filename in os.listdir():
            if filename.endswith(".json"):
                isbn = filename[:-5]
                with open(filename, 'r') as f:
                    book_info = json.load(f)
                book = Book(isbn,book_info)
                self.books[isbn] = book

    def add_books(self, isbn):
        # ISBNを元に新たなBookオブジェクトを作成し、辞書に追加します。
        self.books[isbn] = Book(isbn)

    def remove_books(self, isbn):
        # 指定したISBNの書籍を辞書から削除します。ISBNが辞書に存在しない場合は何も行いません。
        if isbn in self.books:
            del self.books[isbn]
            # 対応する.jsonファイルも削除します。
            if os.path.exists(f'{isbn}.json'):
                os.remove(f'{isbn}.json')

    def show_allbooks_info(self):
        # 保持している全ての本の情報を表示します。
        for book in self.books.values():
            book.show_info()
