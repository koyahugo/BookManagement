from gui import BookApp
from users import Users
from books import Books


if __name__ == "__main__":
    b = Books()
    b.add_books("9784789819503")
    u = Users(b)
    u.load_users()
    u.remove_user("23")
    #u.add_user("23")
    #u.borrow_book("23","9784789819503")
    u.save_users()
    
    app = BookApp(Users(Books))

    app.mainloop()
