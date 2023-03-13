from flask import request, render_template, redirect, url_for

from python import services
from python.config import app
from python.serializers import serializer_module, serializer_teacher

#----------------Рендер-страниц-------------


@app.route('/homepage', methods=['GET'])
def start_page():
    return render_template('homepage.html')


@app.route('/registration', methods=['GET'])
def register_page():
    return render_template('registration.html')


@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@app.route('/service', methods=['GET'])
def service_page():
    return render_template('service.html')


@app.route('/exit', methods=['GET'])
def exit_():
    services.exit_()
    return render_template('homepage.html')


@app.route('/teacher', methods=['GET'])
def get_teacher():
    teachers = services.get_teachers()
    return render_template('teachers.html', teachers=teachers)


@app.route('/module', methods=['GET'])
def get_module():
    modules = services.get_modules()
    return render_template('modules.html', modules=modules)


@app.route('/timetable', methods=['GET'])
def timetable_page():
    timetable = services.get_timetable()
    modules = services.get_my_modules()
    return render_template('timetable.html', timetable=timetable, modules=modules)


@app.route('/my-modules', methods=['GET'])
def my_modules_page():
    modules = services.get_my_modules()
    return render_template('my_modules.html', modules=modules)


@app.route('/my-lessons', methods=['GET'])
def my_lessons_page():
    lessons = services.get_my_lessons()
    return render_template('my_lessons.html', lessons=lessons)


@app.route('/timetable-admin', methods=['GET'])
def timetable_admin_page():
    teachers = services.get_teachers()
    auditoriums = services.get_auditoriums()
    return render_template('timetable_admin.html', teachers=teachers, auditoriums=auditoriums)


@app.route('/teacher-admin', methods=['GET'])
def teacher_admin_page():
    return render_template('teacher_admin.html')


@app.route('/module-admin', methods=['GET'])
def module_admin_page():
    return render_template('module_admin.html')


@app.route('/service-admin', methods=['GET'])
def service_admin_page():
    return render_template('service_admin.html')

#-----------------------Выгрузка-данных---------


@app.route('/get-teachers', methods=['GET'])
def get_teachers_to_excel():
    teachers = services.get_teachers()
    services.to_xlsx(teachers, serializer_teacher, 'teachers.xlsx')
    return get_teacher()


@app.route('/get-modules', methods=['GET'])
def get_modules_to_excel():
    modules = services.get_modules()
    services.to_xlsx(modules, serializer_module, 'modules.xlsx')
    return get_module()


@app.route('/get-teachers-json', methods=['GET'])
def get_teachers_to_json():
    teachers = services.get_teachers()
    services.to_json(teachers, serializer_teacher, 'teachers.json')
    return get_teacher()


@app.route('/get-modules-json', methods=['GET'])
def get_modules_to_json():
    modules = services.get_modules()
    services.to_json(modules, serializer_module, 'modules.json')
    return get_module()

#------------------Действия-на-страницах----------


# регистрация
@app.route('/register', methods=['POST'])
def registration():
    student = request.form
    services.register_service(student)
    return render_template('login.html')


# вход
@app.route('/login_', methods=['POST'])
def login():
    name = request.form.get("name")
    password_ = request.form.get("password_")
    service = services.login_service(name, password_)
    if service == 1:
         return render_template('service.html')
    elif service == 2:
        return render_template('service_admin.html')
    return render_template('login.html')


@app.route('/buy-module', methods=['POST'])
def buy_module():
    id = int(request.form.get("id"))
    quantity = request.form.get("quantity")
    services.buy_module_(id, quantity)
    return get_module()


@app.route('/sign-up-lesson', methods=['POST'])
def lesson():
    id_module = int(request.form.get("id_module"))
    id_lesson = int(request.form.get("id_lesson"))
    if services.sign_up_lesson(id_lesson, id_module):
        return timetable_page()
    else:
        return render_template('timetable_problem.html')


@app.route('/timetable-admin-add', methods=['POST'])
def timetable_admin_add():
    time_ = request.form.get("time_")
    date_ = request.form.get("date_")
    id_teacher = request.form.get("id_teacher")
    id_cabinet = request.form.get("id_cabinet")
    type_ = request.form.get("type")
    services.timetable_add(time_, date_, id_teacher, id_cabinet, type)
    return render_template('timetable_admin.html')


@app.route('/teacher-admin-add', methods=['POST'])
def teacher_admin_add():
    teacher = request.form
    services.teacher_add(teacher)
    return render_template('teacher_admin.html')


@app.route('/module-admin-add', methods=['POST'])
def module_admin_add():
    module = request.form
    services.module_add(module)
    return render_template('module_admin.html')