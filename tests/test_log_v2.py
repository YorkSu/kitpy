import kitpy as kp
import kitpy.log_v2 as log_v2

HERE = kp.paths.fd(__file__)
ROOT = kp.paths.dir(HERE)
CONFIG_PATH = kp.paths.join(ROOT, 'config')
DEFAULT_CFG = log_v2.DEFAULT_CFG
DEFAULT_CFG['file']['basename'] = 'kitpy'
Log = log_v2.Log
log = Log({}, root=ROOT)


def log_ok(name: str, msg: str = 'OK'):
    Log.get_logger(name).info(msg)


class TestLog:
    def test_list_init(self):
        print()  # pytest new line
        log.set_cfg([])
        log.clear()
        assert log.init()
        assert Log.is_status(Log.BASE)

    def test_empty_dict_init(self):
        print()  # pytest new line
        log.set_cfg({})
        log.clear()
        assert log.init()
        assert Log.is_status(Log.BASE)
        log_ok('test_empty_dict_init')

    def test_repeat_base(self):
        print()  # pytest new line
        log.set_cfg({})
        log.clear()
        assert log.init()
        assert Log.is_status(Log.BASE)
        assert not log.init()
        log_ok('test_repeat_base')

    def test_cfg_init(self):
        print()  # pytest new line
        log.set_cfg(DEFAULT_CFG)
        log.clear()
        assert log.init()
        assert Log.is_status(Log.INITED)
        log_ok('test_cfg_init')

    def test_from_file(self):
        print()  # pytest new line
        cfg = kp.config.load('config.yml', CONFIG_PATH)
        log.set_cfg(cfg)
        log.clear()
        assert log.init()
        assert Log.is_status(Log.INITED)
        logger = Log.get_logger('test_from_file')
        assert logger
        logger.info('OK')
        logger.warning('warning infomation')
        logger.error('error infomation')

    def test_repeat_init(self):
        print()  # pytest new line
        log.set_cfg(DEFAULT_CFG)
        log.clear()
        assert log.init()
        assert Log.is_status(Log.INITED)
        assert not log.init()
        log_ok('test_repeat_init')
