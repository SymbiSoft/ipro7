

import sys
import e32
from e32 import _stdo
class Stream(object, ) :

    __module__ = __name__
    def __init__(self):
        self.writebuf = []

        def make_flusher(buf):
            def doflush():
                adding = ''.join(buf)
                try :
                    adding = adding.encode('u8')
                except :
                    pass
                try :
                    f = open('C:\\iPro7_error.log', 'a')
                    f.write(adding)
                    f.close()
                except :
                    pass
                del buf[:]
            return doflush

        self._doflush = make_flusher(self.writebuf)
        self._flushgate = e32.ao_callgate(self._doflush)


    def write(self, obj):
        self.writebuf.append(obj)
        self.flush()


    def writelines(self, list):
        self.write(''.join(list))


    def flush(self):
        if len(self.writebuf) > 0 : 
            if e32.is_ui_thread() : 
                self._doflush()
            else : 
                self._flushgate()
            pass


stream = Stream()
sys.stderr = sys.stdout = stream
_stdo(u'c:\\iPro7_stdo.log')
