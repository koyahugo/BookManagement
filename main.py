#from books import Book, Books
from books import Books, User



if __name__ == "__main__":
    print("main")
    a = Books()
    a.load_books()
    a.add_books("9784563012519")
    a.show_allbooks_info()
    a.save_books()
    #a.remove_books("9784563012519")
    a.show_allbooks_info()
    
    b = User(23)
    b.show_borrowed_books()
    b.borrow_book(books=a,isbn="9784563012519")
    b.show_borrowed_books()
    b.borrow_book(books=a,isbn="9784563012519")
