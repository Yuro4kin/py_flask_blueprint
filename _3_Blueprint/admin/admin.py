from flask import Blueprint, render_template, request, url_for, redirect, flash, session

# создадим admin-экземпляр класса-Blueprint <class 'flask.blueprints.Blueprint'>
# Параметры Blueprint()
# 'admin' – имя Blueprint, которое будет суффиксом ко всем именам методов, данного модуля;
# __name__ – имя исполняемого модуля, относительно которого будет искаться папка admin и соответствующие подкаталоги;
# template_folder – подкаталог для шаблонов данного Blueprint (необязательный параметр, при его отсутствии берется подкаталог шаблонов приложения);
# static_folder – подкаталог для статических файлов (необязательный параметр, при его отсутствии берется подкаталог static приложения).
# далее регистрируем Blueprint() в основном приложении файле flsite.py
admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')
#                  bp


# пропишем функцию из обработчика login
# session - в сессии создаем и сохраняем следующую запись со значением 1, если эта запись существует, то пользователь зашел в admin панель
def login_admin():
    session['admin_logged'] = 1

# isLogged() - функция проверяет, зашел администратор в admin панель, True - возвращает, если запись admin_logged существует
# False - если запись не существует
def isLogged():
    return True if session.get('admin_logged') else False

# logout_admin() - функция, которая будет удалять из сессии запись admin_logged, с помощью данной ф-ции будем выходить из admin панели
def logout_admin():
    session.pop('admin_logged', None)

menu = [{'url': '.index', 'title': 'Панель'}, {'url': '.logout', 'title': 'Выйти'}]
# Перейдем в модуль admin.py и пропишем декоратор route:
# admin - переменная, ссылка на Blueprint() и зарегистрирована в нашем приложении
# route - создает функцию представления для обработки запроса, главная страница с учетом префикса будет соответствовать адресу
# http://127.0.0.1:5000/admin/
# улучшим обработчик index(), проверим if-если пользователь не залогинился, то мы не будем отображать admin панель, a
# будем перенаправлять пользователя на форму авторизации, далее отобразим панель с шаблоном index.html у шаблона будет отображаться menu b
@admin.route('/')
def index():
#    return "admin"
    if not isLogged():
        return redirect(url_for('.login'))

    return render_template('admin/index.html', menu=menu, title='Админ-панель')

# например добавим возможность авторизации в нашей тестовой панели администрации
# для этого пропишем функцию представления login для авторизации
# if - проверяем, что пришли данные по POST запросу, затем
# if - проверяем верность login-admin и пароля-12345, где при истинности
# будем выполнять авторизацию с помощью функции login_admin() которую проишем позже, далее
# делаем перенаправление на страницу admin панели
# flash - если были какие-то ошибки
# если шаблон не сработает сработает форма авторизации админ панели admin/login.html
# .index - точка означает, что функцию представления index следует брать из текущего Blueprint, а не глобальную из основного WSGI приложения программы
# admin.index эквивалентно записи .index, admin - это имя Blueprint

# сделаем проверку, если-if зарегистрирован, залогинился, то мы перенаправим нашего пользователя на главную страницу .index
# .index - точки означает, что берем ф-цию index из Blueprint и к url будет добавлен префикс /admin - главня страница нашей admin панели
@admin.route('/login', methods=["POST", "GET"])
def login():
    if isLogged():
        return redirect(url_for('.index'))
#                                 index - без точки переход на главную страницу
    if request.method == "POST":
        if request.form['user'] == "admin" and request.form['psw'] == "12345":
            login_admin()
            return redirect(url_for('.index'))
#                               admin.index - эквивалентная запись
#                                  bp.index - эквивалентная запись
        else:
            flash("Неверная пара логин/пароль", "error")

    return render_template('admin/login.html', title='Админ-панель')

# пропишем выход администратора из админ панели
# обработчик - /logout
# logout() - функция представления
# if - проверяем если администратор не вошел в админ панель, то переводим его на страницу login
# иначе, если он авторизован, выполняем удаление из сессии, т.е. выходим из админ-панели logout_admin() и
# перенаправляем-redirect его на страницу авторизации login
# далее создадим шаблон login.html для авторизации
@admin.route('/logout', methods=["POST", "GET"])
def logout():
    if not isLogged():
        return redirect(url_for('.login'))

    logout_admin()

    return redirect(url_for('.login'))