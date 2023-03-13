def serializer_module(model):
    return {
        "name": model.name,
        "pg_description": model.pg_description,
        "quantity": model.quantity,
        "price": model.price
    }


def serializer_teacher(model):
    return {
        "surname": model.surname,
        "name": model.name,
        "education": model.education,
        "exp_teach": model.exp_teach,
        "exp_native": model.exp_native,
        "description": model.description
    }