from PyQt5 import QtCore, QtGui, QtWidgets
import json

# Функции для работы с JSON
def load_movies():
    try:
        with open('movies.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_movies(movies):
    with open('movies.json', 'w', encoding='utf-8') as file:
        json.dump(movies, file, ensure_ascii=False, indent=4)

def load_users():
    try:
        with open('users.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_users(users):
    with open('users.json', 'w', encoding='utf-8') as file:
        json.dump(users, file, ensure_ascii=False, indent=4)

# Класс для интерфейса
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)



        # Кнопка логина
        self.login_button = QtWidgets.QPushButton("Войти / Зарегистрироваться")
        self.login_button.setStyleSheet("background-color: #2196F3; color: white; font-size: 20px; padding: 15px;")
        self.login_button.clicked.connect(self.open_login_window)
        main_layout.addWidget(self.login_button)

        self.history_button = QtWidgets.QPushButton("Моя история")
        self.history_button.setStyleSheet("background-color: #2196F3; color: white; font-size: 20px; padding: 15px;")
        self.history_button.clicked.connect(self.show_user_history)
        main_layout.addWidget(self.history_button)

        # Кнопка добавления фильма
        self.add_movie_button = QtWidgets.QPushButton("Добавить фильм")
        self.add_movie_button.setStyleSheet("background-color: #2196F3; color: white; font-size: 20px; padding: 15px;")
        self.add_movie_button.clicked.connect(self.add_movie)
        main_layout.addWidget(self.add_movie_button)

        # Кнопка удаления фильма
        self.delete_movie_button = QtWidgets.QPushButton("Удалить фильм")
        self.delete_movie_button.setStyleSheet("background-color: #2196F3; color: white; font-size: 20px; padding: 15px;")
        self.delete_movie_button.clicked.connect(self.delete_movie)
        main_layout.addWidget(self.delete_movie_button)

        # Список фильмов
        self.movie_list = QtWidgets.QListWidget(self.centralwidget)
        self.movie_list.setStyleSheet("font-size: 25px; padding: 25px; background-color: #f0f0f0; border: 1px solid #ccc;")
        self.movie_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.movie_list.setSpacing(30)
        main_layout.addWidget(self.movie_list)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Загружаем фильмы
        self.load_movies_to_ui()

        self.current_user = None

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Movie Manager"))

    def load_movies_to_ui(self):
        self.movie_list.clear()
        movies = load_movies()
        for movie in movies:
            item = QtWidgets.QListWidgetItem()
            item.setData(QtCore.Qt.UserRole, movie['id'])

            movie_widget = QtWidgets.QWidget()
            movie_layout = QtWidgets.QVBoxLayout(movie_widget)

            title_label = QtWidgets.QLabel(movie['title'])
            title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333;")
            movie_layout.addWidget(title_label)

            sessions_layout = QtWidgets.QHBoxLayout()
            for session in movie['sessions']:
                session_button = QtWidgets.QPushButton(session['time'])
                # Передаем данные о сеансе и фильме
                session_button.clicked.connect(lambda checked, session=session, movie_id=movie['id']: self.open_booking_window(session, movie_id))
                sessions_layout.addWidget(session_button)

            movie_layout.addLayout(sessions_layout)
            movie_layout.setContentsMargins(20, 20, 20, 20)
            movie_widget.setLayout(movie_layout)

            item.setSizeHint(movie_widget.sizeHint())
            self.movie_list.addItem(item)
            self.movie_list.setItemWidget(item, movie_widget)

    def open_login_window(self):
        login_window = LoginWindow(self)
        login_window.exec_()

    def update_user_info(self, user):
        self.current_user = user
        self.login_button.setText(f"Вы вошли как: {user['name']}")

    def open_booking_window(self, session, movie_id):
        if not self.current_user:
            QtWidgets.QMessageBox.warning(None, "Ошибка", "Пожалуйста, войдите в систему!")
            return

        # Создаем окно бронирования для выбранного сеанса
        booking_window = BookingWindow(session, movie_id, self.current_user)
        booking_window.exec_()  # Окно бронирования откроется, но главное окно останется открытым

    def add_movie(self):
        movie_name, ok = QtWidgets.QInputDialog.getText(None, "Добавить фильм", "Введите название фильма:")
        if ok and movie_name:
            new_movie = {
                'id': len(load_movies()) + 1,
                'title': movie_name,
                'sessions': [
                    {'time': '10:00', 'reserved_seats': [], 'users': []},
                    {'time': '13:00', 'reserved_seats': [], 'users': []},
                    {'time': '16:00', 'reserved_seats': [], 'users': []},
                    {'time': '19:00', 'reserved_seats': [], 'users': []},
                    {'time': '22:00', 'reserved_seats': [], 'users': []}
                ]
            }
            movies = load_movies()
            movies.append(new_movie)
            save_movies(movies)
            self.load_movies_to_ui()

    def delete_movie(self):
        selected_item = self.movie_list.currentItem()
        if selected_item:
            movie_id = selected_item.data(QtCore.Qt.UserRole)
            movies = load_movies()
            movie_to_delete = next((movie for movie in movies if movie['id'] == movie_id), None)

            if movie_to_delete:
                movies.remove(movie_to_delete)
                save_movies(movies)
                self.load_movies_to_ui()
                QtWidgets.QMessageBox.information(None, "Удаление фильма", "Фильм был удален успешно!")
            else:
                QtWidgets.QMessageBox.warning(None, "Ошибка", "Фильм не найден!")
        else:
            QtWidgets.QMessageBox.warning(None, "Ошибка", "Пожалуйста, выберите фильм для удаления!")

    def show_user_history(self):
        if not self.current_user:
            QtWidgets.QMessageBox.warning(None, "Ошибка", "Пожалуйста, войдите в систему!")
            return

        # Получаем список купленных билетов пользователя
        tickets = self.current_user.get('purchased_tickets', [])
        if not tickets:
            QtWidgets.QMessageBox.information(None, "История билетов", "Вы еще не купили ни одного билета.")
            return

        # Формируем строку для отображения
        ticket_history = "\n".join(tickets)
        QtWidgets.QMessageBox.information(None, "Моя история", f"Ваши билеты:\n{ticket_history}")


class AddMovieWindow(QtWidgets.QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Добавить фильм")
        self.setFixedSize(400, 250)

        layout = QtWidgets.QVBoxLayout(self)

        self.title_input = QtWidgets.QLineEdit(self)
        self.title_input.setPlaceholderText("Название фильма")
        layout.addWidget(self.title_input)

        self.add_button = QtWidgets.QPushButton("Добавить", self)
        self.add_button.clicked.connect(self.add_movie)
        layout.addWidget(self.add_button)

    def add_movie(self):
        title = self.title_input.text()

        if not title:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите название фильма!")
            return

        movies = load_movies()
        new_movie = {
            'id': len(movies) + 1,  # Уникальный ID
            'title': title,
            'sessions': []
        }
        movies.append(new_movie)
        save_movies(movies)
        self.main_window.load_movies_to_ui()  # Обновляем список фильмов
        self.accept()

class RemoveMovieWindow(QtWidgets.QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Удалить фильм")
        self.setFixedSize(400, 250)

        layout = QtWidgets.QVBoxLayout(self)

        self.movie_select = QtWidgets.QComboBox(self)
        layout.addWidget(self.movie_select)

        self.remove_button = QtWidgets.QPushButton("Удалить", self)
        self.remove_button.clicked.connect(self.remove_movie)
        layout.addWidget(self.remove_button)

        self.load_movies_to_select()

    def load_movies_to_select(self):
        movies = load_movies()
        self.movie_select.clear()
        for movie in movies:
            self.movie_select.addItem(movie['title'], movie['id'])

    def remove_movie(self):
        selected_movie_id = self.movie_select.currentData()

        movies = load_movies()
        movies = [movie for movie in movies if movie['id'] != selected_movie_id]
        save_movies(movies)
        self.main_window.load_movies_to_ui()  # Обновляем список фильмов
        self.accept()

class LoginWindow(QtWidgets.QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Логин / Регистрация")
        self.setFixedSize(400, 250)

        layout = QtWidgets.QVBoxLayout(self)

        self.username_input = QtWidgets.QLineEdit(self)
        self.username_input.setPlaceholderText("Имя пользователя")
        layout.addWidget(self.username_input)

        self.password_input = QtWidgets.QLineEdit(self)
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.captcha_checkbox = QtWidgets.QCheckBox("Докажите, что вы не робот", self)
        layout.addWidget(self.captcha_checkbox)

        self.login_button = QtWidgets.QPushButton("Войти", self)
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.register_button = QtWidgets.QPushButton("Зарегистрироваться", self)
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Проверка на капчу
        if not self.captcha_checkbox.isChecked():
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Пожалуйста, подтвердите, что вы не робот!")
            return

        users = load_users()
        user = next((u for u in users if u['name'] == username and u['password'] == password), None)

        if user:
            self.main_window.update_user_info(user)
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Неверное имя пользователя или пароль!")

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля!")
            return

        # Проверка на капчу
        if not self.captcha_checkbox.isChecked():
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Пожалуйста, подтвердите, что вы не робот!")
            return

        users = load_users()
        if any(u['name'] == username for u in users):
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Пользователь с таким именем уже существует!")
            return

        new_user = {'name': username, 'password': password, 'purchased_tickets': []}
        users.append(new_user)
        save_users(users)
        self.main_window.update_user_info(new_user)
        self.accept()

class BookingWindow(QtWidgets.QDialog):
    def __init__(self, session, movie_id, current_user):
        super().__init__()
        self.setWindowTitle(f"Бронирование билетов - {session['time']}")
        self.setFixedSize(600, 400)

        self.session = session
        self.movie_id = movie_id
        self.current_user = current_user
        self.selected_seats = []  # Выбранные места

        layout = QtWidgets.QVBoxLayout(self)

        # Заголовок
        self.info_label = QtWidgets.QLabel("Выберите места для бронирования")
        self.info_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.info_label)

        # Сетка мест
        self.seat_grid = QtWidgets.QGridLayout()
        self.buttons = {}  # Хранение кнопок мест

        rows = ["A", "B", "C", "D", "E"]
        seats_per_row = 10

        for row_index, row in enumerate(rows):
            for seat_num in range(1, seats_per_row + 1):
                seat_name = f"{row}{seat_num}"
                button = QtWidgets.QPushButton(seat_name)
                button.setCheckable(True)
                button.setStyleSheet(self.get_seat_style(seat_name))
                button.clicked.connect(lambda checked, seat=seat_name: self.toggle_seat(seat))
                self.buttons[seat_name] = button
                self.seat_grid.addWidget(button, row_index, seat_num - 1)

        layout.addLayout(self.seat_grid)

        # Кнопка подтверждения
        self.confirm_button = QtWidgets.QPushButton("Подтвердить бронирование")
        self.confirm_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px; padding: 10px;")
        self.confirm_button.clicked.connect(self.confirm_booking)
        layout.addWidget(self.confirm_button)

        # Кнопка Муви Инфо
        self.movie_info_button = QtWidgets.QPushButton("Муви Инфо")
        self.movie_info_button.setStyleSheet("background-color: #2196F3; color: white; font-size: 16px; padding: 10px;")
        self.movie_info_button.clicked.connect(self.show_movie_info)
        layout.addWidget(self.movie_info_button)

        self.load_reserved_seats()

    def get_seat_style(self, seat_name):
        """ Стиль для кнопки места: зарезервированные места будут серыми """
        return "background-color: lightgray; font-size: 14px; padding: 5px;" if seat_name in self.session['reserved_seats'] else "background-color: #2196F3; color: white; font-size: 14px; padding: 5px;"

    def toggle_seat(self, seat):
        """ Добавляет/убирает место из выбранных """
        if seat in self.session['reserved_seats']:
            QtWidgets.QMessageBox.warning(self, "Ошибка", f"Место {seat} уже забронировано!")
            return

        if seat in self.selected_seats:
            self.selected_seats.remove(seat)
            self.buttons[seat].setStyleSheet("background-color: #2196F3; color: white; font-size: 14px; padding: 5px;")
        else:
            self.selected_seats.append(seat)
            self.buttons[seat].setStyleSheet("background-color: #FFEB3B; color: black; font-size: 14px; padding: 5px;")

    def load_reserved_seats(self):
        """ Загружает уже забронированные места """
        for seat_name in self.session['reserved_seats']:
            if seat_name in self.buttons:
                self.buttons[seat_name].setStyleSheet("background-color: lightgray; font-size: 14px; padding: 5px;")
                self.buttons[seat_name].setEnabled(False)

    def confirm_booking(self):
        """ Подтверждает бронирование выбранных мест """
        if not self.selected_seats:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите хотя бы одно место!")
            return

        # Обновляем данные
        self.session['reserved_seats'].extend(self.selected_seats)
        # Добавляем информацию о пользователе, который купил билеты
        self.session['users'].append({
            'user': self.current_user['name'],
            'seats': self.selected_seats
        })
        self.current_user['purchased_tickets'].extend(
            [f"{self.session['time']} - {seat}" for seat in self.selected_seats])

        # Сохраняем обновленные данные в JSON
        movies = load_movies()
        for movie in movies:
            if movie['id'] == self.movie_id:
                for sess in movie['sessions']:
                    if sess['time'] == self.session['time']:
                        sess['reserved_seats'] = self.session['reserved_seats']
                        sess['users'] = self.session['users']  # Обновляем список пользователей
                        break
                break
        save_movies(movies)

        users = load_users()
        for user in users:
            if user['name'] == self.current_user['name']:
                user['purchased_tickets'] = self.current_user['purchased_tickets']
                break
        save_users(users)

        QtWidgets.QMessageBox.information(self, "Успешно", "Ваши билеты забронированы!")
        self.accept()

    def show_movie_info(self):
        """ Открывает окно с информацией о фильме """
        movie_info_window = MovieInfoWindow(self.session['reserved_seats'], self.session['users'])
        movie_info_window.exec_()


class MovieInfoWindow(QtWidgets.QDialog):
    def __init__(self, reserved_seats, users, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Информация о фильме")
        self.setFixedSize(400, 300)

        self.reserved_seats = reserved_seats
        self.users = users

        layout = QtWidgets.QVBoxLayout(self)

        # Лейблы для статистики
        self.stats_label_total_tickets = QtWidgets.QLabel("Всего куплено билетов: 0")
        self.stats_label_total_money = QtWidgets.QLabel("Денег в кассе: 0 сом")
        self.stats_label_total_users = QtWidgets.QLabel("Пользователи купили билеты: ")

        # Добавляем лейблы статистики в layout
        layout.addWidget(self.stats_label_total_tickets)
        layout.addWidget(self.stats_label_total_money)
        layout.addWidget(self.stats_label_total_users)

        # Обновляем статистику
        self.update_statistics()

    def update_statistics(self):
        # Подсчитываем количество купленных билетов
        total_tickets = len(self.reserved_seats)
        total_money = total_tickets * 200  # Стоимость одного билета 200 сом

        # Получаем уникальных пользователей
        users = set(user['user'] for user in self.users)
        total_users = len(users)

        # Обновляем текст статистики
        self.stats_label_total_tickets.setText(f"Всего куплено билетов: {total_tickets}")
        self.stats_label_total_money.setText(f"Денег в кассе: {total_money} сом")
        self.stats_label_total_users.setText(f"Пользователи купили билеты: {', '.join(users)}")


# Запуск приложения
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
