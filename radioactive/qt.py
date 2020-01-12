import sys


QT = None
QT_LIST = ['PyQt5', 'PySide2', 'PyQt4', 'PySide']


def __import_qt():
    for qt in QT_LIST:
        try:
            return __import__(qt)
        except ModuleNotFoundError:
            continue


def __get_qt():
    for qt in QT_LIST:
        mod = sys.modules.get(qt)
        if mod is not None:
            return mod
    else:
        return __import_qt()


def Qt():
    global QT
    if QT is None:
        import sys
        qt = __get_qt()
        name = qt.__name__
        QT = __import__(f'{name}.Qt', fromlist=(name,))
    return QT


def connect_property(qobject, prop, model, key, adapter=str):
    def update(model, key, value):
        qobject.setProperty(prop, adapter(value))
    model.connect(key, update, weak=False)
    update(model, key, model[key])


def connect_lineedit(editor, model, key):
    def update_model(t):
        model[key] = t
    editor.textChanged.connect(update_model)
    connect_property(editor, 'text', model, key)


def connect_spinbox(spin, model, key):
    def update_model(t):
        model[key] = t
    adapter = float if isinstance(spin, Qt().QDoubleSpinBox) else int
    spin.valueChanged.connect(update_model)
    connect_property(spin, 'value', model, key, adapter=adapter)


def connect(widget, model, key):
    qt = Qt()
    if isinstance(widget, qt.QLabel):
        return connect_property(widget, 'text', model, key)
    elif isinstance(widget, qt.QLineEdit):
        return connect_lineedit(widget, model, key)
    elif isinstance(widget, qt.QSpinBox):
        return connect_spinbox(widget, model, key)
