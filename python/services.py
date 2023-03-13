import json
import xlsxwriter as xlsxwriter
from flask import jsonify
import hashlib
from python import models
from python.models import *
from datetime import datetime

STUDENT_ID = None
ADMIN_ID = None


def where_filters(query, model: models.BaseModel, **filters):
    _filters = [
        getattr(model, key) == value
        for key, value in filters.items() if value is not None
    ]
    if _filters:
        return query.where(*_filters)
    return query


def execute_get_all(model, serializer, **filters):
    query = model.select()
    query = where_filters(query, model, **filters)
    return jsonify([serializer(model) for model in query])


def execute_get_one(pk, model, serializer):
    return serializer(model.select().where(model.id == int(pk)).get())


# создание нового ученика
def register_service(json: dict):
    pas = json["password_"]
    pas = hashlib.sha256(pas.encode('utf-8')).hexdigest()  # хеширование
    j = dict(json)
    j["password_"] = pas
    Student.create(**j)


# вход
def login_service(name_, password):
    password_ = hashlib.sha256(password.encode('utf-8')).hexdigest()

    query = models.Student.select(models.Student.id) \
        .where((models.Student.name_ == name_) & (models.Student.password_ == password_))
    query = [{'id': row.id} for row in query]
    if not query:
        query = models.Admin.select(models.Admin.id) \
            .where((models.Admin.name_ == name_) & (models.Admin.password_ == password_))
        query = [{'id': row.id} for row in query]
        if not query:
            return 3
        global ADMIN_ID
        ADMIN_ID = query[0].get('id')
        return 2
    else:
        global STUDENT_ID
        STUDENT_ID = query[0].get('id')
        return 1


def exit_():
    global STUDENT_ID
    STUDENT_ID = None
    global ADMIN_ID
    ADMIN_ID = None


def get_teachers():
    query = models.Teacher.select()
    execute = list(query)
    return execute


def get_modules():
    query = models.Module.select()
    execute = list(query)
    return execute


def get_timetable():
    query = models.Timetable.select(models.Timetable.id, models.Timetable.date_, models.Timetable.time_,
                                    models.Teacher.name_, models.Teacher.surname, models.Auditorium.number,
                                    models.Auditorium.building, models.Timetable.type_) \
        .join(models.Auditorium, on=(models.Timetable.auditorium == models.Auditorium.id)) \
        .switch(models.Timetable) \
        .join(models.Teacher, on=(models.Timetable.teacher == models.Teacher.id) & models.Timetable.available &
                                 (models.Timetable.date_ >= datetime.today().strftime('%Y-%m-%d')))

    execute = list(query)
    return execute


def get_my_modules():
    query = models.Student_Module.select(models.Module.id, models.Module.name_, models.Student_Module.quantity) \
        .join(models.Module,
              on=((models.Module.id == models.Student_Module.module) & (models.Student_Module.student == STUDENT_ID)))

    execute = list(query)
    return execute


def get_my_lessons():
    query = models.Timetable_Student_Module.select(models.Timetable.date_, models.Timetable.time_, models.Teacher.name_,
                                                   models.Teacher.surname, models.Auditorium.number,
                                                   models.Auditorium.building,
                                                   models.Timetable.type_) \
        .join(models.Timetable, on=(models.Timetable.id == models.Timetable_Student_Module.timetable)) \
        .join(models.Teacher, on=(models.Timetable.teacher == models.Teacher.id)) \
        .switch(models.Timetable) \
        .join(models.Auditorium, on=(models.Timetable.auditorium == models.Auditorium.id)) \
        .join(models.Student_Module, on=(
            (models.Timetable_Student_Module.student_module == models.Student_Module.id) & (
            models.Student_Module.student == STUDENT_ID)))

    execute = list(query)
    return execute


def buy_module_(id: int, quantity):
    j = {'student_id': STUDENT_ID, 'module_id': id, 'quantity': quantity}
    Student_Module.create(**j)


def sign_up_lesson(lesson_id: int, module_id: int):
    query = models.Student_Module.select(models.Student_Module.id) \
        .where((models.Student_Module.student == STUDENT_ID) & (models.Student_Module.module == module_id))
    query = [{'id': row.id} for row in query]
    student_module_id = query[0].get('id')
    j = {'timetable_id': lesson_id, 'student_module_id': student_module_id}
    try:
        models.Timetable_Student_Module.create(**j)
    except:
        return False
    else:
        return True


def get_auditoriums():
    query = models.Auditorium.select()
    execute = list(query)
    return execute


def timetable_add(time_, date_, id_teacher, id_auditorium, type_):
    j = {'available': True, 'time_': time_, 'date_': date_, 'teacher_id': id_teacher, 'id_cabinet': id_auditorium,
         'type_': type_}
    Timetable.create(**j)


def teacher_add(teacher):
    Teacher.create(**teacher)


def module_add(module):
    Module.create(**module)


def to_xlsx(data, serializer, filename):
    my_workbook = xlsxwriter.Workbook(filename)
    my_worksheet = my_workbook.add_worksheet()
    count = 0
    dict1 = [serializer(row) for row in data]
    for tmp in dict1:
        for key, value in tmp.items():
            my_worksheet.write(f'A{count}', key)
            my_worksheet.write(f'B{count}', value)
            count += 1
    my_workbook.close()


def to_json(data, serializer, filename):
    data1 = [serializer(row) for row in data]

    with open(filename, 'w') as f:
        json.dump(data1, f, indent=2, ensure_ascii=False)
