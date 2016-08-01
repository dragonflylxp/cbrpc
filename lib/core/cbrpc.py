#encoding=utf-8

import traceback
import msgpackrpc
from util.tools import Log
logger = Log().getLog()

class CBClient(msgpackrpc.Client):

    def __init__(self, host, port):
        super(CBClient, self).__init__(msgpackrpc.Address(host, port))

    def call(self, method, *args):
        try:
            return super(CBClient, self).call(method, *args)
        except Exception as e: #捕获服务端抛出的异常
            logger.error(traceback.format_exc())

    """
    def on_connect_failed(self):
        print 'connect faild callback!'

    def on_timeout(self):
        print 'time out callback'

    def on_response(self):
        print 'response callback'
    """


class CBServer(msgpackrpc.Server):

    def __init__(self, rpcobj, port, ips="127.0.0.1"):
        super(CBServer, self).__init__(rpcobj)
        self.listen(msgpackrpc.Address(ips,port))

    def current_ioloop(self):
        return self._loop._ioloop
