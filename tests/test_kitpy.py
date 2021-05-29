import kitpy as kp


HERE = kp.path.fd(__file__)
ROOT = kp.path.dir(HERE)
CONFIG_PATH = kp.path.join(ROOT, 'config')


def log_ok(name: str, msg: str = 'OK'):
    Log.get_logger(name).info(msg)


class TestKitpy:
    def test_singleton(self):
        class Foo(kp.Singleton):
            ...
        a = Foo()
        b = Foo()
        assert a is b

    def test_flags(self):
        f = kp.Flags()
        assert f is kp.FLAGS
        assert f.not_exist is None
        assert f.get('not_exist') is None
        assert f.get('not_exist', 1) == 1
        f.foo = 1
        assert f.foo == 1
        assert f.get('foo') == 1
        f.set('foo', 2)
        assert f.foo == 2

    def test_config_json_load(self):
        source = kp.path.join(CONFIG_PATH, 'demo.json')
        data1 = kp.config.load(source)
        data2 = kp.config.JsonHandler(source).load()
        assert data1
        assert data2
        assert data1 == data2

    def test_config_json_dump(self):
        source = kp.path.join(CONFIG_PATH, 'demo.json')
        data1 = {'test': 'abc'}
        data2 = kp.config.load(source)
        kp.config.dump(source, data1)
        assert data1 == kp.config.load(source)
        kp.config.JsonHandler(source).dump(data2)
        assert data2 == kp.config.load(source)

    def test_convert_dict2dict(self):
        data = {
            'a': 1,
            'obj': {'b': 2},
            'li': ['abc', 'def'],
            'objs': [{'c': 3}, {'d': 4}]
        }
        obj = kp.dict2ad(data)
        print(obj)
        assert obj.a == 1
        assert isinstance(obj.obj, kp.convert.AdvancedDict)
        assert obj.obj.b == 2
        assert obj.li[0] == 'abc'
        assert isinstance(obj.objs[0], kp.convert.AdvancedDict)
        assert obj.objs[0].c == 3
