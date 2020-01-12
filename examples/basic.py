from radioactive import Dict


def demo():
    state = Dict(name='foo', version='1.2.3')

    CB = []
    def cb(model, key, value):
        print(f'model[{key}] = {value}')
        CB.append(1)
    state.subscribe('name', cb)

    state['name'] = 'bar'
    assert len(CB) == 1


if __name__ == '__main__':
    demo()

