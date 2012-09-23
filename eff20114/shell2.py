#-*- encoding:utf-8 -*-
#Made by zl@sun

import appuifw as ui
import sys
import e32
import os
sys.path.append(os.getcwd()[0]+":\\system\\inspect2\\")
try:
  from key_codes import EKeySelect
  from key_codes import EKeyEnter
except :
  EKeySelect = 63557
  EKeyEnter = 13
_text = ui.Text()
class NameSpace(object):
  __module__ = __name__

  def __init__(s):
    s.namespace = {'__builtins__': __builtins__,
     '__name__': '__main__'}



  def __del__(s):
    s.namespace.clear()

def add(text):
  _text.add(text)
  write_file(text)

class Stream(object):
  __module__ = __name__

  def __init__(s):
    s.lock = e32.Ao_lock()
    s.text = _text
    s.text.font = ('dense',
     16)
    s.text.bind(EKeySelect, s.lock_signal)
    s.text.bind(EKeyEnter, lambda:e32.ao_sleep(0, s.lock.signal))
    s.savestdin = sys.stdin
    s.savestdout = sys.stdout
    s.writebuf = []

    def make_flusher(text, buf):

      def doflush():
        try:
          add(unicode(''.join(buf)))
        except:
          import traceback
          add(unicode(''.join(traceback.format_exception(*sys.exc_info())), 'u8', 'ignore'))
        del buf[:]
        if (text.len() > 5000):
          text.delete(0, (text.len() - 1000))


      return doflush


    s._Stream__doflush = make_flusher(s.text, s.writebuf)
    s._Stream__flushgate = e32.ao_callgate(s._Stream__doflush)



  def __del__(s):
    sys.stdin = s.savestdin
    sys.stdout = s.savestdout
    s.text = None



  def write(s, text):
    s.writebuf.append(text)
    s.flush()



  def writelines(s, list):
    s.write(''.join(list))



  def flush(s):
    if (len(s.writebuf) > 0):
      if e32.is_ui_thread():
        s._Stream__doflush()
      else:
        s._Stream__flushgate()



  def lock_signal(s):
    s.write(u'\n')
    s.lock.signal()



  def readline(s):
    if (not e32.is_ui_thread()):
      raise IOError('Cannot call readline from non-UI thread')
    old_pos = s.text.get_pos()
    old_len = s.text.len()
    s.lock.wait()
    current_pos = s.text.get_pos()
    current_len = s.text.len()
    if ((current_pos <= old_pos) | ((current_len - old_len) != (current_pos - old_pos))):
      s.text.set_pos(s.text.len())
      s.write(u'\n')
      user_input = ''
    else:
      user_input = s.text.get(old_pos, ((current_pos - old_pos) - 1))
    return user_input.encode('u8')



class StdErr(object):
  __module__ = __name__

  def __init__(s):
    s.text = _text
    s.savestderr = sys.stderr
    s.writebuf = []

    def make_flusher(text, buf):

      def doflush():
        try:
          exc_info = ''.join(buf)
          add(unicode(exc_info, 'u8', 'ignore'))
        except:
          import traceback
          add(unicode(''.join(traceback.format_exception(*sys.exc_info())), 'u8', 'ignore'))
        del buf[:]
        if (text.len() > 5000):
          text.delete(0, (text.len() - 1000))


      return doflush


    s._StdErr__doflush = make_flusher(s.text, s.writebuf)
    s._StdErr__flushgate = e32.ao_callgate(s._StdErr__doflush)



  def __del__(s):
    sys.stderr = s.savestderr



  def write(s, obj):
    s.writebuf.append(obj)
    s.flush()


  def writelines(s, list):
    s.write(''.join(list))



  def flush(s):
    if (len(s.writebuf) > 0):
      if e32.is_ui_thread():
        s._StdErr__doflush()
      else:
        s._StdErr__flushgate()



class Interactive(object):
  __module__ = __name__

  def __init__(s, stream):
    s.std = stream
    s.historys=[]


  def show_history(s):
    if s.historys==[]:
      ui.note('历史为空'.decode('u8'), 'error')
    else:
      select=ui.popup_menu(s.historys, '历史'.decode('u8'))
      if select==None:
        return None
      else:
        s.std.write(s.historys[select])

  def clear_history(s):
    s.historys=[]
    ui.note('历史已清空'.decode('u8'), 'conf')
        


  def read_input(s, n):
    s.std.write(n.decode('u8'))
    user_input = s.std.readline()
    if history:
        s.history.insert(0, user_input)
    write_file(user_input+'\n')
    return user_input



  def interactive(s, scope = locals()):
    import code
    ui.app.menu = [('退出'.decode('u8'),
      ui.app.set_exit)]
    if history:
      ui.app.menu.insert(0, ('清空历史'.decode('u8'), s.clear_history))
      ui.app.menu.insert(0, ('历史'.decode('u8'), s.show_history))
    s.std.text.bind(EKeySelect, s.std.lock_signal)
    s.std.text.bind(EKeyEnter, lambda: e32.ao_sleep(0, s.std.lock.signal))
    code.interact(((u'pys60 version: ' + e32.pys60_version) + u'\n=======Shell======='), s.read_input, scope)
    s.std.text.bind(EKeySelect, None)
    s.std.text.bind(EKeyEnter, None)





def shell():
  script_namespace = NameSpace()
  ui.app.exit_key_handler = ui.app.set_exit
  ui.app.menu = [('退出'.decode('u8'),
    ui.app.set_exit)]
  ui.app.body = stream.text
  sys.stderr = stderr
  sys.stdin = sys.stdout = stream
  Interactive(stream).interactive(script_namespace.namespace)

def _write_file1(text):
    try :
        f = open('d:\\shell_print', 'a')
        try :
            f.write(text.encode('u8'))
        finally :
            f.close()
    except :
        pass

def _write_file2(text):
    pass

write_file=[_write_file2, _write_file1][os.path.exists('print')]
history=os.path.exists('history')

stream = Stream()
stderr = StdErr()
sys.stderr = stderr
sys.stdin = sys.stdout = stream
#e32._stdo(u'c:\\python_error.log')
shell()
