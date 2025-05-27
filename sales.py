from PyQt6 import QtCore
from PyQt6.QtWidgets import QTableWidget, QMessageBox, QMainWindow, QHeaderView, QTableWidgetItem
from forms.Sales import Ui_MainWindow
from connect_to_database import connect_db

class SalesWidow (QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.partners = []
        self.sales = []

        self.ui.backBtn.clicked.connect(self.go_back)
        self.ui.partnerComboBox.currentTextChanged.connect(self.load_data)

        self.load_filters()
        self.load_data()

    def go_back(self):
        self.parent().show()
        self.hide()

    def closeEvent(self, event):
        QtCore.QCoreApplication.quit()

    def load_filters(self):
        try:
            cursor = connect_db.cursor()
            cursor.execute("select id, name from Partners")
            partners = cursor.fetchall()
            cursor.close()

            self.partners = {name : pid for pid, name in partners}
            self.ui.partnerComboBox.addItems(self.partners.keys())
            self.ui.partnerComboBox.addItem("Все")
            self.ui.partnerComboBox.setCurrentText("Все")
        except Exception as err:
            print(err)

    def load_data(self):
        self.ui.salesTableWidget.setColumnCount(4)
        header = ["Партнер", "Продукт", "Количество", "Дата"]
        self.ui.salesTableWidget.setHorizontalHeaderLabels(header)
        self.ui.salesTableWidget.verticalHeader().setVisible(False)
        self.ui.salesTableWidget.verticalHeader().setDefaultSectionSize(50)
        self.ui.salesTableWidget.setRowCount(0)

        try:
            cursor = connect_db.cursor()
            query = "select p.name, pr.name, s.quantity, s.date_sale " \
                           "from Sales s " \
                           "join Partners p on p.id = s.partner_id " \
                           "join Products pr on pr.id = s.product_id "

            param = []

            combo_text = self.ui.partnerComboBox.currentText()
            if combo_text == "Все":
                pass
            else:
                query += "where p.name = %s"
                param.append(combo_text)

            cursor.execute(query, param)
            self.sales = cursor.fetchall()
            cursor.close()

            print(self.sales)
            self.ui.salesTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.display_sales()

        except Exception as err:
            print(err)
            self.display_sales()


    def display_sales(self):
        if not self.sales:
            self.ui.salesTableWidget.setRowCount(0)
            return

        self.ui.salesTableWidget.setRowCount(len(self.sales))

        try:
            for i, row in enumerate(self.sales):
                self.ui.salesTableWidget.setItem(i, 0, QTableWidgetItem(row[0]))
                self.ui.salesTableWidget.setItem(i, 1, QTableWidgetItem(row[1]))
                self.ui.salesTableWidget.setItem(i, 2, QTableWidgetItem(str(row[2])))
                self.ui.salesTableWidget.setItem(i, 3, QTableWidgetItem(str(row[3])))

        except Exception as err:
            print(err)


