import pytest

import radioactive.model

@pytest.mark.parametrize(
    'args', [([], dict(k1='foo', k2='bar')),
             ([dict(k1='foo', k2='bar')], {}),
             ([dict(k1='bla', k2='ble')], dict(k1='foo', k2='bar'))
])
def test_dict(args):
    a, k = args
    state = radioactive.model.Dict(*a, **k)

    assert state['k1'] == 'foo'
    assert state['k2'] == 'bar'
    assert state.get('k1') == 'foo'
    assert state.get('k2') == 'bar'
    assert set(state.keys()) == {'k1', 'k2'}
    assert set(state.values()) == {'foo', 'bar'}
    assert set(state.items()) == {('k1', 'foo'), ('k2', 'bar')}

    calls = []
    def cb(model, key, value):
        calls.append((model, key, value))

    state.connect('k1', cb)

    assert len(calls) == 0
    state['k2'] = 'foo'
    assert len(calls) == 0
    state['k3'] = 'foo'
    assert len(calls) == 0
    state.update(dict(k2='bla', k4='ble'))
    assert len(calls) == 0
    state['k1'] = 'bar'
    assert len(calls) == 1
    assert calls[0] == (state, 'k1', 'bar')
    state.update(dict(k1='bla', k2='ble'))
    assert len(calls) == 2
    assert calls[1] == (state, 'k1', 'bla')

    state.disconnect('k1', cb)
    state['k1'] = 'kaka'
    assert len(calls) == 2


def test_multiple_observers():
    state = radioactive.model.Dict(k1='foo')

    calls1 = []
    def cb1(model, key, value):
        calls1.append((model, key, value))

    calls2 = []
    def cb2(model, key, value):
        calls2.append((model, key, value))

    state.connect('k1', cb1)
    state.connect('k1', cb2)

    state['k1'] = 'bar'

    assert len(calls1) == 1
    assert len(calls2) == 1


def test_bad_observer():
    state = radioactive.model.Dict(k1='foo')

    def cb1(model, key, value):
        1 / 0

    calls2 = []
    def cb2(model, key, value):
        calls2.append((model, key, value))

    calls3 = []
    def cb3():
        calls3.append(None)

    state.connect('k1', cb1)
    state.connect('k1', cb2)
    state.connect('k1', cb3)

    state['k1'] = 'bar'

    assert len(calls2) == 1
    assert len(calls3) == 0
