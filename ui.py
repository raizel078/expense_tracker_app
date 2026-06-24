from PySide6.QtWidgets import QMainWindow , QTableWidgetItem ,QHeaderView, QTableWidget,QPushButton, QDateEdit,QSizePolicy, QComboBox, QLineEdit, QLabel , QWidget , QHBoxLayout , QVBoxLayout
from PySide6.QtCore import  Qt , QDate
from database import create_connection, create_tables, add_transaction , fetch_data , get_total

#Codes
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(700,800)
        self.move(1920,1)
        self.setWindowTitle('Tracker -Sooynieal')

        self.conn = create_connection()
        create_tables(self.conn)

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
        self.summary_income_box.setFixedHeight(60)
        self.summary_expense_box.setFixedHeight(60)
        self.summary_balance_box.setFixedHeight(60)

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
        self.add_button.setStyleSheet('''
            QPushButton {color:white; font-size:15px; border:2px solid white;}
            QPushButton:disabled {color:grey; border:2px solid grey;}
            QPushButton:pressed {background-color:#3a3a38;}
        ''')
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
        self.table.setColumnCount(5)
        self.table.setStyleSheet(
            'QHeaderView::section { border: none; background-color: #1f1f1e; color: white; font-size:11px; }'
            'QTableWidget { color: white; font-size: 12px; }'
            'QTableCornerButton::section {background-color:#1f1f1e; border: none;}'
        )
        self.table.setHorizontalHeaderLabels(['Date','Description', 'Category', 'Type', 'Amount'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)

        self.add_button.clicked.connect(self.connect_to_data)
        # MOVED here from connect_to_data — signal must only be connected once
        self.filter_type.currentTextChanged.connect(lambda text: self.load_transaction(text))
        #self.search_bar.textChanged.connect(lambda: self.load_transaction(self.filter_type.currentText())) # we will use the SQL way
        self.search_bar.textChanged.connect(lambda: self.load_transaction(self.filter_type.currentText()))
        self.load_transaction()
        self.update_totals()

    def update_totals(self):
        income, expense, balance = get_total(self.conn)
        self.income_value.setText(str(income))
        self.expense_value.setText(str(expense))
        self.balance_value.setText(str(balance))

    def connect_to_data(self):
        if self.amount_input.text()=='' or self.description.text() =='':
            return
        try:
            amount = float(self.amount_input.text())
        except ValueError:
            return
        add_transaction(self.conn, self.amount_input.text(), self.description.text(),
                        self.category.currentText(), self.type.currentText(),
                        self.date.date().toString('yyyy-MM-dd'))
        self.reset_fields()
        self.load_transaction(self.filter_type.currentText())
        self.update_totals()

    def reset_fields(self):
        self.amount_input.clear()
        self.description.clear()
        self.category.setCurrentIndex(0)
        self.type.setCurrentIndex(0)
        self.date.setDate(QDate.currentDate())

    def create_box(self, title_text, color):
        box = QWidget()
        box.setObjectName('summaryBox')
        box.setStyleSheet('#summaryBox {border-radius:10px; background-color:#262624; }')
        box_layout = QVBoxLayout()
        box.setLayout(box_layout)
        title = QLabel(title_text)
        title.setStyleSheet('color:white; font-weight:bold; font-size: 13px; background-color:transparent')
        value = QLabel()
        value.setStyleSheet(f'color:{color}; font-weight: bold; font-size: 10px; background-color:transparent;')
        box_layout.addWidget(title)
        box_layout.addWidget(value)
        box_layout.addStretch()
        return box, value

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
    #trial
    def load_transaction(self, filter_type='All'):
        self.table.setRowCount(0)
        data = fetch_data(self.conn, self.search_bar.text())
        if filter_type != 'All':
            data = [row for row in data if row[4] == filter_type]
        #we will use the SQL way so commenting it out.
        #search_text = self.search_bar.text().lower()
        #if search_text:
            #data = [row for row in data if search_text in str(row[2]).lower()]
        for row in data:
            self.table.insertRow(self.table.rowCount())
            row_index = self.table.rowCount() - 1
            date_item = QTableWidgetItem(str(row[3]))
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row_index, 0, date_item)

            desc_item = QTableWidgetItem(str(row[2]))
            desc_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row_index, 1, desc_item)

            cat_item = QTableWidgetItem(str(row[5]))
            cat_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row_index, 2, cat_item)

            type_item = QTableWidgetItem(str(row[4]))
            type_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row_index, 3, type_item)

            amount_item = QTableWidgetItem(str(row[1]))
            amount_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            if row[4] == 'Expense':
                type_item.setForeground(Qt.GlobalColor.red)
                amount_item.setForeground(Qt.GlobalColor.red)
            else:
                type_item.setForeground(Qt.GlobalColor.green)
                amount_item.setForeground(Qt.GlobalColor.green)
            self.table.setItem(row_index, 4, amount_item)