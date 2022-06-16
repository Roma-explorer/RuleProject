from PyQt5 import QtWidgets as qtw


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance, True


def not_all_filled():
    message = qtw.QMessageBox(icon=qtw.QMessageBox.Warning, text='Не все поля заполнены')
    message.show()
    return
