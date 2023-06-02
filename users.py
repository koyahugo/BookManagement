from books import *
import json

class User():
    def __init__(self,student_id:str,book_list = []):
        self.student_id = student_id
        self.book_list:list[str] = book_list
    
    def borrow_book(self,isbn:str):
        self.book_list.append(isbn)
    def return_book(self,isbn:str):
        self.book_list.remove(isbn)
    def return_borrow_books_list(self) -> list :
        return self.book_list


class Users():
    def __init__(self, books:Books):
        self.student_dict:dict[str, User] = {}
        self.books:Books = books
        self.load_users()
    
    def retunr_books_class(self) -> Books:
        return self.books
    
    def save_users(self):
        os.makedirs("users", exist_ok=True)
        for student_id, books_class in self.student_dict.items():
            with open(f'./users/{student_id}.json', 'w') as f:
                json.dump(books_class.return_borrow_books_list(), f, indent=4)
    
    def load_users(self):
        os.makedirs("users", exist_ok=True)
        for filename in os.listdir("./users"):
            if filename.endswith(".json"):
                student_id = filename[:-5]
                with open(f"./users/{filename}", 'r') as f:
                    book_list = json.load(f)
                user = User(student_id, book_list)
                self.student_dict[student_id] = user
    
    def add_user(self, student_id):
        self.student_dict[student_id] = User(student_id)
    
    def remove_user(self, student_id):
        self.student_dict.pop(student_id)
        if os.path.exists(f'users/{student_id}.json'):
            os.remove(f'users/{student_id}.json')
    
    def show_all_users(self):
        for i in self.student_dict:
            print(i)
    
    def borrow_book(self, student_id, isbn):
        try:
            self.books.borrow_book(isbn)
            self.student_dict[student_id].borrow_book(isbn)
            print(f"{student_id}が{isbn}を借りました。")
        except BooksError as e:
            print(e)
    def return_book(self, student_id, isbn):
        try:
            self.books.return_book(isbn)
            self.student_dict[student_id].return_book(isbn)
            print(f"{student_id}が{isbn}を返却しました。")
        except BookError as e:
            print(e)

    def show_borrow_books(self,student_id) -> None:
        print(self.student_dict[student_id].return_borrow_books_list())
    def return_borrow_books_list(self,student_id) -> list:
        return self.student_dict[student_id].return_borrow_books_list()
