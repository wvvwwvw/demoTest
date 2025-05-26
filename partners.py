from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow, QFrame, QLabel, QMessageBox, QVBoxLayout, QGridLayout, QDialog
from connect_to_database import connect_db
from forms.Partner import Ui_MainWindow
from changePartner import ChangePartner


class PartnersWidow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.partners = []

        self.load_partners()

        self.ui.backBtn.clicked.connect(self.go_back)
        self.ui.addPartnerBtn.clicked.connect(self.add_partner)

    def go_back(self):
        self.parent().show()
        self.hide()

    def closeEvent(self, event):
        QtCore.QCoreApplication.quit()

    def load_partners(self):
        try:
            cursor = connect_db.cursor(dictionary=True)
            cursor.execute("select p.id, t.name as type, p.name, p.FIO, p.phone, p.rating "
                           "from Partners p "
                           "join Types t on t.id = p.type_id "
                           "order by p.id asc ")
            self.partners = cursor.fetchall()
            cursor.close()

            try:
                self.display_partners()
            except Exception as err:
                QMessageBox.critical(self, "Ошибка!", f"Произошла ошибка {err} при попытке выводе Партнеров!")
                print(err)

        except Exception as err:
            QMessageBox.critical(self, "Ошибка!", f"Произошла ошибка {err} при попытке получения Партнеров!")

    def display_partners(self):
        layout = self.ui.partnersVerticalLayout
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for partner in self.partners:
            frame = QFrame()
            frame.setFrameShape(QFrame.Shape.Box)
            frame.setStyleSheet("background-color: #F4E8D3;")
            frame.setFixedHeight(120)

            frame.setMouseTracking(True)
            frame.mousePressEvent = lambda _, part=partner: self.change_partner(part)

            frame_layout = QGridLayout(frame)

            frame_layout.setColumnMinimumWidth(0, 370)
            frame_layout.setColumnMinimumWidth(1, 300)

            info_layout = QVBoxLayout()

            type_and_name = QLabel(f"{partner['type']} | {partner['name']}")
            type_and_name.setStyleSheet("font-size: 15pt;")

            fio = QLabel(f"Директор: {partner['FIO']}")
            fio.setStyleSheet("font-size: 9pt;")

            phone = QLabel(
                f"+7 ({partner['phone'][:3]}) {partner['phone'][3:6]}-{partner['phone'][6:8]}-{partner['phone'][8:]}")
            phone.setStyleSheet("font-size: 9pt;")

            rating = QLabel(f"Рейтинг: {partner['rating']}")
            rating.setStyleSheet("font-size: 9pt;")

            info_layout.addWidget(type_and_name)
            info_layout.addWidget(fio)
            info_layout.addWidget(phone)
            info_layout.addWidget(rating)

            frame_layout.addLayout(info_layout, 0, 0)

            discount_value = self.count_discount(partner['id'])
            discount = QLabel(discount_value)
            discount.setStyleSheet("font-size: 15pt;")
            discount.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignRight)

            frame_layout.addWidget(discount, 0, 1)

            layout.addWidget(frame)

    def count_discount(self, p_id):
        try:
            cursor = connect_db.cursor(dictionary=True)
            cursor.execute("select sum(quantity) as summ "
                           "from Sales "
                           "where partner_id = %s "
                           "group by partner_id ", (p_id,))
            sale = cursor.fetchone()
            sale_sum = int(sale['summ'])
            cursor.close()

            if sale_sum < 10000:
                return '0%'
            elif 10000 < sale_sum < 50000:
                return '5%'
            elif 50000 < sale_sum < 300000:
                return '10%'
            else:
                return '15%'

        except Exception as err:
            QMessageBox.critical(self, "Ошибка!", f"Произошла ошибка {err} при расчете скидки!")

    def change_partner(self, partner):
        part = partner
        dialog = ChangePartner(self, part)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                id_type, name, fio, phone, rating = dialog.save_changes()
            except Exception as err:
                print(err)
            try:
                cursor = connect_db.cursor()
                # SQL-запрос для обновления данных партнера
                query = """
                    UPDATE Partners 
                    SET type_id = %s, 
                        name = %s, 
                        FIO = %s, 
                        phone = %s, 
                        rating = %s 
                    WHERE id = %s
                    """
                # Параметры для запроса (предполагается, что self.partner_id существует)
                params = (id_type, name, fio, phone, rating, part['id'])
                cursor.execute(query, params)
                connect_db.commit()
                cursor.close()
                QMessageBox.information(self, "Успех", "Данные успешно обновлены")
                self.load_partners()
            except Exception as e:
                connect_db.rollback()
                QMessageBox.critical(self, "Ошибка базы данных", f"Произошла ошибка: {str(e)}")
                print(f"Database error: {e}")

    def add_partner(self):
        pass
