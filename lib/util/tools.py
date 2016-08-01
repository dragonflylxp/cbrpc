#coding=utf-8

import logging
import logging.config


class Log():
    logger = None

    @classmethod
    def set_up(cls, log_cnf):
        logging.config.fileConfig(log_cnf['config_file'])
        Log.logger = logging.getLogger(log_cnf['default_logger'])

    def getLog(self):
        if Log.logger == None:
            Log.logger = logging.getLogger('simple')
        return Log.logger
