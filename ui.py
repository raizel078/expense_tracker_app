from PySide6.QtWidgets import QMainWindow ,QHeaderView, QTableWidget,QPushButton, QDateEdit,QSizePolicy, QComboBox, QLineEdit, QLabel , QWidget , QHBoxLayout , QVBoxLayout
from PySide6.QtCore import  Qt , QDate


#Codes
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

        self.transaction_widget = QWidget()
        self.transaction_widget.setStyleSheet('background-color:#262624; border-radius:10px;')
        self.transaction_widget.setFixedHeight(120)
        self.main_layout.addWidget(self.transaction_widget)

        self.transaction_layout = QVBoxLayout()
        self.transaction_layout.setContentsMargins(0,0,0,0)
        self.transaction_widget.setLayout(self.transaction_layout)

        self.trans_title = QLabel('Add transaction')
        self.trans_title.setStyleSheet('font-size:15px; color:white;')
        self.trans_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.transaction_layout.addWidget(self.trans_title)



        #for trans widget.
        self.amount_input = QLineEdit()
        self.amount_input.setStyleSheet('color:white; font-size:12px; border: 2px solid white')
        self.amount_field = self.create_trans('Amount', self.amount_input)
        self.description = QLineEdit()
        self.description.setStyleSheet('color:white; font-size:12px; border: 2px solid white;')
        self.description_field = self.create_trans('Description', self.description)
        self.category = QComboBox()
        self.category.setStyleSheet('color:white; font-size:12px; border: 2px solid white')
        self.category.addItems(['Food', 'Rent', 'Transport', 'Health', 'Other'])
        self.category_combo = self.create_trans('Category', self.category)
        self.type = QComboBox()
        self.type.setStyleSheet('color:white; font-size:12px; border: 2px solid white')
        self.type.addItems(['Expense','Income'])
        self.type_combo = self.create_trans('Type', self.type)
        self.date = QDateEdit()
        self.date.setDate(QDate.currentDate())
        self.date.setCalendarPopup(True)
        self.date.setStyleSheet('color:white; font-size:12px; border: 2px solid white')
        self.date_field = self.create_trans('Date', self.date)


        #now adding to the layout.
        self.fields_layout = QHBoxLayout()
        self.fields_layout.setContentsMargins(0,0,0,0)
        self.transaction_layout.addLayout(self.fields_layout)
        self.fields_layout.addWidget(self.amount_field)
        self.fields_layout.addWidget(self.description_field)
        self.fields_layout.addWidget(self.category_combo)
        self.fields_layout.addWidget(self.type_combo)
        self.fields_layout.addWidget(self.date_field)

        #now add button
        self.add_button = QPushButton(' + Add')
        self.add_button.setStyleSheet('color:white; font-size:10px; border:2px solid white; font-size:15px;')
        self.add_button.setFixedWidth(130)
        self.transaction_layout.addWidget(self.add_button)
        self.transaction_layout.addStretch()

        #now the search button adding.
        self.filter_layout = QHBoxLayout()
        self.main_layout.addLayout(self.filter_layout)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText('    Search by Description')
        self.search_bar.setStyleSheet('color:white; font-size:10px;')
        self.filter_type = QComboBox()
        self.filter_type.addItems(['All', 'Expense', 'Income'])
        self.filter_layout.addWidget(self.search_bar)
        self.filter_layout.addWidget(self.filter_type)
        self.filter_type.setStyleSheet('color:white; font-size:10px;')

        # table.
        self.table = QTableWidget()
        self.main_layout.addWidget(self.table)
        self.main_layout.addStretch()
        self.table.setColumnCount(5)
        self.table.setStyleSheet(
            'QHeaderView::section { border: none; background-color: #1f1f1e; color: white; font-size:11px; }')
        self.table.setHorizontalHeaderLabels(['Date','Description', 'Category', 'Type', 'Amount'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setShowGrid(False)



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


    def create_trans(self, title_text, field):
        field.setFixedHeight(25)
        box = QWidget()
        box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        box_layout = QVBoxLayout()
        box_layout.setContentsMargins(0, 0, 0, 0)
        box.setLayout(box_layout)

        title = QLabel(str(title_text))
        title.setStyleSheet('color:white; font-size:10px;')
        box_layout.addWidget(title)
        box_layout.addWidget(field)
        box_layout.addStretch()
        return box

















