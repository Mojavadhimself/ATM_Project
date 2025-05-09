import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

persian_font = QFont('Vazir', 16)
english_font = QFont('Spendthrift', 16)


class Bank:
    def __init__(self, accounts):
        self.accounts = accounts


class Account:
    def __init__(self, card_number, card_pass, balance):
        self.card_number = card_number
        self.card_pass = card_pass
        self.balance = balance

    def show_balance(self):
        return self.balance

    def get_cash(self, cash):
        if cash > self.balance:
            self.balance -= cash
            return True
        else:
            return False

    def transfer(self, other, amount):
        if amount > self.balance:
            self.balance -= amount
            other.balance += amount
            return True
        else:
            return False

    def change_password(self, password):
        if password == self.card_pass:
            return False
        else:
            self.card_pass = password
            return True


class LanguageWindow(QWidget):
    def __init__(self, bank):
        super().__init__()
        self.bank = bank
        self.setFixedSize(1080, 720)
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addStretch(3)
        self.eng_window = None
        self.per_window = None

        layout1 = QVBoxLayout()
        layout1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label1 = QLabel('زبان خود را انتخاب کنید')
        label1.setFont(persian_font)
        label2 = QLabel('Select your language')
        label2.setFont(english_font)
        layout1.addWidget(label1)
        layout1.addWidget(label2)
        self.main_layout.addLayout(layout1)

        self.main_layout.addStretch(1)

        layout2 = QHBoxLayout()
        button1 = QPushButton('فـارسـی')
        button1.setFont(persian_font)
        button1.setFixedWidth(120)
        button1.setFixedHeight(40)
        button1.clicked.connect(self.persian_window)
        button2 = QPushButton('English')
        button2.setFont(english_font)
        button2.setFixedWidth(120)
        button2.setFixedHeight(40)
        button2.clicked.connect(self.english_window)
        layout2.addStretch(3)
        layout2.addWidget(button1)
        layout2.addStretch(1)
        layout2.addWidget(button2)
        layout2.addStretch(3)
        self.main_layout.addLayout(layout2)

        self.main_layout.addStretch(3)

        self.setLayout(self.main_layout)
        self.show()

    def persian_window(self):
        self.per_window = EntryWindow('persian', self.bank)
        self.per_window.show()
        self.hide()

    def english_window(self):
        self.eng_window = EntryWindow('english', self.bank)
        self.eng_window.show()
        self.hide()


class EntryWindow(QWidget):
    def __init__(self, language, bank):
        super().__init__()
        self.language = language
        self.bank = bank
        self.setFixedSize(1080, 720)
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addStretch(3)

        self.card_number_input = None
        self.card_pass_input = None
        self.card_number = ''
        self.card_pass = ''
        self.menu_window = None

        if self.language == 'persian':
            self.setFont(persian_font)
        else:
            self.setFont(english_font)

        layout1 = QVBoxLayout()
        layout1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if self.language == 'persian':
            label1 = QLabel('شماره کارت خود را وارد کنید')
            label2 = QLabel('رمز کارت خود را وارد کنید')
        else:
            label1 = QLabel('Enter Your card number')
            label2 = QLabel('Enter Your card pass')

        label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_number_box = QLineEdit()
        card_number_box.setFixedWidth(600)
        card_number_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_validator = QRegularExpressionValidator(QRegularExpression(r'\d{0,16}'))
        card_number_box.setValidator(card_validator)
        self.card_number_input = card_number_box

        label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pass_box = QLineEdit()
        pass_box.setFixedWidth(600)
        pass_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pass_box.setEchoMode(QLineEdit.EchoMode.Password)
        pass_validator = QRegularExpressionValidator(QRegularExpression(r'\d{0,4}'))
        pass_box.setValidator(pass_validator)
        self.card_pass_input = pass_box

        if self.language == 'persian':
            submit_button = QPushButton('تایید')
        else:
            submit_button = QPushButton('Submit')
        submit_button.clicked.connect(self.handle_submit)
        submit_button.setFixedWidth(120)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(submit_button)

        layout1.addStretch(1)
        layout1.addWidget(label1)
        layout1.addSpacing(5)
        layout1.addWidget(card_number_box)
        layout1.addSpacing(30)
        layout1.addWidget(label2)
        layout1.addSpacing(5)
        layout1.addWidget(pass_box)
        layout1.addStretch(1)

        self.main_layout.addLayout(layout1)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(button_layout)
        self.main_layout.addStretch(3)

        self.setLayout(self.main_layout)
        self.show()

    def handle_submit(self):
        self.card_number = self.card_number_input.text()
        self.card_pass = self.card_pass_input.text()

        print(f"Card Number: {self.card_number}")
        print(f"Card Pass: {self.card_pass}")

        found = False
        for account in self.bank.accounts:
            if account.card_number == self.card_number:
                found = True
                if account.card_pass == self.card_pass:
                    print('Pass')
                    self.submit(self.card_pass, self.card_number)
                    return
                else:
                    print('Wrong password')
                    self.show_error_window('pass')
                    return

        if not found:
            self.show_error_window('number')

    def show_error_window(self, error_type):
        error_window = QWidget()
        error_window.setFixedSize(400, 150)
        error_window.setWindowTitle("Error")
        error_window.setFont(persian_font if self.language == 'persian' else english_font)
        error_layout = QVBoxLayout()


        if error_type == 'pass':
            error_text = 'رمز اشتباه است!' if self.language == 'persian' else 'Wrong Password!'
        else:
            error_text = 'شماره کارت نا معتبر است!' if self.language == 'persian' else 'Invalid card number!'

        error_label = QLabel(error_text)
        back_button = QPushButton('بازگشت' if self.language == 'persian' else 'Back')
        back_button.clicked.connect(lambda: (error_window.close(), self.show()))

        error_layout.addStretch(1)
        error_layout.addWidget(error_label)
        error_layout.addWidget(back_button)
        error_layout.addStretch(1)

        error_window.setLayout(error_layout)
        error_window.show()
        self.hide()

    def submit(self, password, number):
        this_account = None
        for account in self.bank.accounts:
            if account.card_number == number:
                this_account = account
                break
        self.menu_window = MenuWindow(self.language, self.bank, this_account)
        self.menu_window.show()
        self.hide()

    def back(self):
        self.show()


class MenuWindow(QWidget):
    def __init__(self, language, bank, account):
        super().__init__()
        self.language = language
        self.bank = bank
        self.account = account
        self.setFixedSize(1080, 720)
        if self.language == 'persian':
            self.setFont(persian_font)
        else:
            self.setFont(english_font)
        self.main_layout = QGridLayout()

        english_buttons = (
            ['Get Cash', 0, 0, 1],
            ['Change Password', 0, 1, 2],
            ['Money Transfer', 1, 0, 3],
            ['Account Balance', 1, 1, 4]
        )
        persian_buttons = (
            ['برداشت وجه', 0, 0, 1],
            ['تغییر رمز', 0, 1, 2],
            ['کارت به کارت', 1, 0, 3],
            ['اعلام موجودی', 1, 1, 4]
        )
        if self.language == 'persian':
            for text, row, col, func in persian_buttons:
                button = QPushButton(text)
                button.setFixedWidth(150)
                button.setFixedHeight(70)
                if func == 1:
                    button.clicked.connect(self.get_cash)
                elif func == 2:
                    button.clicked.connect(self.change_password)
                elif func == 3:
                    button.clicked.connect(self.money_transfer)
                else:
                    button.clicked.connect(self.account_balance)
                self.main_layout.addWidget(button, row, col)
        else:
            for text, row, col, func in english_buttons:
                button = QPushButton(text)
                button.setFixedWidth(250)
                button.setFixedHeight(70)
                if func == 1:
                    button.clicked.connect(self.get_cash)
                elif func == 2:
                    button.clicked.connect(self.change_password)
                elif func == 3:
                    button.clicked.connect(self.money_transfer)
                else:
                    button.clicked.connect(self.account_balance)
                self.main_layout.addWidget(button, row, col)

        self.setLayout(self.main_layout)
        self.show()

    def get_cash(self):
        get_cash_window = GetCash(self.account, self.language)
        get_cash_window.show()
        self.hide()

    def change_password(self):
            pass

    def money_transfer(self):
            pass

    def account_balance(self):
            pass


class GetCash(QWidget):
    def __init__(self, account, language):
        super().__init__()
        self.account = account
        self.language = language
        self.setFixedSize(1080, 720)
        self.setFont(persian_font if self.language == 'persian' else english_font)

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addStretch(1)
        if self.language == 'persian':
            label1 = QLabel('مقدار وجه مورد نظر را انتخاب کنید')
        else:
            label1 = QLabel('Select your wanted money')
        label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(label1)
        self.main_layout.addSpacing(20)

        layout1 = QGridLayout()

        buttons = (
            ['100,000', 0, 0, 100000],
            ['200,000', 0, 1, 200000],
            ['500,000', 1, 0, 500000],
            ['1,000,000', 1, 1, 1000000]
        )
        for text, row, col, amount in buttons:
            button = QPushButton(text)
            button.setFixedWidth(250)
            button.setFixedHeight(70)
            button.clicked.connect(lambda _, cash=amount: self.get_cash(cash))
            layout1.addWidget(button, row, col)

        self.main_layout.addLayout(layout1)

        self.main_layout.addSpacing(20)

        layout2 = QHBoxLayout()
        if self.language == 'persian':
            label2 = QLabel('وجه دلخواه:')
        else:
            label2 = QLabel('wanted amount:')
        label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.selected_cash = QLineEdit()
        self.selected_cash.setFixedWidth(300)
        layout2.addStretch(1)
        layout2.addWidget(self.selected_cash)
        layout2.addWidget(label2)
        layout2.addStretch(1)

        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(layout2)

        self.main_layout.addStretch(1)

        self.setLayout(self.main_layout)

    def back_to_menu(self):
        menu_window = MenuWindow(self.language, self.bank, self.account)
        menu_window.show()
        self.hide()

    def get_cash(self, amount):
        print(self.account.balance)
        print(int(amount))
        if self.account.get_cash(int(amount)):
            msg = QMessageBox(self)
            if self.language == 'persian':
                msg.setWindowTitle('موفقیت‌آمیز')
                msg.setText('برداشت وجه با موفقیت انجام شد.')
            else:
                msg.setWindowTitle('Success')
                msg.setText('Withdrawal completed successfully.')
            back_button = QPushButton('Back')
            msg.setStandardButtons(self.back_to_menu)
            msg.exec()
        else:
            msg = QMessageBox(self)
            if self.language == 'persian':
                msg.setWindowTitle('موجودی ناکافی')
                msg.setText('موجودی حسابتان کافی نیست.')
            else:
                msg.setWindowTitle('Not Enough Money')
                msg.setText('your balance is not enough for wanted amount.')
            back_button = QPushButton('Back')
            back_button.clicked.connect(self.back_to_menu)
            msg.setStandardButtons(back_button)
            msg.exec()


if __name__ == "__main__":
    account1 = Account('5894631219067527', '1111', 1000000)
    account2 = Account('5894631219067520', '1000', 4300000)
    accounts = [account1, account2]
    bank = Bank(accounts)

    app = QApplication(sys.argv)

    window = LanguageWindow(bank)
    window.show()

    app.exec()
