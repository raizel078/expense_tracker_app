from PySide6.QtWidgets import QMainWindow , QLabel , QWidget , QHBoxLayout , QVBoxLayout
from PySide6.QtCore import  Qt


#codes
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(700,800)
        self.move(1920,1)
        self.setWindowTitle('Tracker -Sooynieal')

        self.main_widget = QWidget()
        self.main_widget.setStyleSheet('background-color:#1f1f1e; font-size:30px; font-weight:bold;')
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        self.title_label = QLabel('❖ Expense Tracker')
        self.title_label.setStyleSheet('color:white;')
        self.main_layout.addWidget(self.title_label)


        self.summery_layout = QHBoxLayout()
        self.main_layout.addLayout(self.summery_layout)

        self.summary_income_box, self.income_value = self.create_box('income', 'green')
        self.summary_expense_box, self.expense_value = self.create_box('expense', '#ff6b6b')
        self.summary_balance_box, self.balance_value = self.create_box('balance', 'white')
        self.summery_layout.addWidget(self.summary_income_box)
        self.summery_layout.addWidget(self.summary_expense_box)
        self.summery_layout.addWidget(self.summary_balance_box)
        #self.main_layout.addStretch()

        self.transaction_widget = QWidget()
        self.transaction_widget.setStyleSheet('background-color:#262624; border-radius:10px;')
        self.transaction_widget.setFixedHeight(100)
        self.main_layout.addWidget(self.transaction_widget)
        self.transaction_widget.setStyleSheet('border:1px solid white') # need to remove later.
        self.main_layout.addStretch()

        self.transaction_layout = QHBoxLayout()
        self.transaction_widget.setLayout(self.transaction_layout)

        self.trans_title = QLabel('Add transaction')
        self.trans_title.setStyleSheet('font-size:15px; color:white;')
        self.trans_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.transaction_layout.addWidget(self.trans_title)




    def create_box(self, title_text, color):
        box = QWidget()
        box.setObjectName('summaryBox')
        box.setStyleSheet('#summaryBox {border-radius:10px; background-color:#262624; }')

        box_layout = QHBoxLayout()
        box.setLayout(box_layout)
        title = QLabel(title_text)
        title.setStyleSheet('color:white; font-weight:bold; font-size: 13px; background-color:transparent')
        value = QLabel()
        value.setStyleSheet(f'color:{color}; font-weight: bold; font-size: 10px; background-color:transparent;')
        box_layout.addWidget(title)
        box_layout.addWidget(value)
        box_layout.addStretch()
        return box , value


    def create_trans(self, title_text):
        pass    0










