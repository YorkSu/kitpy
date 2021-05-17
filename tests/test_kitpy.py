import kitpy as kp

HERE = kp.paths.fd(__file__)
ROOT = kp.paths.dir(HERE)
CONFIG_PATH = kp.paths.join(ROOT, 'config')
CFG = kp.config.load('config.yml', CONFIG_PATH)
kp.log.init(CFG, ROOT)


def log(name: str, msg: str = 'OK'):
    kp.get_logger(name).info(msg)


class TestKitpy:
    def test_singleton(self):
        class Foo(kp.Singleton):
            ...

        a = Foo()
        b = Foo()
        assert a is b
        log('test_singleton')

    def test_config_load(self):
        source = 'config.yml'
        filepath = kp.paths.join(CONFIG_PATH, source)
        assert kp.config.load(filepath) != {}
        log('test_config_load')

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
        log('test_config_dump')

    def test_lazy(self):
        time = kp.lazy.load('time')
        assert time
        assert time.time()
        log('test_lazy')

    def test_utils_times_count(self):
        with kp.Count(show=False) as c:
            s = 0
            for i in range(2 ** 20):
                s += i
        assert c
        assert c.cost
        log('test_utils_times_count')
