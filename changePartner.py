from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QMessageBox
from connect_to_database import connect_db

class ChangePartner(QDialog):
    def __init__(self, parent=None, partner=None):
        super().__init__(parent)
        self.setWindowTitle("Изменить Партнера")
        self.layout = QVBoxLayout(self)


        self.part = partner

        self.type_combo = QComboBox()
        try:
            cursor = connect_db.cursor()
            cursor.execute("select id, name from Types ")
            type = cursor.fetchall()
            cursor.close()
        except Exception as err:
            print(err)
            type = []

        self.type = {name : tid for tid, name in type}
        self.type_combo.addItems(self.type.keys())
        self.type_combo.setCurrentText(self.part['type'])

        self.layout.addWidget(QLabel("Тип:"))
        self.layout.addWidget(self.type_combo)

        self.name = QLineEdit(self.part['name'])
        self.layout.addWidget(QLabel("Наименование:"))
        self.layout.addWidget(self.name)

        fio = self.part['FIO'].split()

        self.last_name = QLineEdit(fio[0])
        self.layout.addWidget(QLabel("Фамилия:"))
        self.layout.addWidget(self.last_name)

        self.first_name = QLineEdit(fio[1])
        self.layout.addWidget(QLabel("Имя:"))
        self.layout.addWidget(self.first_name)

        self.patronimic = QLineEdit(fio[2])
        self.layout.addWidget(QLabel("Отчество:"))
        self.layout.addWidget(self.patronimic)

        self.phone = QLineEdit(str(self.part['phone']))
        self.layout.addWidget(QLabel("Телефон:"))
        self.layout.addWidget(self.phone)

        self.rating = QLineEdit(str(self.part['rating']))
        self.layout.addWidget(QLabel("Рейтинг:"))
        self.layout.addWidget(self.rating)

        self.saveBtn = QPushButton("Сохранить")
        self.saveBtn.clicked.connect(self.accept)
        self.layout.addWidget(self.saveBtn)


    def save_changes(self):
        type_name = self.type_combo.currentText()
        id_type = self.type.get(type_name)

        name = self.name.text().strip()
        last_name = self.last_name.text().strip()
        first_name = self.first_name.text().strip()
        patronymic = self.patronimic.text().strip()
        phone = self.phone.text().strip()
        rating_text = self.rating.text().strip()

        if len(phone) > 10:
            QMessageBox.critical(self, "Ошибка", "Слишком много символов")
        try:
            rating = int(rating_text)
        except:
            QMessageBox.critical(self, "Ошибка", "Рейтинг должен быть целым числом")

        fio = f"{last_name} {first_name} {patronymic}" if patronymic else f"{last_name} {first_name}"

        return id_type, name, fio, phone, rating

