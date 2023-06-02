from gui import BookApp
from users import Users
from books import Books


if __name__ == "__main__":
    app = BookApp(Users(Books))

    app.mainloop()
