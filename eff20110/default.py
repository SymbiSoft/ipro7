import sys
disk=sys.argv[0][0]
sys.path.append(disk+":\\resource\\")
import argv
file_path=argv.get()
if file_path!="":
    import error_exc
    from iPro7 import program
    program.start()
    program.fetch_file(path = file_path)
    argv.set("")
else:
    try:
        import error_exc
        from iPro7 import program
        program.start()
    except:
        import appuifw
        import traceback
        import sys
        import os

        appuifw.app.title = '错误'.decode('u8')
        appuifw.app.screen = 'normal'
        appuifw.app.menu = [('退出'.decode('u8'), appuifw.app.set_exit)]
        appuifw.app.exit_key_handler = appuifw.app.set_exit
        appuifw.app.body = appuifw.Text((''.join(traceback.format_exception(*sys.exc_info()))).decode('u8'))