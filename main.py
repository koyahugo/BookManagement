#from books import Book, Books
from books import Books
from users import Users



if __name__ == "__main__":
    print("main")
    a = Books()
    a.load_books()
    a.add_books("9784563012519")
    a.show_allbooks_info()
    a.save_books()
    
    b = Users(a)
    b.add_user("2312079")
    b.show_all_users()
    b.borrow_book(isbn="9784563012519",student_id="2312079")
    b.return_book(isbn="9784563012519",student_id="2312079")
    b.borrow_book(isbn="9784563012519",student_id="2312079")
    b.show_borrow_books(student_id="2312079")
    b.borrow_book(isbn="9784563012519",student_id="2312079")
    
    
    
    #a.remove_books("9784563012519")
    """a.show_allbooks_info()
    
    b = User(23)
    b.show_borrowed_books()
    b.borrow_book(books=a,isbn="9784563012519")
    b.show_borrowed_books()
    b.borrow_book(books=a,isbn="9784563012519")"""
