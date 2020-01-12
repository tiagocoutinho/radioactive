from PyQt5 import Qt
from radioactive import Dict, qt


def test_qt():
    app = Qt.QApplication([])
    state = Dict(foo='foo', count=55)

    label_foo = Qt.QLabel()
    edit_foo = Qt.QLineEdit()
    label_count = Qt.QLabel()
    spin_count = Qt.QSpinBox()

    qt.connect(label_foo, state, 'foo')
    qt.connect(edit_foo, state, 'foo')
    qt.connect(label_count, state, 'count')
    qt.connect(spin_count, state, 'count')

    assert label_foo.text() == 'foo'
    assert edit_foo.text() == 'foo'
    assert label_count.text() == '55'
    assert spin_count.value() == 55

    state['foo'] = 'bar'
    assert label_foo.text() == 'bar'
    assert edit_foo.text() == 'bar'
    assert label_count.text() == '55'
    assert spin_count.value() == 55

    state['count'] += 5
    assert label_foo.text() == 'bar'
    assert edit_foo.text() == 'bar'
    assert label_count.text() == '60'
    assert spin_count.value() == 60

