import datetime


class Loan:
    def __init__(self, book, borrower, loan_date, due_date):
        self.book = book
        self.borrower = borrower
        self.loan_date = loan_date
        self.due_date = due_date

    def is_overdue(self):
        # 返却が遅延しているかどうかを判定するメソッド
        # 現在日付が返却予定日を過ぎていれば遅延と判定する
        return datetime.date.today() > self.due_date
