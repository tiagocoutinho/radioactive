
QT = None
def Qt():
    global QT
    if QT is None:
        import sys
        get = sys.modules.get
        qt = get('PyQt5', get('PySide2', get('PyQt4', get('PySide'))))
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
