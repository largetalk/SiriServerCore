import thread, time
from ftmsc import qisr
from PluginManager import getAPIKeyForAPI

lock = thread.allocate_lock()

class XunfeiPool(object):
    instance = None
    conn = None
#    session_pool = {}

    class OnlyOne:
        def __init__(self, *args, **kwargs):
            XunfeiPool.conn = qisr.IftQISR(getAPIKeyForAPI('xunfei'))
            XunfeiPool.conn.init()

        def __del__(self):
            XunfeiPool.conn.fini()

    def __init__(self, *args, **kwargs):
        if not XunfeiPool.instance:
            super(XunfeiPool, self).__init__(*args, **kwargs)
            XunfeiPool.instance = XunfeiPool.OnlyOne(*args, **kwargs)
            #self.init_session_pool()

    #def init_session_pool(self):
    #    self.session_pool = {}#key: session, value:{'lastUsedTime':xx, 'isFree':True}
       
    def get_session(self):
        lock.acquire()
        try:
            return XunfeiPool.conn.createSession(grammarList='', params="ssm=1,sub=iat,auf=audio/L16;rate=16000,aue=speex,ent=sms16k,rst=plain,rse=utf8,coding_libs=libspeex.so")

            #print '###############################', XunfeiPool.session_pool.items()
            #for sess, status in XunfeiPool.session_pool.items():
            #    lastTime = status['lastUsedTime']
            #    isFree = status['isFree']
            #    if not isFree and time.time() - lastTime > 5 * 60:
            #        XunfeiPool.session_pool.pop(sess)
            #        continue
            #    if isFree:
            #        XunfeiPool.session_pool.update({sess:{'lastUsedTime':time.time(), 'isFree': False}})
            #        return sess
            #sess = XunfeiPool.conn.createSession(grammarList='', params="ssm=1,sub=iat,auf=audio/L16;rate=16000,aue=speex,ent=sms16k,rst=plain,rse=utf8,coding_libs=libspeex.so")
            #XunfeiPool.session_pool[sess] = {'lastUsedTime':time.time(), 'isFree': False}
            #return sess
        finally:
            lock.release()


    def release_session(self, sess):
        lock.acquire()
        try:
            del sess
            #status = XunfeiPool.session_pool[sess]
            #if status == None:
            #    del sess
            #else:
            #    XunfeiPool.session_pool[sess] = {'lastUsedTime':time.time(), 'isFree': True}
        finally:
            lock.release()


