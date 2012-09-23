

import sys
import os
import series60_console
import appuifw

sys.path.insert(0, os.path.join(os.getcwd(), 'lib.zip'))
sys.path.insert(0, os.getcwd())
default_namespace = {'__builtins__': __builtins__, '__name__': '__main__'}

my_console = series60_console.Console()
saved_exit_key_handler = appuifw.app.exit_key_handler


def restore_defaults():
    appuifw.app.body = my_console.text
    sys.stderr = sys.stdout = my_console
    appuifw.app.screen = 'normal'
    appuifw.app.menu = []

restore_defaults()


def display_traceback():
    import traceback
    traceback.print_exc()


try:
    try:
        execfile('default.py', default_namespace)
    finally:
        default_namespace.clear()
        appuifw.app.exit_key_handler = saved_exit_key_handler
        restore_defaults()
except SystemExit, err:
    if str(err) not in [str(0), '']:
        display_traceback()
    else:
        appuifw.app.set_exit()
except:
    display_traceback()
else:
    if not appuifw.app.body.len():
        appuifw.app.set_exit()
