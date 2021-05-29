import kitpy as kp


HERE = kp.path.fd(__file__)
ROOT = kp.path.dir(HERE)
CONFIG_PATH = kp.path.join(ROOT, 'config')
DEFAULT_CFG = kp.log.DEFAULT_CFG
DEFAULT_CFG['file']['basename'] = 'kitpy'
DEFAULT_CFG['file']['root'] = ROOT
Log = kp.Log
log = Log({})


class TestLog:
    def test_log_list_init(self):
        log.clear()
        log.set_cfg([])
        assert log.init()
        assert Log.is_status(Log.BASE)

    def test_log_empty_dict_init(self):
        log.clear()
        log.set_cfg({})
        assert log.init()
        assert Log.is_status(Log.BASE)

    def test_log_repeat_base(self):
        log.clear()
        log.set_cfg({})
        assert log.init()
        assert Log.is_status(Log.BASE)
        assert not log.init()

    def test_log_cfg_init(self):
        log.clear()
        log.set_cfg(DEFAULT_CFG)
        assert log.init()
        assert Log.is_status(Log.INITED)
        Log.get_logger().info(log.cfg)

    def test_from_file(self):
        source = kp.path.join(CONFIG_PATH, 'config.yml')
        cfg = kp.config.load(source)
        cfg['logging']['file']['root'] = ROOT
        log.clear()
        log.set_cfg(cfg)
        assert log.init()
        assert Log.is_status(Log.INITED)
        logger = Log.get_logger('test_from_file')
        assert logger
        logger.info('OK')
        logger.warning('warning infomation')
        logger.error('error infomation')

    def test_repeat_init(self):
        log.clear()
        log.set_cfg(DEFAULT_CFG)
        assert log.init()
        assert Log.is_status(Log.INITED)
        assert not log.init()

