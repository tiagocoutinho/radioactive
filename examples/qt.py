from PyQt5 import Qt
from radioactive import Dict
from radioactive import qt


def demo():
    data = dict(name='Hello!', version='1.2.3', count='1', fg_color='blue',
                cars=('Ferrari', 'Porche', 'Maserati', 'Rolls Royce'),
                active_car_index=2)
    state = Dict(data)
    state['title'] = f'{state["name"]} - {state["version"]}'
    def title(model, key, value):
        model['title'] = f'{model["name"]} - {model["version"]}'
    def fg_style(model, key, value):
        model['fg_style'] = f'color: {value}'
    state['active_car'] = state['cars'][state['active_car_index']]
    def active_car(model, key, value):
        model['active_car'] = model['cars'][value]
    state.connect('name', title)
    state.connect('version', title)
    state.connect('fg_color', fg_style)
    state.connect('active_car_index', active_car)

    app = Qt.QApplication([])
    w = Qt.QWidget()
    layout = Qt.QGridLayout(w)

    labelName = Qt.QLabel()
    editorName = Qt.QLineEdit()
    layout.addWidget(Qt.QLabel('Name:'), 0, 0)
    layout.addWidget(editorName, 0, 1)
    layout.addWidget(labelName, 0, 2)
    qt.connect(labelName, state, 'name')
    qt.connect(editorName, state, 'name')

    labelCount = Qt.QLabel()
    spinCount = Qt.QSpinBox()
    layout.addWidget(Qt.QLabel('Count:'), 1, 0)
    layout.addWidget(spinCount, 1, 1)
    layout.addWidget(labelCount, 1, 2)
    qt.connect(labelCount, state, 'count')
    qt.connect(spinCount, state, 'count')

    labelFg = Qt.QLabel()
    editFg = Qt.QLineEdit()
    layout.addWidget(Qt.QLabel('Fg:'), 2, 0)
    layout.addWidget(editFg, 2, 1)
    layout.addWidget(labelFg, 2, 2)
    qt.connect(labelFg, state, 'fg_color')
    qt.connect(editFg, state, 'fg_color')
    qt.connect_property(labelFg, 'styleSheet', state, 'fg_style')
    qt.connect_property(editFg, 'styleSheet', state, 'fg_style')

    labelCar = Qt.QLabel()
    comboCar = Qt.QComboBox()
#    comboCar.addItems(state['cars'])
    layout.addWidget(Qt.QLabel('Car:'), 3, 0)
    layout.addWidget(comboCar, 3, 1)
    layout.addWidget(labelCar, 3, 2)
    qt.connect(labelCar, state, 'active_car')
    qt.connect_combo_box_items(comboCar, state, 'cars')
    qt.connect(comboCar, state, 'active_car_index')

    for i in range(4, 6):
        labelVersion = Qt.QLabel()
        editorVersion = Qt.QLineEdit()
        layout.addWidget(Qt.QLabel('Version:'), i, 0)
        layout.addWidget(editorVersion, i, 1)
        layout.addWidget(labelVersion, i, 2)
        qt.connect(labelVersion, state, 'version')
        qt.connect(editorVersion, state, 'version')

    def reset():
        state.update(data)

    btn = Qt.QPushButton('Reset')
    btn.clicked.connect(reset)
    layout.addWidget(btn, 5, 0, 1, 3)
    qt.connect_property(w, 'windowTitle', state, 'title')

    w.show()
    app.exec_()


if __name__ == '__main__':
    demo()
