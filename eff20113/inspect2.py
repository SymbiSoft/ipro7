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
try:
  f = open('d:\\Inspect_Dir')
  sys.path[0] = f.read()
  f.close()
except:
  ui.note('无法初始化模块搜寻路径'.decode('u8'), 'error')
path = 'd:\\iPro7_Inspecting\\default.py'

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
          write(exc_info)
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



  def read_input(s, n):
    s.std.write(n.decode('u8'))
    user_input = s.std.readline()
    write_file(user_input+"\n")
    return user_input



  def interactive(s, scope = locals()):
    import code
    ui.app.menu = [('退出'.decode('u8'),
      ui.app.set_exit)]
    s.std.text.bind(EKeySelect, s.std.lock_signal)
    s.std.text.bind(EKeyEnter, lambda: e32.ao_sleep(0, s.std.lock.signal))
    code.interact(u'>>> ', s.read_input, scope)
    s.std.text.bind(EKeySelect, None)
    s.std.text.bind(EKeyEnter, None)




def exitfunc():
  sys.exit()



def inspect(path):
  script_namespace = NameSpace()
  try:
    try:
      ui.app.menu = []
      if time:
        from time import clock
        t=clock()
        print '>>> inspect start'
      execfile(path, script_namespace.namespace)
      if time:
        print '>>> inspect end,use time:',clock()-t,'s'
    finally:
      ui.app.exit_key_handler = ui.app.set_exit
      ui.app.title = u'Inspect2'
      ui.app.menu = [('退出'.decode('u8'),
        ui.app.set_exit)]
      if (ui.app.body is not stream.text):
        ui.app.body = stream.text
      ui.app.screen = 'normal'
      sys.stderr = stderr
      sys.stdin = sys.stdout = stream

  except:
    import traceback
    exc_info = ''.join(traceback.format_exception(*sys.exc_info()))
    print unicode(exc_info, 'u8', 'ignore'),
    write(exc_info)
  Interactive(stream).interactive(script_namespace.namespace)


def _write_file1(text):
    try :
        f = open('d:\\inspect_print', 'a')
        try :
            f.write(text.encode('u8'))
        finally :
            f.close()
    except :
        pass

def _write_file2(text):
    pass


def write(text):
  if (text.find('File') < 0):
    return 
  try:
    f = open('d:\\inspect_mistake', 'a')
    try:
      f.write(text)

    finally:
      f.close()

  except:
    pass


write_file=[_write_file2, _write_file1][os.path.exists('print')]
time=os.path.exists('time')

stream = Stream()
stderr = StdErr()
sys.exitfunc = exitfunc
sys.stderr = stderr
sys.stdin = sys.stdout = stream
#e32._stdo(u'c:\\python_error.log')
ui.app.body = stream.text
print ((u'pys60 version: ' + e32.pys60_version) + u'\n=======Inspect2=======\n>>> ')
e32.ao_sleep(0.05)
inspect(path)
