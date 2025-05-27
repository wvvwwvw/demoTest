from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow
from forms.Navigation import Ui_MainWindow
from partners import PartnersWidow
from sales import SalesWidow

class Navigation(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.salesBtn.clicked.connect(self.go_sales)
        self.ui.calcBtn.clicked.connect(self.go_calc)
        self.ui.partnersBtn.clicked.connect(self.go_partners)


    def go_sales(self):
        sale_win = SalesWidow(self)
        sale_win.show()
        self.hide()


    def go_calc(self):
        pass

    def go_partners(self):
        partners_win = PartnersWidow(self)
        partners_win.show()
        self.hide()

