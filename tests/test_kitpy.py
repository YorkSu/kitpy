import kitpy as kp

HERE = kp.paths.fd(__file__)
ROOT = kp.paths.dir(HERE)
CONFIG_PATH = kp.paths.join(ROOT, 'config')


class TestKitpy:
    def test_singleton(self):
        class Foo(kp.Singleton):
            ...

        a = Foo()
        b = Foo()
        assert a is b

    def test_config_load(self):
        source = 'config.yml'
        filepath = kp.paths.join(CONFIG_PATH, source)
        assert kp.config.load(filepath) != {}

    def test_config_dump(self):
        source = 'test.yml'
        cfg = {'test': {
            'foo': 'bar',
            'num': 123,
            'bool': True,
            'fake_bool': 'true',
        }}
        filepath = kp.paths.join(CONFIG_PATH, source)
        if kp.paths.exists(filepath):
            kp.paths.remove(filepath)
        assert kp.config.dump(cfg, filepath)
        kp.paths.remove(filepath)

    def test_lazy(self):
        time = kp.lazy.load('time')
        assert time
        assert time.time()

    def test_utils_times_count(self):
        with kp.Count(show=False) as c:
            s = 0
            for i in range(2 ** 20):
                s += i
        assert c
        assert c.cost
