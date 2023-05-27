
class User():
    def __init__(self,student_id):
        self.student_id = student_id
        self.book_list = None
    
    def borrow_book(self):
        pass



class Users():
    def __init__(self):
        self.student_dict:dict[str, User] = None
    
    def add_user(self, student_id):
        self.student_dict[student_id] = User(student_id)
    
    def remove_user(self, student_id):
        self.student_dict.pop(student_id)
    
    def borrow_book(self, student_id):
        self.student_dict[student_id].borrow_book(student_id)