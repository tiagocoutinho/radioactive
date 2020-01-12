import sys
from radioactive import Dict, qt


def test_qt():
    from PyQt5 import Qt
    app = Qt.QApplication([])
    state = Dict(foo='foo', count=1, items=tuple('abcdefg'))

    label_foo = Qt.QLabel()
    edit_foo = Qt.QLineEdit()
    label_count = Qt.QLabel()
    spin_count = Qt.QSpinBox()
    combo_count = Qt.QComboBox()

    qt.connect(label_foo, state, 'foo')
    qt.connect(edit_foo, state, 'foo')
    qt.connect(label_count, state, 'count')
    qt.connect(spin_count, state, 'count')
    qt.connect_combo_box_items(combo_count, state, 'items')
    qt.connect(combo_count, state, 'count')

    assert label_foo.text() == 'foo'
    assert edit_foo.text() == 'foo'
    assert spin_count.value() == 1
    assert label_count.text() == '1'
    assert combo_count.currentIndex() == 1
    assert tuple(combo_count.itemText(i) for i in range(combo_count.count())) == state['items']

    state['foo'] = 'bar'
    assert label_foo.text() == 'bar'
    assert edit_foo.text() == 'bar'
    assert label_count.text() == '1'
    assert spin_count.value() == 1

    state['count'] += 1
    assert label_foo.text() == 'bar'
    assert edit_foo.text() == 'bar'
    assert label_count.text() == '2'
    assert spin_count.value() == 2

