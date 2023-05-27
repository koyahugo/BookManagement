from books import *

class User():
    def __init__(self,student_id):
        self.student_id = student_id
        self.book_list:list[str] = []
    
    def borrow_book(self,isbn:str):
        self.book_list.append(isbn)
    def return_book(self,isbn:str):
        self.book_list.remove(isbn)


class Users():
    def __init__(self, books:Books):
        self.student_dict:dict[str, User] = {}
        self.books:Books = books
    
    def add_user(self, student_id):
        self.student_dict[student_id] = User(student_id)
    
    def remove_user(self, student_id):
        self.student_dict.pop(student_id)
    
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

