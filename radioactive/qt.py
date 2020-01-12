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


def connect_label(label, model, key):
    connect_property(label, 'text', model, key)


def connect_line_edit(editor, model, key):
    def update_model(text):
        model[key] = text
    editor.textChanged.connect(update_model)
    connect_property(editor, 'text', model, key)


def connect_spin_box(spin, model, key):
    def update_model(number):
        model[key] = number
    adapter = float if isinstance(spin, Qt().QDoubleSpinBox) else int
    spin.valueChanged.connect(update_model)
    connect_property(spin, 'value', model, key, adapter=adapter)


def connect_combo_box(combo, model, key):
    def update_model(index):
        model[key] = index
    combo.currentIndexChanged[int].connect(update_model)
    connect_property(combo, 'currentIndex', model, key, adapter=int)


def connect_combo_box_items(combo, model, key):
    def update_combo(model, key, value):
        combo.clear()
        combo.addItems(value)
    model.connect(key, update_combo, weak=False)
    update_combo(model, key, model[key])


def connect(widget, model, key):
    qt = Qt()
    if isinstance(widget, qt.QLabel):
        conn = connect_label
    elif isinstance(widget, qt.QLineEdit):
        conn = connect_line_edit
    elif isinstance(widget, qt.QSpinBox):
        conn = connect_spin_box
    elif isinstance(widget, qt.QComboBox):
        conn = connect_combo_box
    return conn(widget, model, key)
