import kitpy as kp

HERE = kp.paths.fd(__file__)
ROOT = kp.paths.dir(HERE)
CONFIG_PATH = kp.paths.join(ROOT, 'config')
DEFAULT_CFG = kp.log.DEFAULT_CFG
DEFAULT_CFG['file']['basename'] = 'kitpy'
Log = kp.Log


class TestLog:
    def test_list_init(self):
        kp.log.clear()
        assert not kp.log.init([], root=ROOT)
        assert Log.STATUS == Log.NOT_INIT

    def test_skip_init(self):
        print()  # pytest new line
        kp.log.clear()
        assert kp.log.init(root=ROOT)
        assert Log.STATUS == Log.BASE
        logger = Log.get_logger('test_skip_init')
        assert logger
        logger.info('OK')

    def test_empty_dict_init(self):
        print()  # pytest new line
        Log.clear()
        assert Log.init({}, root=ROOT)
        assert Log.STATUS == Log.BASE
        logger = Log.get_logger('test_empty_dict_init')
        assert logger
        logger.info('OK')

    def test_cfg_init(self):
        print()  # pytest new line
        Log.clear()
        assert Log.init(DEFAULT_CFG, root=ROOT)
        assert Log.STATUS == Log.INITED
        logger = Log.get_logger('test_cfg_init')
        assert logger
        logger.info('OK')

    def test_from_file(self):
        print()  # pytest new line
        Log.clear()
        cfg = kp.config.load('config.yml', CONFIG_PATH)
        assert Log.init(cfg, ROOT)
        assert Log.STATUS == Log.INITED
        logger = Log.get_logger('test_from_file')
        assert logger
        logger.info('OK')
        logger.warning('warning infomation')
        logger.error('error infomation')

    def test_repeat_init(self):
        print()  # pytest new line
        Log.clear()
        cfg = kp.config.load('config.yml', CONFIG_PATH)
        assert Log.init(cfg, ROOT)
        assert Log.STATUS == Log.INITED
        assert not Log.init(cfg, ROOT)

    def test_repeat_base(self):
        print()  # pytest new line
        Log.clear()
        assert Log.init()
        assert Log.STATUS == Log.BASE
        assert not Log.init()
