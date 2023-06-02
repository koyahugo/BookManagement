from gui import BookApp
from users import Users
from books import Books


if __name__ == "__main__":
    b = Books()
    b.load_books()
    b.add_books("9784798151847")
    b.save_books()
    app = BookApp(Users(Books))
    
    app.mainloop()
