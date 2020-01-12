from PyQt5 import Qt
from radioactive import Dict
from radioactive import qt


def demo():
    data = dict(name='Hello!', version='1.2.3', count='1')
    state = Dict(data)
    state['title'] = f'{state["name"]} - {state["version"]}'
    def title(model, key, value):
        model['title'] = f'{model["name"]} - {model["version"]}'
    state.connect('name', title)
    state.connect('version', title)

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

    for i in range(2, 4):
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
    layout.addWidget(btn, 4, 0, 1, 3)
    qt.connect_property(w, 'windowTitle', state, 'title')

    w.show()
    app.exec_()


if __name__ == '__main__':
    demo()
