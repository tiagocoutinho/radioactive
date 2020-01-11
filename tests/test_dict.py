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

    calls = []
    def cb(model, key, value):
        calls.append((model, key, value))

    state.subscribe('k1', cb)

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

    state.unsubscribe('k1', cb)
    state['k1'] = 'kaka'
    assert len(calls) == 2

    
