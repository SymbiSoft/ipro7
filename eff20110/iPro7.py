__date__ = '2012/09/01'
__version__ = '3.2.0'
__doc__ = ('名称: iPro7\n作者: 逆浪′\n修改更新：zl@SUN\n版本: %s\n日期: %s\nCopyright © 2010-2012 逆浪′\n修改或利用此源码前请先取得原作者的同意。\n版权所有，请勿用于商业用途。' % (__version__, __date__))

import ui
import e32
import sys
import os
try:
    from key_codes import EKey0, EKey1, EKey2, EKey3, EKey4, EKey5, EKey6, EKey7, EKey8, EKey9, EKeyYes, EKeySelect, EKeyStar, EKeyHash, EKeyBackspace, EKeyEnter, EKeyLeftArrow, EKeyRightArrow, EKeyUpArrow, EKeyDownArrow
except:
    EKey0, EKey1, EKey2, EKey3, EKey4, EKey5, EKey6, EKey7, EKey8, EKey9, EKeyYes, EKeySelect, EKeyStar, EKeyHash, EKeyBackspace, EKeyEnter, EKeyLeftArrow, EKeyRightArrow, EKeyUpArrow, EKeyDownArrow = 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 63586, 63557, 42, 35, 8, 13, 63495, 63496, 63497, 63498

from db import *

cn = lambda x, : x.decode('u8') 
en = lambda y, : y.encode('u8')

class Program(object, ) :

    def start(s):
        s.shortcut_level = 0
        s.only_page_shortcut = False
        s.file_paths = []
        s.poss = []
        s.codes = []
        s.windows = []
        s.contents = []
        s.initial_contents = []
        s.current_w = 0
        s.keywords = [u'and', u'assert', u'break', u'class', u'continue', u'def', u'del', u'elif', u'else', u'except', u'exec', u'finally', u'for', u'from', u'global', u'if', u'import', u'as', u'in', u'is', u'lambda', u'not', u'or', u'pass', u'print', u'raise', u'return', u'try', u'while', u'yield']
        s.codes_list = [u'utf-8', u'utf-16', u'gbk', u'gb2312', u'big5', u'ascii', u'koi8-r', u'latin-1']
        s.circuit_dict = {1 : cn('开启'), 0 : cn('禁用')}
        s.screen_size_dict = {'full' : cn('全屏'), 'normal' : cn('普通'), 'large' : cn('大屏')}
        s.screen_rotate_dict={'automatic' : cn('自动'), 'portrait' : cn('竖屏'), 'landscape' : cn('横屏')}
        s.hl_style_dict = {'ui.STYLE_BOLD' : cn('粗体'), 'ui.STYLE_ITALIC' : cn('斜体'), 'ui.STYLE_UNDERLINE' : cn('下划线'), '0' : cn('默认')}
        s.initial_body_dict = {'0' : cn('历史'), '1' : cn('新建'), '2' : cn('最后打开')}
        s.mode_dict = {cn('区分大小写') : 0, cn('完全匹配') : 0, cn('正则匹配') : 0}
        s.seek_type = 'normal'
        s.read_db()
        s.load_menu(path=os.path.join(os.getcwd(), "menu.py"))

        if db['change_input_mode'] : 
            input_mode = 1
        else : 
            input_mode = None
        s.infopopup = ui.InfoPopup()
        s.w = ui.Text(edit_callback = s.keyword_highlight, skinned = s.skinned, scrollbar = s.scrollbar, input_mode = input_mode)
        s.w.font = (s.font, s.font_size)
        s.w.color = s.font_color
        s.w.highlight_color = s.highlight_color
        sys.exitfunc = s.cache

        if (windows_db['contents'] != [''] or windows_db['file_paths'] != ['']) and ui.query(cn('恢复未完成文件?'), 'query') : 
            s.contents = windows_db['contents']
            s.current_w = windows_db['current_w']
            s.windows = windows_db['windows']
            s.file_paths = windows_db['file_paths']
            s.codes = windows_db['codes']
            s.poss = windows_db['poss']
            s.initial_contents = []
            for idx in range(len(s.file_paths)):
                s.initial_contents.append(s.read_initial_content(s.file_paths[idx], code = s.codes[idx]))
            s.update_ui()
            e32.ao_yield()
            s.infopopup.show((cn('%d个未完成文件') % len(s.windows)), (0, 0), 3000, 0)
            pass
        elif db['initial_body'] == '0' : 
            if history.list == [] : 
                e32.ao_yield()
                s.build_window()
            else : 
                ask = file_manager.AskFile('历史文件\\', ext = ['.' + et for et in db['ext']], auto_return_ui = False, body_process = False, dirs = eval(db['work_dirs']))
                if ask == [] : 
                    e32.ao_yield()
                    s.build_window()
                else : 
                    ui.app.title = cn('请稍候,..')
                    for i in ask:
                        e32.ao_yield()
                        s.fetch_file(path = i)
                    pass
            pass
        elif db['initial_body'] == '1' : 
            e32.ao_yield()
            s.build_window()
        else : 
            e32.ao_yield()
            s.fetch_file(path = windows_db['last_file_path'], code = windows_db['last_code'], pos = windows_db['last_pos'])

        e32.ao_sleep(0, s._prepare)

        ui.app.screen = s.screen_size
        ui.app.orientation=s.screen_rotate
        ui.app.menu = s.menu
        ui.app.exit_key_handler = s.exit_key_handle
        s.focus_func = lambda fg : None
        ui.app.focus = s.focus_callback

    def _prepare(s):
        from keycapture import KeyCapturer
        s.KeyCapturer = KeyCapturer
        s.w.bind(EKeySelect, s.newline)
        s.w.bind(EKeyYes, s.shortcut)
        try :
            s.w.bind(EKeyEnter, lambda  :  e32.ao_sleep(0, s.ekeyenter_event) )
        except :
            pass
        s.extend()

    def load_menu(s, path=''):
        s.menu=[
        (cn('测试'), s.inspect), 
        (cn('文件'), 
          ((cn('打开文件'), s.fetch_file), 
          (cn('打开历史'), s.fetch_history),
          (cn('新建文件'), s.build_window), 
          (cn('保存文件'), s.ask_save), 
          (cn('另存文件'), s.save_as_new), 
          (cn('全部保存'), s.save_all), 
          (cn('切换编码'), s.change_code), 
          (cn('存为模板'), s.save_as_mould), 
          (cn('文件详情'), s.file_details))),
        (cn('编辑'), 
          ((cn('查找文字'), s.seek), 
          (cn('查找下个'), s.seek_next), 
          (cn('高级查找'), s.senior_seek), 
          (cn('查找替换'), s.seek_replace), 
          (cn('插入模板'), s.insert_mould),
          (cn('函数浏览'), s.read_funcs), 
          (cn('清空内容'), s.clear_content))),
        (cn('跳转'), s.jump), 
        (cn('窗口'), s.change_window), 
        (cn('设置'), s.set), 
        (cn('拓展'), s.execute_extend), 
        (cn('运行'), s.run_script), 
        (cn('解释'), s.shell), 
        (cn('退出'), s.exit)]
        if os.path.exists(path):
            try:
                execfile(path)
            except:
                pass

    def load_shortcut_menu(s):
        all_action_names = [cn('查找文字'), cn('高级查找'), cn('查找替换'), cn('查找下个'), cn('跳转行数'), cn('跳至开头'), cn('跳至底部'), cn('行首'), cn('行末'), cn('上一页'), cn('下一页'), cn('窗口切换'), cn('关闭当前'), cn('关闭其它'), cn('打开文件'), cn('打开历史'), cn('保存文件'), cn('新建文件'), cn('解释'), cn('测试'), cn('运行'), cn('缩进'), cn('删除缩进'),cn('函数浏览'), cn('插入模板'), cn('拓展')]
        all_action_list = ['seek', 'senior_seek', 'seek_replace', 'seek_next', 'to_line', 'to_start', 'to_end', 'to_linestart', 'to_lineend', 'last_page', 'next_page', 'change_window', 'kill_window', 'kill_others', 'fetch_file', 'fetch_history', 'ask_save', 'build_window', 'shell', 'inspect', 'run_script', 'add_indentation', 'delete_indentation', 'read_funcs', 'insert_mould', 'execute_extend']
        s.action_names = [all_action_names[i] for i in db['shortcut_menu_list']]
        s.action_list = [all_action_list[i] for i in db['shortcut_menu_list']]

    def read_initial_content(s, path, code = 'u8'):
        try :
            f = open(path)
        except :
            return u''
        try :
            try :
                return f.read().decode(code).replace(u'\r\n', u'\u2029').replace(u'\n', u'\u2029')
            finally :
                f.close()
        except :
            return u''

    def update_ui(s):
        ui.app.set_tabs([], None)
        e32.ao_yield()
        ui.app.menu = s.menu
        ui.app.exit_key_handler = s.exit_key_handle
        s.w.clear_selection()
        s.w.clear()
        if db['change_input_mode'] : 
            input_mode = 1
        else : 
            input_mode = None
        s.w = ui.Text(edit_callback = s.keyword_highlight, skinned = s.skinned, scrollbar = s.scrollbar, input_mode = input_mode)
        s.w.font = (s.font, s.font_size)
        s.w.color = s.font_color
        s.w.highlight_color = s.highlight_color
        s.w.bind(EKeySelect, s.newline)
        s.w.bind(EKeyYes, s.shortcut)
        try :
            s.w.bind(EKeyEnter, lambda  :  e32.ao_sleep(0, s.ekeyenter_event) )
        except :
            pass
        ui.app.title = cn('请稍候...')
        ui.app.body = s.w
        if s.screen_size != ui.app.screen : 
            ui.app.screen = s.screen_size
        if s.screen_rotate != ui.app.orientation : 
            ui.app.orientation = s.screen_rotate
        if s.contents[s.current_w] in s.keywords : 
            s.w.focus = False
            s.w_set(s.contents[s.current_w] + u'\n')
            s.w.delete((s.w.len() - 1), 1)
            s.w.focus = True
        else : 
            s.w_set(s.contents[s.current_w])
        s.w.set_pos(0)
        try :
            s.highlight_handle()
        except:
            ui.note(cn('无法高亮处理'), 'error')
        s.w.set_pos(s.poss[s.current_w])
        ui.app.title = s.windows[s.current_w]

    def build_window(s, newly = True):
        if  not (s.contents == []) : 
            s.contents[s.current_w] = s.w.get()
            s.poss[s.current_w] = s.w.get_pos()
        s.current_w = len(s.contents)
        s.w.clear_selection()
        s.w.clear()
        if ui.app.body != s.w : 
            ui.app.body = s.w
            ui.app.menu = s.menu
            ui.app.exit_key_handler = s.exit_key_handle
        if  not (newly) : 
            s.windows.append(u'')
            ui.app.title = u''
        else : 
            s.windows.append(cn('新建文件'))
            ui.app.title = cn('新建文件')
        s.file_paths.append('')
        s.codes.append(s.default_code)
        s.contents.append(u'')
        s.poss.append(0)
        s.initial_contents.append(u'')
        if ui.app.screen != s.screen_size : 
            ui.app.screen = s.screen_size
        if s.screen_rotate != ui.app.orientation : 
            ui.app.orientation = s.screen_rotate

    def change_window(s, w_index = None):
        s.contents[s.current_w] = s.w.get()
        s.poss[s.current_w] = s.w.get_pos()
        contents_len = len(s.contents)
        if w_index != None : 
            choose = w_index
        elif contents_len >= 3 : 
            choose = ui.popup_menu([unicode((i + 1)) + u'. ' + s.windows[i] for i in range(len(s.windows))], (cn('窗口(%d/%d)') % ((s.current_w + 1), len(s.contents))))
            if choose == None : 
                return None
            pass
        elif contents_len == 2 : 
            choose = (s.current_w ^ 1)
        else : 
            s.infopopup.show(cn('仅有一个窗口'), (0, 0), 3000, 0)
            return None
        s.current_w = choose
        s.w.clear_selection()
        s.w.clear()
        if s.contents[choose] in s.keywords : 
            s.w.focus = False
            s.w_set(s.contents[choose] + u'\n')
            s.w.delete((s.w.len() - 1), 1)
            s.w.focus = True
        else : 
            s.w_set(s.contents[choose])
        s.w.set_pos(0)
        try :
            s.highlight_handle()
        except :
            ui.note(cn('无法高亮处理'), 'error')
        s.w.set_pos(s.poss[choose])
        ui.app.title = s.windows[choose]

    def save_all(s):
        s.contents[s.current_w] = s.w.get()
        s.poss[s.current_w] = s.w.get_pos()
        current = s.current_w
        if  not (s.ask_save()) : 
            return None
        for i in range(len(s.contents)):
            if i != current : 
                e32.ao_yield()
                s.change_window(i)
                if s.file_paths[s.current_w] == '' : 
                    e32.ao_sleep(1)
                if  not (s.ask_save()) : 
                    return None
                pass

    def kill_window(s):
        current_w = s.current_w
        s.contents[s.current_w] = s.w.get()
        s.poss[s.current_w] = s.w.get_pos()
        if len(s.contents) == 1 : 
            ui.note(cn('仅有一个窗口'))
            return False
        if s.contents[s.current_w] != s.initial_contents[s.current_w] : 
            ask = ui.popup_menu([cn('保存'), cn('取消')], cn('保存文件'))
            if ask is None : 
                return False
            elif ask == 0 : 
                if  not (s.ask_save()) : 
                    return False
                pass
            pass
        if s.current_w == 0 : 
            s.change_window(1)
            s.current_w = 0
        else : 
            s.change_window((s.current_w - 1))
        del s.contents[current_w]
        del s.poss[current_w]
        del s.windows[current_w]
        del s.file_paths[current_w]
        del s.codes[current_w]
        del s.initial_contents[current_w]
        return True

    def kill_others(s):
        if len(s.contents) == 1 : 
            ui.note(cn('仅有一个窗口'))
            return None
        if ui.query(cn('放弃其它所有窗口？'), 'query') : 
            s.contents = [s.contents[s.current_w]]
            s.poss = [s.poss[s.current_w]]
            s.windows = [s.windows[s.current_w]]
            s.file_paths = [s.file_paths[s.current_w]]
            s.codes = [s.codes[s.current_w]]
            s.initial_contents = [s.initial_contents[s.current_w]]
            s.current_w = 0

    def read_db(s):
        try :
            import time
            s.scene = db['scene']
            localtime = time.localtime()
            if s.scene['start'] <= (localtime[3] * 3600) + (localtime[4] * 60) <= s.scene['end'] : 
                s.font_color = eval(s.scene['font_color'])
                s.open_highlight = s.scene['open_highlight']
                s.highlight_color = eval(s.scene['highlight_color'])
                s.highlight_style = eval(s.scene['highlight_style'])
                s.skinned = s.scene['skinned']
                s.scrollbar = s.scene['scrollbar']
            else : 
                raise ImportError
        except :
            s.font_color = eval(db['font_color'])
            s.open_highlight = db['open_highlight']
            s.highlight_color = eval(db['highlight_color'])
            s.highlight_style = eval(db['highlight_style'])
            s.skinned = db['skinned']
            s.scrollbar = db['scrollbar']
        s.shortcut_menu=db['shortcut_menu']
        if s.shortcut_menu:
            s.load_shortcut_menu()
        s.autosave = db['autosave']
        s.autosave_time = db['autosave_time']
        if s.autosave:
            s.timer = e32.Ao_timer()
            s.timer.after(s.autosave_time, s.timer_callback)
        if db['mediakeys']:
            ui.app.mediakeys = True
            ui.app.bind_mediakeys(s.last_page, s.next_page)
        else:
            ui.app.mediakeys = False
            ui.app._mediakeys_listener = None
        s.font = db['font']
        s.font_size = db['font_size']
        s.screen_size = db['screen_size']
        s.screen_rotate = db['screen_rotate']
        s.keyword_blank = db['keyword_blank']
        s.indentation_length = db['indentation_length']
        s.inspect_add_lock = db['inspect_add_lock']
        s.default_file_name = cn(db['default_file_name'])
        s.seek_replace_content = db['seek_replace_content']
        s.seek_content = cn(db['seek_content'])
        s.seek_type = db['seek_type']
        s.format = cn(db['format'])
        s.default_fetch_dir = db['default_fetch_dir']
        s.default_save_dir = db['default_save_dir']
        s.py_version = db['py_version']
        if e32.s60_version_info >= (3, 0) : 
            if s.py_version == '1.45':
                s.shell_path = disk + '\\sys\\bin\\Shell_0xeff20112.exe'
            else:
                s.shell_path = disk + '\\sys\\bin\\Shell2_0xeff20114.exe'
        else : 
            s.shell_path = disk + '\\System\\apps\\iPro7\\Shell\\Shell.app'
        s.default_code = db['default_code']
        if s.indentation_length != 'off' : 
            s.indentation = u''.join([u' ' for i in range(int(s.indentation_length))])
        else : 
            s.indentation = u''
        if db['set_system'] : 
            try :
                import envy
                envy.set_app_system(1)
            except ImportError : 
                try :
                    import msys
                    msys.set_system()
                except ImportError : 
                    ui.note(cn('无法设为系统程序'), 'error')
                pass
            pass
        else : 
            try :
                import envy
                envy.set_app_system(0)
            except ImportError : 
                try :
                    import msys
                    msys.unset_system()
                except ImportError : 
                    pass
                pass
            pass

    def focus_callback(s, fg):
        s.focus_func(fg)
        if not fg or ui.app.body!=s.w:
            return None
        import argv
        file_path=argv.get()
        if file_path!="":
            s.fetch_file(path = file_path)
            argv.set("")

    def fetch_file(s, path = None, code = None, pos = 0, title = None, is_temp = False, read_initial = False, initial_path = None):
        if code is None : 
            code = db['default_code']
        if path is None : 
            ask = file_manager.AskFile(s.default_fetch_dir, ext = ['.' + et for et in db['ext']], body_process = True, auto_return_ui = False, dirs = eval(db['work_dirs']))
            if ask == [] : 
                file_manager.return_ui()
                return None
            else : 
                for i in ask:
                    s.fetch_file(path = i)
                return None
            pass
        elif path == '' : 
            s.build_window()
            return None
        else : 
            ask_file_path = cn(path)
        s.build_window(newly = False)
        ui.app.title = cn('请稍候...')
        if  not (os.path.exists(en(ask_file_path))) : 
            ui.app.title = cn('错误')
            ui.note((cn("文件不存在\n'%s'") % ask_file_path), 'error')
            history.remove(ask_file_path)
            return None
        try :
            file_open = open(en(ask_file_path), 'r')
        except:
            ui.app.title = cn('错误')
            ui.note((cn("无法打开\n'%s'") % ask_file_path), 'error')
            return None
        e32.ao_yield()
        file_content = file_open.read()
        try :
            file_open.close()
        except :
            ui.note((cn('文件出现异常\n%s') % ask_file_path), 'error')
        if file_content.startswith('\xff\xfe') or file_content.startswith('\xfe\xff') : 
            if ui.query(cn("用'utf-16'编码打开此文本？"), 'query') : 
                code = 'utf_16'
            pass
        try :
            s.w.clear()
            while True:
                try:
                    file_content = file_content.decode(code)
                    break
                except:
                    if ui.query(cn("当前编码%s无效，选择其他编码打开此文本？")%code, 'query'):
                        select=ui.popup_menu(s.codes_list, cn("选择编码(%s)"%code))
                        if select==None:
                            break
                        else:
                            code=en(s.codes_list[select])
                    else:
                        break
            if not db['fast_fetch'] : 
                e32.ao_yield()
                s.w.set(file_content.replace(u'\r\n', u'\n'))
            elif  not (file_content.find(u'\t') > -1 and ui.query(cn('将tab空格转换为普通空格？'), 'query')) : 
                e32.ao_yield()
                s.w_set(file_content.replace(u'\r\n', u'\n'))
            else : 
                if s.indentation == u'' : 
                    indentation = u'    '
                else : 
                    indentation = s.indentation
                s.w.set(file_content.replace(u'\t', indentation).replace(u'\r\n', u'\n'), fast = True)
        except:
            ui.app.title = cn('错误')
            ui.note((cn("无法打开\n'%s'") % ask_file_path), 'error')
            return None
        s.contents[s.current_w] = s.w.get()
        s.windows[s.current_w] = os.path.basename(ask_file_path)
        s.file_paths[s.current_w] = en(ask_file_path)
        s.codes[s.current_w] = code
        s.w.set_pos(0)
        try :
            s.highlight_handle()
        except :
            ui.note(cn('无法高亮处理'), 'error')
        if title == None : 
            ui.app.title = os.path.basename(ask_file_path)
        elif title != u'' : 
            ui.app.title = title
        else : 
            ui.app.title = cn('新建文件')
        try :
            s.w.set_pos(pos)
        except :
            s.w.set_pos(0)
        s.poss[s.current_w] = s.w.get_pos()
        if  not (is_temp) : 
            history.write(ask_file_path)
            s.initial_contents[s.current_w] = s.w.get()
        if read_initial : 
            s.initial_contents[s.current_w] = s.read_initial_content(initial_path, code = code)

    def fetch_history(s):
        ask = file_manager.AskFile(path = '历史文件\\', body_process = True, ext = ['.' + et for et in db['ext']], auto_return_ui = False, dirs = eval(db['work_dirs']))
        if ask == [] : 
            file_manager.return_ui()
            return None
        for i in ask:
            s.fetch_file(path = i)

    def ask_save(s, code = None, w_index = None, newly = False, default_save_dir = None):
        s.contents[s.current_w] = s.w.get()
        s.poss[s.current_w] = s.w.get_pos()
        if w_index is None : 
            w_index = s.current_w
        if code is None : 
            code = s.codes[w_index]
        if default_save_dir is None : 
            default_save_dir = s.default_save_dir
        ask_save_name = None
        if s.file_paths[w_index] == '' or newly : 
            ask_save_dir = file_manager.AskDir(path = default_save_dir, body_process = True, auto_return_ui = False, dirs = eval(db['work_dirs']))
            if ask_save_dir is None : 
                file_manager.return_ui()
                return False
            ask_save_name = ui.query(cn('文件名') + u'(' + s.format + u')', 'text', s.default_file_name)
            if ask_save_name is None : 
                file_manager.return_ui()
                return False
            elif ask_save_name.count(u'.') > 0 and ui.query((cn('更改拓展名为%s？') % os.path.splitext(ask_save_name)[-1]), 'query') : 
                pass
            else : 
                ask_save_name += s.format
            file_path = os.path.join(ask_save_dir, en(ask_save_name))
            while True : 
                if os.path.exists(file_path) : 
                    ask_cover = ui.popup_menu([cn('重命名'), cn('覆盖')], cn('同名文件已存在'))
                    if ask_cover is None : 
                        file_manager.return_ui()
                        return False
                    elif ask_cover == 0 : 
                        ask_save_name = ui.query(cn('文件名(%s)'%s.format), 'text', s.default_file_name)
                        if ask_save_name is None : 
                            file_manager.return_ui()
                            return False
                        elif ask_save_name.find(u'.') > -1 and ui.query((cn('更改拓展名为%s？') % os.path.splitext(ask_save_name)[-1]), 'query') : 
                            pass
                        else : 
                            ask_save_name += s.format
                        file_path = ask_save_dir + en(ask_save_name)
                    else : 
                        break
                    pass
                else : 
                    break
            file_manager.return_ui()
            if  not (s.save(file_path, code = code, w_index = w_index)) : 
                return False
            pass
        elif  not (s.save(s.file_paths[w_index], code = code, w_index = w_index)) : 
            return False
        return True

    def save_as_new(s):
        s.ask_save(code = s.codes[s.current_w], newly = True, default_save_dir = os.path.dirname(s.file_paths[s.current_w]))

    def save_as_mould(s):
        ui.app.body.focus = False
        mould_name = ui.query(cn('模板名'), 'text')
        ui.app.body.focus = True
        if mould_name is None : 
            return None
        mould_path = disk + en(u'\\System\\iPro7\\Mould\\' + mould_name + u'.py')
        while True : 
            if os.path.exists(mould_path) : 
                ask_cover = ui.popup_menu([cn('重命名'), cn('覆盖')], cn('同名模板已存在'))
                if ask_cover is None : 
                    return None
                elif ask_cover == 0 : 
                    ui.app.body.focus = False
                    name = ui.query(cn('模板名'), 'text')
                    ui.app.body.focus = True
                    if name is None : 
                        return None
                    mould_path = disk + en(u'\\System\\iPro7\\insert_mould\\' + name + u'.py')
                else : 
                    break
                pass
            else : 
                break
        try :
            f = open(mould_path, 'w')
            f.write(en(ui.app.body.get().replace(u'\r\u2029', u'\r\n').replace(u'\u2029', u'\r\n').replace(u'\r\u2028', u'\r\n').replace(u'\u2028', u'\r\n')))
            f.close()
            s.infopopup.show(cn('保存成功'), (0, 0), 3000, 0)
            return True
        except :
            ui.note(cn('无法保存'), 'error')
            return False

    def save_temp(s):
        if ui.app.body.len() > 0 : 
            s.save(temp_file_path, save_as_temp = True)

    def save(s, path, code = None, w_index = None, save_as_temp = False):
        if w_index is None : 
            w_index = s.current_w
        if code is None : 
            if  not (save_as_temp) : 
                code = s.codes[w_index]
            else : 
                code = 'u8'
            pass
        s.get = s.contents[w_index]
        s.get_replace = s.get.replace(u'\r\u2029', u'\r\n').replace(u'\u2029', u'\r\n').replace(u'\r\u2028', u'\r\n').replace(u'\u2028', u'\r\n')
        try :
            save_content = s.get_replace.encode(code)
            save_file = open(path, 'w')
            save_file.write(save_content)
            save_file.close()
            if  not (save_as_temp) : 
                s.file_paths[w_index] = path
                history.write(cn(path))
                s.infopopup.show(cn('保存成功'), (0, 0), 3000, 0)
                pass
        except :
            if  not (save_as_temp) : 
                ui.note(cn('无法保存'), 'error')
                return False
            pass
        if  not (save_as_temp) : 
            s.file_paths[w_index] = path
            s.windows[w_index] = cn(os.path.split(path)[-1])
            s.initial_contents[w_index] = s.get
            if (ui.app.body == s.w) & (w_index == s.current_w) : 
                ui.app.title = s.windows[w_index]
            pass
        return True

    def timer_callback(s):
        s.cache()
        if s.autosave :
            s.timer.after(s.autosave_time, s.timer_callback)

    def w_set(s, text):
        s.w.set(text, fast = (db['fast_fetch'] and text.find(u'\t') == -1))

    def change_code(s):
        choose = ui.popup_menu(s.codes_list, (cn('选择编码(%s)') % cn(s.codes[s.current_w])))
        if choose != None : 
            s.codes[s.current_w] = en(s.codes_list[choose])

    def clear_content(s):
        s.w.clear_selection()
        s.w.set_pos(0)
        s.w.clear()

    def extend_error(s, m = u''):
        try :
            import globalui
            import traceback
            exc_info = ''.join(traceback.format_exception(*sys.exc_info()))
            if globalui.global_msg_query((cn('%s\n是否保存错误信息？') % cn(exc_info)), (cn('%s插件错误') % m)) : 
                try :
                    f = open(disk + '\\iPro7_Extend_Error.txt', 'w')
                    f.write(exc_info)
                    f.close()
                    ui.note((cn('错误信息保存为\n%s') % cn(disk + '\iPro7_Extend_Error.txt')), 'conf')
                except IOError : 
                    ui.note(cn('无法保存错误信息'), 'error')
                pass
        except ImportError : 
            ui.note((cn("插件错误\n'%s'") % m), 'error')

    def extend(s):
        if len(s.contents) != 0 : 
            s.contents[s.current_w] = s.w.get()
            s.poss[s.current_w] = s.w.get_pos()
        s.extends = {}
        s.extend_funcs_dict = {}
        s.all_extends_dict = {}
        dir = disk + '\\System\\iPro7\\Extend\\'
        if  not (os.path.isdir(dir)) : 
            os.makedirs(dir)
        sys.path.insert(0, dir)
        for m in os.listdir(dir):
            if  not (m.lower().endswith('py') or m.lower().endswith('pyc')) : 
                continue
            m = cn(os.path.splitext(m)[0])
            try :
                exec ((u"import %s\ns.extends[u'%s'] = %s" % (m, m, m)), {'s' : s})
            except :
                s.extend_error(m)
        for m in s.extends.keys():
            try :
                try :
                    funcs = s.extends[m].connect_to_iPro7(disk, s)
                except TypeError : 
                    funcs = s.extends[m].connect_to_iPro7()
                if type(funcs) != type({}) : 
                    s.extend_error(m)
                    continue
                s.extend_funcs_dict[m] = funcs
            except :
                s.extend_error(m)
        k = 1
        for i in s.extend_funcs_dict.keys():
            for f in s.extend_funcs_dict[i].keys():
                try :
                    exec (u"s.all_extends_dict[u'%d. ' %k + f] = s.extend_funcs_dict[i][f]", {'s' : s, 'i' : i, 'f' : f, 'k' : k})
                    k += 1
                except :
                    s.extend_error()
                    return None

    def execute_extend(s):
        s.contents[s.current_w] = s.w.get()
        s.poss[s.current_w] = s.w.get_pos()
        if s.all_extends_dict == {} : 
            ui.note(cn('无可用插件'))
            return None
        extends = s.all_extends_dict.keys()
        extends.sort()
        try :
            choose = ui.popup_menu(extends, cn('拓展'))
        except :
            s.extend_error()
            return None
        if choose is None : 
            return None
        try :
            s.all_extends_dict[extends[choose]]()
        except :
            s.extend_error()

    def edit_text(s, title=u'', content=u''):
        old = (ui.app.title, ui.app.screen, ui.app.body, ui.app.menu, ui.app.exit_key_handler)
        lok = e32.Ao_lock()
        def back():
            lok.signal()
        ui.app.body=t=ui.Text(scrollbar=1)
        ui.app.title=title
        ui.app.menu=[
        (cn("清屏"),lambda :ui.app.body.set(u'')),
        (cn('返回'), back)]
        ui.app.exit_key_handler = back
        t.set(content)
        lok.wait()
        (ui.app.title, ui.app.screen, ui.app.body, ui.app.menu, ui.app.exit_key_handler,) = old
        return t.get()

    def seek(s, next = False):
        if  not (next) : 
            s.w.focus = False
            seek_content = ui.query(cn('查找内容'), 'text', s.seek_content)
            s.w.focus = True
            if seek_content is None : 
                return None
            s.seek_content = seek_content
            s.seek_type = 'normal'
            db['seek_content'] = en(s.seek_content)
            db['seek_type'] = 'normal'
        pos = s.w.get_pos()
        s.get = s.w.get()
        if next and pos != s.w.len() : 
                find = (s.get[(pos + 1) : len(s.get)]).find(s.seek_content)
                if find != -1 : 
                    find += 1
                pass
        else : 
            find = s.get[pos : len(s.get)].find(s.seek_content)
        if find != -1 : 
            s.find_pos = pos + find
            s.w.set_pos(s.find_pos)
        elif pos != 0 and ui.query(cn('未找到，从头开始？'), 'query') : 
            s.find_pos = s.get[ : len(s.get)].find(s.seek_content)
            if s.find_pos >= 0 : 
                s.w.set_pos(s.find_pos)
            else : 
                ui.note((cn('未找到\n%s') % s.seek_content))
            pass
        elif pos == 0 : 
            ui.note((cn('未找到\n%s') % s.seek_content))

    def senior_seek(s, next = False):
        import re
        if  not (next) : 
            seek_content = ui.query(cn('高级查找'), 'text', s.seek_content)
            if seek_content is None : 
                return None
            while True : 
                mode_list = s.mode_dict.keys()
                for i in mode_list:
                    if s.mode_dict[i] == 1 : 
                        mode_list[mode_list.index(i)] = u'*' + mode_list[mode_list.index(i)]
                    else : 
                        mode_list[mode_list.index(i)] = u' ' + mode_list[mode_list.index(i)]
                mode = ui.popup_menu([cn(' 确定')] + mode_list + [cn('编辑查找内容')], cn('查找模式'))
                if mode == None : 
                    return None
                elif mode == 1 : 
                    s.mode_dict[s.mode_dict.keys()[0]] ^= 1
                elif mode == 2 : 
                    s.mode_dict[s.mode_dict.keys()[1]] ^= 1
                elif mode == 3 : 
                    s.mode_dict[s.mode_dict.keys()[2]] ^= 1
                elif mode == 4 :
                    seek_content=s.edit_text(title=cn('查找内容'), content=seek_content)
                    e32.ao_sleep(0)
                elif mode == 0 : 
                    if seek_content=='':
                        ui.note(cn('查找内容不能为空!'), 'error')
                    else:
                        break
            pass
        else : 
            seek_content = s.seek_content
        s.seek_content = seek_content
        s.seek_type = 'senior'
        db['seek_content'] = en(seek_content)
        db['seek_type'] = 'senior'
        s.get = s.w.get()
        if not s.mode_dict[cn('正则匹配')] : 
           for i in u'\\.^$*+?{}[]|()':
                seek_content = seek_content.replace(i, u'\\' + i)
        if s.mode_dict[cn('完全匹配')] : 
            seek_content = '\\b' + seek_content + '\\b'
        try:
            if s.mode_dict[cn('区分大小写')] : 
                seek_re = re.compile(seek_content)
            else : 
                seek_re = re.compile(seek_content, re.IGNORECASE)
        except:
            ui.note(cn('表达式错误!'), 'error')
            return
        if next : 
            if ui.app.body.get_pos() != ui.app.body.len() : 
                s.find = seek_re.search(s.get[(ui.app.body.get_pos() + 1) : ])
            else : 
                s.find = seek_re.search(s.get[ui.app.body.get_pos() : ])
            pass
        else : 
            s.find = seek_re.search(s.get[ui.app.body.get_pos() : ])
        if s.find is not None : 
            s.find_pos = s.find.start()
            if next : 
                s.find_pos += 1
            s.find_pos += ui.app.body.get_pos()
            ui.app.body.set_pos(s.find_pos)
        elif ui.app.body.get_pos() != 0 and ui.query(cn('未找到，从头开始？'), 'query') : 
            s.find = seek_re.search(s.get)
            if s.find is not None : 
                s.find_pos = s.find.start()
                ui.app.body.set_pos(s.find_pos)
            else : 
                ui.note((cn('未找到\n%s') % s.seek_content))
            pass
        elif ui.app.body.get_pos() == 0 : 
            ui.note((cn('未找到\n%s') % s.seek_content))

    def seek_next(s):
        if s.seek_type == 'normal' : 
            s.seek(next = True)
        else : 
            s.senior_seek(next = True)

    def seek_replace(s):
        import re
        s.w.focus = False
        tmp=s.seek_replace_content[0]
        while True:
            seek_content = ui.query(cn('查找内容'), 'text', tmp)
            if seek_content == None : 
                s.w.focus = True
                return None
            tmp=seek_content
            replace_content = ui.query(cn('替换内容'), 'text', s.seek_replace_content[1])
            if replace_content != None:
                break
        s.w.focus = True
        temp_seek_content = seek_content
        pos = s.w.get_pos()
        while True : 
            mode_list = s.mode_dict.keys()
            for i in mode_list:
                if s.mode_dict[i] == 1 : 
                    mode_list[mode_list.index(i)] = u'*' + mode_list[mode_list.index(i)]
                else : 
                    mode_list[mode_list.index(i)] = u' ' + mode_list[mode_list.index(i)]
            mode = ui.popup_menu([cn(' 确定')] + mode_list + [cn('编辑查找内容'), cn('编辑替换内容')], cn('查找模式'))
            if mode == None : 
                return None
            elif mode == 1 : 
                s.mode_dict[s.mode_dict.keys()[0]] ^= 1
            elif mode == 2 : 
                s.mode_dict[s.mode_dict.keys()[1]] ^= 1
            elif mode == 3 : 
                s.mode_dict[s.mode_dict.keys()[2]] ^= 1
            elif mode == 4:
                    seek_content=s.edit_text(title=cn('查找内容'), content=seek_content)
                    e32.ao_sleep(0)
            elif mode == 5:
                    replace_content=s.edit_text(title=cn('替换内容'), content=replace_content)
                    e32.ao_sleep(0)
            elif mode == 0 : 
                if seek_content=='':
                    ui.note(cn('查找内容不能为空!'), 'error')
                else:
                    break
        s.seek_replace_content = [seek_content, replace_content]
        db['seek_replace_content'] = s.seek_replace_content
        if not s.mode_dict[cn('正则匹配')] : 
           for i in u'\\.^$*+?{}[]|()':
                seek_content = seek_content.replace(i, u'\\' + i)
        if s.mode_dict[cn('完全匹配')] : 
            seek_content = '\\b' + seek_content + '\\b'
        try:
            if s.mode_dict[cn('区分大小写')] : 
                seek_re = re.compile(seek_content)
            else : 
                seek_re = re.compile(seek_content, re.IGNORECASE)
        except:
            ui.note(cn('表达式错误!'), 'error')
            return
        replace_all = False
        s.find_pos = 0
        s.open_highlight = 0
        s.keyword_blank = 0
        while True : 
            e32.ao_yield()
            s.find = seek_re.search(s.w.get()[s.find_pos : ])
            if s.find != None : 
                flength=s.find.end()-s.find.start()
                s.find_pos += s.find.start()
                s.get = s.w.get()
                current_line = len(s.get[ : ui.app.body.get_pos()].split(u'\u2029'))
                split = s.get.split(u'\u2029')
                if current_line == len(split) : 
                    find_detail = split[-1]
                elif current_line <= (len(split) - 4) : 
                    find_detail = u'\n'.join(split[(current_line - 1) : (current_line + 4)])
                else : 
                    find_detail = u'\n'.join(split[(current_line - 1) : ])
                if replace_all : 
                    s.w.delete(s.find_pos, flength)
                    s.w.insert(s.find_pos, replace_content)
                    s.find_pos += len(replace_content)
                    #s.w.set_pos(s.find_pos)
                    continue
                else : 
                    s.w.set_pos(s.find_pos)
                    s.w.set_selection(s.find_pos, s.find_pos+flength)
                    while True : 
                        title=len(split[(current_line - 1)])<50 and split[(current_line - 1)] or split[(current_line - 1)][:50]
                        ask_replace = ui.popup_menu([(cn("替换为'%s'") % replace_content), cn('跳过'), cn('输入'), cn('全部替换'), cn('详情')], title)
                        if ask_replace == 4 : 
                            try :
                                import globalui
                                globalui.global_msg_query(find_detail, cn('详情'))
                            except ImportError : 
                                ui.note(find_detail)
                            pass
                        elif ask_replace == 2 : 
                            input_replace_content = ui.query(cn('输入'), 'text', replace_content)
                            if input_replace_content is not None : 
                                s.w.delete(s.find_pos, flength)
                                s.w.insert(s.find_pos, input_replace_content)
                                s.find_pos += len(input_replace_content)
                                s.w.set_pos(s.find_pos)
                                break
                            pass
                        else : 
                            break
                    if ask_replace is None : 
                        s.open_highlight = db['open_highlight']
                        s.keyword_blank = db['keyword_blank']
                        break
                    elif ask_replace == 0 : 
                        s.w.delete(s.find_pos, flength)
                        s.w.insert(s.find_pos, replace_content)
                        s.find_pos += len(replace_content)
                        s.w.set_pos(s.find_pos)
                        pass
                    elif ask_replace == 2 : 
                        continue
                    elif ask_replace == 3 : 
                        replace_all = True
                        s.w.focus = False
                        s.w.read_only = True
                        s.w.bind(EKeySelect, None)
                        s.w.bind(EKeyYes, None)
                        try :
                            s.w.bind(EKeyEnter, None)
                        except :
                            pass
                        pass
                    else : 
                        s.find_pos += flength
                pass
            else : 
                s.w.set_pos(0)
                s.w.insert(0, u'\n')
                s.w.delete(0, 1)
                s.w.set_pos(pos)
                s.open_highlight = db['open_highlight']
                s.keyword_blank = db['keyword_blank']
                s.w.focus = True
                s.w.read_only = False
                s.w.bind(EKeySelect, s.newline)
                s.w.bind(EKeyYes, s.shortcut)
                try :
                    s.w.bind(EKeyEnter, lambda  :  e32.ao_sleep(0, s.ekeyenter_event) )
                except :
                    pass
                break
        try :
            s.highlight_handle()
        except:
            pass

    def newline(s):
        current_pos = s.w.get_pos()
        get = s.w.get(0, current_pos)
        indentation = s.judge_indentation(get)
        s.w.insert(current_pos, '\n'+indentation)
        s.w.set_pos((current_pos + 1) + len(indentation))




    def ekeyenter_event(s):
        current_pos = s.w.get_pos()
        get = s.w.get(0, (current_pos - 1))
        indentation = s.judge_indentation(get)
        s.w.insert(current_pos, indentation)
        s.w.set_pos(current_pos + len(indentation))




    def judge_indentation(s, text):
        blank = u''
        if s.indentation_length == 'off' : 
            return u''
        elif text == u'' : 
            return u''
        pos = s.w.get_pos()
        text_lastline = text.split(u'\u2029')[-1]
        for b in text_lastline:
            if b == u' ' : 
                blank += u' '
            else : 
                break
        lastline=text_lastline.replace(u" ","").replace(u"\t","")
        if lastline=='':
            return blank
        start=lastline[0]
        end=lastline[-1]
        if ord(start)>255 or ord(end)>255:
            return blank
        flag=0
        for i in [u"break", u"return"]:
            if lastline.startswith(i):
                flag=-1
                break
        if not flag:
            flag=lastline in [u"else"]
        for i in [u"for", u"while", u"if", u"elif", u"else if"]:
            if flag:break
            flag=(lastline.startswith(i)) and (lastline[len(i)] in [u' ', u'(']) and end==")"
        if flag:
            next=s.w.get(pos,1)
            if next and next==u"{":
                flag=0
        else:
            for i in [u"#",u"\\\\",u"/*"]:
                if lastline.startswith(i):
                    return blank
            for i in [u"()", u"[]", u"{}"]:
                if end==i[0]:
                    flag=1
                    next=s.w.get(pos,1)
                    if next and next==i[1]:
                        s.w.insert(pos, u'\n'+blank)
            if end == u":":
                flag=1
        if flag==1:
            blank+=s.indentation
        elif flag==-1:
            if blank.endswith(s.indentation):
                blank=blank[:-len(s.indentation)]
        return blank




    def add_indentation(s):
        pos_place = ui.app.body.get_pos()
        ui.app.body.insert(pos_place, s.indentation)
        ui.app.body.set_pos(pos_place + len(s.indentation))




    def delete_indentation(s):
        if s.w.get(0, s.w.get_pos()).endswith(s.indentation) : 
            ilen = len(s.indentation)
            s.w.set_pos((s.w.get_pos() - ilen))
            s.w.delete(s.w.get_pos(), ilen)




    def run_script(s, path = None):
        if s.contents != [] : 
            s.contents[s.current_w] = s.w.get()
            s.poss[s.current_w] = s.w.get_pos()
        import appswitch
        if path is None : 
            ask_script = file_manager.AskFile(path = s.default_fetch_dir, ext = ['.' + et for et in db['ext']], multi = False, body_process = True, dirs = eval(db['work_dirs']))
            if ask_script == [] : 
                return None
            ask_script = cn(ask_script[0])
        else : 
            ask_script = cn(path)
        if appswitch.switch_to_bg(u'Inspect') : 
            if ui.query(cn('必须关闭当前测试才能进行新的测试，现在关闭？'), 'query') : 
                if  not (appswitch.end_app(u'Inspect')) : 
                    appswitch.kill_app(u'Inspect')
                e32.ao_sleep(0.5)
            else : 
                return None
            pass
        if  not (os.path.isdir('d:\\iPro7_Inspecting\\')) : 
            try :
                os.mkdir('d:\\iPro7_Inspecting\\')
            except :
                ui.note((cn('无法运行\n%s') % ask_script), 'error')
                return None
            pass
        try :
            f = open(en(ask_script))
            w_get = f.read()
            f.close()
        except :
            ui.note((cn('无法运行\n%s') % ask_script), 'error')
        try :
            f = open('d:\\Inspect_Dir', 'w')
            f.write(os.path.dirname(en(ask_script)))
            f.close()
        except :
            pass
        if s.inspect_add_lock and w_get != '' : 
            end = "\n\n\nexec(u'import e32\\ne32.Ao_lock().wait()', {}, {})"
        else : 
            end = ''
        try :
            get = ''.join([w_get, end])
            file = open('d:\\iPro7_Inspecting\\default.py', 'w')
            try :
                file.write(get)
            finally :
                file.close()
        except ImportError : 
            ui.note(cn('无法进行测试'), 'error')
            return None
        if e32.s60_version_info >= (3, 0) : 
            e32.start_exe(disk + '\\sys\\bin\\Inspect_0xeff20111.exe', '')
        else : 
            e32.start_exe('z:\\system\\programs\\apprun.exe', disk + '\\System\\apps\\iPro7\\Inspect\\Inspect.app')
        s.focus_func = None




    def shell(s):
        import appswitch
        if s.py_version=='1.45':
            shell_name=u'Shell'
        else:
            shell_name=u'Shell2'
        if appswitch.switch_to_bg(shell_name) : 
            appswitch.switch_to_fg(shell_name)
        elif e32.s60_version_info >= (3, 0) : 
            try :
                e32.start_exe(s.shell_path, '')
            except :
                ui.note(cn('无法启动解释器'), 'error')
            pass
        else : 
            try :
                e32.start_exe('z:\\system\\programs\\apprun.exe', s.shell_path)
            except :
                ui.note(cn('无法启动解释器'), 'error')
            pass




    def inspect(s):
        s.contents[s.current_w] = s.w.get()
        if s.contents[s.current_w].startswith(u'#tested by Inspect2\u2029') or (s.py_version=='2.0' and not(s.contents[s.current_w].startswith(u'#tested by Inspect\u2029'))) :
            inspect_name=u'Inspect2'
            exe_name='Inspect2_0xeff20113'
        else:
            inspect_name=u'Inspect'
            exe_name='Inspect_0xeff20111'
        s.poss[s.current_w] = s.w.get_pos()
        import appswitch
        if appswitch.switch_to_bg(inspect_name) : 
            if ui.query(cn('必须关闭当前测试才能进行新的测试，现在关闭？'), 'query') : 
                if  not (appswitch.end_app(inspect_name)) : 
                    appswitch.kill_app(inspect_name)
                e32.ao_sleep(0.5)
            else : 
                return None
            pass
        if  not (os.path.isdir('d:\\iPro7_Inspecting\\')) : 
            try :
                os.mkdir('d:\\iPro7_Inspecting\\')
            except :
                ui.note(cn('无法进行测试'), 'error')
                return None
            pass
        w_get = s.contents[s.current_w].replace(u'\r\u2029', u'\r\n').replace(u'\u2029', u'\r\n').replace(u'\r\u2028', u'\r\n').replace(u'\u2028', u'\r\n')
        try :
            f = open('d:\\Inspect_Dir', 'w')
            f.write(os.path.dirname(s.file_paths[s.current_w]))
            f.close()
        except :
            pass
        if s.inspect_add_lock and w_get != u'' : 
            end = "\n\n\nexec(u'import e32\\ne32.Ao_lock().wait()', {}, {})"
        else : 
            end = ''
        try :
            get = ''.join([en(w_get), end])
            file = open('d:\\iPro7_Inspecting\\default.py', 'w')
            try :
                file.write(get)
            finally :
                file.close()
        except ImportError : 
            ui.note(cn('无法进行测试'), 'error')
            return None
        if e32.s60_version_info >= (3, 0) : 
            e32.start_exe(disk + '\\sys\\bin\\%s.exe'%exe_name, '')
        else : 
            e32.start_exe('z:\\system\\programs\\apprun.exe', disk + '\\System\\apps\\iPro7\\Inspect\\Inspect.app')
        s.focus_func = s.to_mistake




    def to_mistake(s, fg):
        if  not (fg) or ui.app.body != s.w or not(os.path.isfile('d:\\inspect_mistake')) : 
            return None
        import re
        m = open('d:\\inspect_mistake', 'r')
        rm = m.read()
        m.close()
        os.remove('d:\\inspect_mistake')
        location = '  File "d:\\iPro7_Inspecting\\default.py", line '
        location_re = re.compile(location.replace('\\', '\\\\') + '\\d\\d?\\d?\\d?\\d?\\d?\\d?\\d?')
        find_mistake = location_re.finditer(rm)
        mistake_line = None
        for i in find_mistake:
            mistake_line = rm[i.start() + len(location) : i.end()]
        if mistake_line==None:
            return None
        s.infopopup.show((cn('第%s行发生错误') % mistake_line), (0, 0), 3000, 0)
        if len(s.w.get(0, s.w.get_pos()).split(u'\u2029')) != int(mistake_line) : 
            try :
                s.to_line(int(mistake_line))
            except:
                import traceback,sys
                traceback.print_exception(*sys.exc_info())
                pass

    def jump(s):
        list=[cn('跳转行数'), cn('跳转百分比'),cn('上一页'), cn('下一页'), cn('跳至行首'), cn('跳至行尾'), cn('跳至开头'), cn('跳至底部')]
        select=ui.popup_menu(list, cn('跳转'))
        if select==None:return None
        elif select==0:s.to_line()
        elif select==1:s.to_percent()
        elif select==2:s.last_page()
        elif select==3:s.next_page()
        elif select==4:s.to_linestart()
        elif select==5:s.to_lineend()
        elif select==6:s.to_start()
        elif select==7:s.to_end()

    def last_page(s):
        ui.app.body.page_up()

    def next_page(s):
        ui.app.body.page_down()

    def to_linestart(s):
        ui.app.body.move(ui.EFLineBeg)

    def to_lineend(s):
        ui.app.body.move(ui.EFLineEnd)

    def to_start(s):
        ui.app.body.set_pos(0)

    def to_end(s):
        ui.app.body.set_pos(ui.app.body.len())

    def to_line(s, line = None):
        s.get = ui.app.body.get()
        split = s.get.split(u'\u2029')
        if line is None : 
            current_pos = ui.app.body.get_pos()
            current_line = (s.get[0 : current_pos].count(u'\u2029') + 1)
            ui.app.body.focus = False
            target_line = ui.query((cn('跳转行数(1~%d)') % len(split)), 'number', current_line)
            ui.app.body.focus = True
        else : 
            target_line = line
        target_pos = 0
        if target_line != None : 
            if target_line == 0 : 
                target_line = 1
            elif target_line > len(split) : 
                target_line = len(split)
            for w in range((target_line - 1)):
                target_pos += len(split[w]) + 1
            ui.app.body.set_pos(target_pos)

    def to_percent(s):
        length=ui.app.body.len()
        if length == 0 : 
            return None
        percent = ui.query(cn('百分比'), 'number', int(((ui.app.body.get_pos() * 100) / length)))
        if percent is None : 
            return None
        ui.app.body.set_pos(int(((length * percent) / 100)))

    def highlight_handle(s, start = None, end = None):
        if not s.open_highlight : 
            return None
        if (s.w.len() / 1024) > db['largest_highlight_file'] : 
            return None
        import re
        get = s.w.get()
        if start == None : 
            start = 0
        if end == None : 
            end = len(get)
        get = get[start : end]
        s.w.color = s.highlight_color
        s.w.style = s.highlight_style
        scan_re = re.compile(u'\\b('+u'|'.join(s.keywords)+u')\\b')
        for i in scan_re.finditer(get):
            s.w.apply(start + i.start(), len(i.group()))
        s.w.color = s.font_color
        s.w.style = 0
        if s.w.len() < 3000 : 
            ui.app.body = s.w
        else : 
            s.w.insert(0, u'\n'*50)
            s.w.delete(0, 50)

    def keyword_highlight(s, x = None, y = None, insert = True):
        if not(s.open_highlight) and not(s.keyword_blank) : 
            return None
        symbol_list = [u' ', u'(', u')', u'[', u']', u'{', u'}', u'\\', u':', u'\u2029']
        get = s.w.get(0, s.w.get_pos())
        for i in s.keywords:
            if get.endswith(i) : 
                if s.w.get_pos() != len(i) and s.w.get(((s.w.get_pos() - len(i)) - 1), 1) not in symbol_list : 
                    return None
                if s.w.get_pos() != s.w.len() and s.w.get(s.w.get_pos(), 1) not in symbol_list : 
                    return None
                if s.open_highlight and s.w.len() / 1024<= db['largest_highlight_file'] : 
                    s.w.color = s.highlight_color
                    s.w.style = s.highlight_style
                    s.w.apply((s.w.get_pos() - len(i)), len(i))
                    s.w.color = s.font_color
                    s.w.style = 0
                    if insert : 
                        s.w.insert(s.w.get_pos(), u'')
                    pass
                if s.keyword_blank and insert : 
                    if y is None or y != len(i) : 
                        return None
                    if i in (u'else', u'try', u'finally') : 
                        try :
                            if s.w.get(s.w.get_pos(), 1) == u':' : 
                                return None
                        except SymbianError : 
                            pass
                        s.w.insert(s.w.get_pos(), u':')
                        s.w.set_pos((s.w.get_pos() + 1))
                        s.newline()
                        return None
                    elif i in (u'pass', u'break', u'continue') : 
                        return None
                    try :
                        if s.w.get(s.w.get_pos(), 1) == u' ' : 
                            s.w.set_pos((s.w.get_pos() + 1))
                            return None
                    except :
                        pass
                    s.w.insert(s.w.get_pos(), u' ')
                    s.w.set_pos((s.w.get_pos() + 1))
                return None
        else : 
            if s.open_highlight and y < 0 : 
                s.w.insert(s.w.get_pos(), u'')
            pass

    def exit_key_handle(s):
        if s.shortcut_menu :
            s.show_shortcut_menu()
        else:
            if len(s.contents) > 1 : 
                choose = ui.popup_menu([cn('关闭当前'), cn('关闭其它'), cn('退出')])
                if choose == 0 : 
                    s.kill_window()
                elif choose == 1 : 
                    s.kill_others()
                elif choose == 2 : 
                    s.exit()
                pass
            else : 
                s.exit()


    def show_shortcut_menu(s):
        if len(s.contents) != 1 : 
            choose_list = s.action_names + [cn('退出')]
            choose = ui.popup_menu(choose_list)
            if choose == None:
                return None
            elif choose == len(choose_list)-1 : 
                s.exit()
            else:
                getattr(s, s.action_list[choose])()
            pass
        else:
            choose_list = [x for x in s.action_names if x not in [cn('关闭当前'), cn('关闭其它')]] + [cn('退出')]
            choose = ui.popup_menu(choose_list)
            if choose == None:
                return None
            elif choose == len(choose_list)-1 : 
                s.exit()
            else:
                getattr(s, [x for x in s.action_list if x not in ['kill_window', 'kill_others']][choose])()
            pass

    def schedule_shortcut(s, level):
        if level == s.shortcut_level : 
            s.only_page_shortcut = False
            for k in s.arrow_keys:
                try :
                    k.stop()
                except :
                    pass
            e32.ao_sleep(0, lambda  :  s.stop_shortcut() )

    def shortcut(s):
        if s.shortcut_level > 20 : 
            s.shortcut_level = 0
        s.only_page_shortcut = False
        s.shortcut_level += 1
        current_shortcut_level = s.shortcut_level
        s.w.focus = False
        s.w.read_only = True
        s.prepare_shortcut_keys()
        e32.ao_sleep(1, lambda  :  s.schedule_shortcut(current_shortcut_level) )

    def stop_shortcut(s):
        for k in (EKey0, EKey1, EKey2, EKey3, EKey4, EKey5, EKey6, EKey7, EKey8, EKey9, EKeyYes, EKeySelect, EKeyStar, EKeyHash, EKeyBackspace):
            s.w.bind(k, None)
        s.w.bind(63557, s.newline)
        s.w.bind(63586, s.shortcut)
        s.w.read_only = False
        s.w.focus = True

    def execute_action(s, action):
        s.shortcut_level += 1
        if action in ('last_page', 'next_page') : 
            current_shortcut_level = s.shortcut_level
            s.only_page_shortcut = True
            getattr(s, action)()
            e32.ao_sleep(1, lambda  :  s.schedule_shortcut(current_shortcut_level) )
            return None
        for k in s.arrow_keys:
            try :
                k.stop()
            except :
                pass
        e32.ao_sleep(0, lambda  :  s.exec_attr(action) )

    def exec_attr(s, action):
        s.stop_shortcut()
        if  not (action == '未定义') and not(s.only_page_shortcut) : 
            getattr(s, action)()

    def prepare_shortcut_keys(s):
        s.w.bind(EKey0, lambda  :  s.execute_action(db['ct_0']) )
        s.w.bind(EKey1, lambda  :  s.execute_action(db['ct_1']) )
        s.w.bind(EKey2, lambda  :  s.execute_action(db['ct_2']) )
        s.w.bind(EKey3, lambda  :  s.execute_action(db['ct_3']) )
        s.w.bind(EKey4, lambda  :  s.execute_action(db['ct_4']) )
        s.w.bind(EKey5, lambda  :  s.execute_action(db['ct_5']) )
        s.w.bind(EKey6, lambda  :  s.execute_action(db['ct_6']) )
        s.w.bind(EKey7, lambda  :  s.execute_action(db['ct_7']) )
        s.w.bind(EKey8, lambda  :  s.execute_action(db['ct_8']) )
        s.w.bind(EKey9, lambda  :  s.execute_action(db['ct_9']) )
        s.w.bind(EKeyYes, lambda  :  s.execute_action(db['ct_green']) )
        s.w.bind(EKeySelect, lambda  :  s.execute_action(db['ct_ok']) )
        s.w.bind(EKeyStar, lambda  :  s.execute_action(db['ct_star']) )
        s.w.bind(EKeyHash, lambda  :  s.execute_action(db['ct_hash']) )
        s.w.bind(EKeyBackspace, lambda  :  s.execute_action('delete_indentation') )
        s.ct_up = s.KeyCapturer(lambda m, :  s.execute_action(db['ct_up']) )
        s.ct_down = s.KeyCapturer(lambda m, :  s.execute_action(db['ct_down']) )
        s.ct_left = s.KeyCapturer(lambda m, :  s.execute_action(db['ct_left']) )
        s.ct_right = s.KeyCapturer(lambda m, :  s.execute_action(db['ct_right']) )
        s.ct_up.keys = (EKeyUpArrow, )
        s.ct_down.keys = (EKeyDownArrow, )
        s.ct_left.keys = (EKeyLeftArrow, )
        s.ct_right.keys = (EKeyRightArrow, )
        s.arrow_keys = (s.ct_up, s.ct_down, s.ct_left, s.ct_right)
        for k in s.arrow_keys:
            k.start()

    def read_funcs(s):
        funcs=Read_Funcs()
        ui.app.bind_mediakeys(funcs.last_page, funcs.next_page, lambda : funcs.last_page(1), lambda : funcs.next_page(1))
        funcs.read_funcs()
        ui.app.bind_mediakeys(s.last_page, s.next_page)

    def get_file_size(s, path):
        if  not (os.path.isfile(path)) : 
            return u''
        size = os.path.getsize(path)
        if size < 1024 : 
            return (u'%d B' % size)
        else : 
            return (u'%.2f KB' % (size / 1024.0))

    def get_file_time(s, path):
        import time
        if path == '' : 
            return u''
        try :
            getmtime = os.path.getmtime(path)
        except :
            return u''
        localtime = time.localtime((getmtime - time.timezone))
        getmtime = (u'%d-%02d-%02d %02d:%02d:%02d' % localtime[ : 6])
        return getmtime

    def file_details(s):
        import globalui
        e32.ao_yield()
        globalui.global_msg_query(u'\n'.join([(zw('路径: %s') % zw(s.file_paths[s.current_w])), (zw('时间: %s') % s.get_file_time(s.file_paths[s.current_w])), (zw('长度: %d(%d)') % (s.w.len(), s.w.get_pos())), (zw('行数: %d(%d)') % (len(s.w.get().split(u'\u2029')), len(s.w.get()[ : s.w.get_pos()].split(u'\u2029')))), (zw('窗口: %d(%d)') % (len(s.contents), (s.current_w + 1))), (zw('编码: %s') % s.codes[s.current_w].replace('u8', 'utf-8')), (zw('大小: %s') % s.get_file_size(s.file_paths[s.current_w])), (zw('状态: %s') % [zw('已修改'), zw('未修改')][s.w.get() == s.initial_contents[s.current_w]])]), zw('文件详情'))

    def insert_mould(s):
        moulds = os.listdir(disk + '\\System\\iPro7\\Mould\\')
        all_moulds = [cn(os.path.splitext(x)[0]) for x in moulds]
        if all_moulds == [] : 
            ui.note(cn('无模板'))
            return None
        read_funcs = Read_Funcs()
        read_funcs.prepare()
        read_funcs.start_capture()
        old_focus = s.focus_func
        s.focus_func = read_funcs.focus
        e32.ao_yield()
        choose = ui.popup_menu(all_moulds, cn('插入模板'))
        s.focus_func = old_focus
        read_funcs.stop_capture()
        if choose is None : 
            return None
        else : 
            try :
                open_mould = open(disk + '\\System\\iPro7\\Mould\\' + moulds[choose])
            except :
                ui.note(cn('模板异常'), 'error')
                return None
            pos = ui.app.body.get_pos()
            try :
                try :
                    read_mould = cn(open_mould.read())
                finally :
                    open_mould.close()
            except :
                ui.note(cn('模板异常'), 'error')
                return None
            s.w.focus = False
            s.w.insert(pos, read_mould)
            e32.ao_yield()
            try :
                s.highlight_handle(pos, pos + len(read_mould))
            except :
                ui.note(cn('无法高亮处理'), 'error')
            s.w.set_pos(pos)
            try :
                f = open(disk + '\\System\\iPro7\\Mould_Pos\\' + moulds[choose])
                try :
                    s.w.set_pos(pos + int(f.read()))
                finally :
                    f.close()
            except :
                s.w.set_pos(pos + len(read_mould))
            s.w.focus = True

    def write_shortcut_data(s, k, a):
        exec ("db['ct_%s'] = a" % k)

    def set(s):
        
        def item(list):
            return map(lambda i : ui.Item(i[0], subtitle=i[1]), list)

        def backup():
            path=disk+'\\system\\iPro7\\settings.ini.bak'
            if ui.query(cn('备份设置至%s?'%path), 'query'):
                if os.path.exists(path):
                    if not ui.query(cn('要覆盖备份吗?'), 'query'):
                        return None
                try:
                    db.backup(path)
                    ui.note(cn('设置已备份!'), 'conf')
                except:
                    
                    ui.note(cn('备份失败!'), 'error')

        def recover():
            path=disk+'\\system\\iPro7\\settings.ini.bak'
            if not os.path.exists(path):
                ui.note(cn('设置文件%s不存在!'%path), 'error')
                return None
            if ui.query(cn('从%s恢复设置?'%path), 'query'):
                try:
                    db.recover(path)
                    ui.note(cn('设置已恢复!'), 'conf')
                except:
                    ui.note(cn('恢复失败!'), 'error')

        s.contents[s.current_w] = s.w.get()
        s.poss[s.current_w] = s.w.get_pos()
        judge_dict = {0 : cn('禁用'), 1 : cn('开启')}
        def aspect_0():
            list_0 = [(cn('字体颜色'), cn(db['font_color'])), (cn('字体风格'), db['font']), (cn('字体大小'), cn(str(db['font_size']))), (cn('自动缩进'), cn(db['indentation_length'].replace('off', '禁用'))), (cn('快速打开文本'), s.circuit_dict[db['fast_fetch']]), (cn('关键字自动空格'), s.circuit_dict[db['keyword_blank']]), (cn('关键字高亮'), s.circuit_dict[db['open_highlight']]), (cn('高亮颜色'), cn(db['highlight_color'])), (cn('高亮风格'), s.hl_style_dict[db['highlight_style']]), (cn('高亮上限'), (u'%d KB' % db['largest_highlight_file'])), (cn('自动切换输入法'), s.circuit_dict[db['change_input_mode']]), (cn('情景模式'), u'')]
            return list_0

        def aspect_1():
            list_1 = [(cn('系统程序'), s.circuit_dict[db['set_system']]), (cn('测试等待'), s.circuit_dict[db['inspect_add_lock']]), (cn('文件浏览器'), (cn('浏览器%s') % db['file_manager_mode'])), (cn('自动缓存'), s.circuit_dict[db['autosave']]), (cn('缓存间隔'), cn('%d分%d秒'%(db['autosave_time']/60, db['autosave_time']%60))), (cn('快捷键'), u''), (cn('右键快捷菜单'), s.circuit_dict[db['shortcut_menu']]), (cn('设置右键快捷菜单'), u''), (cn('音量键翻页'), s.circuit_dict[db['mediakeys']])]
            return list_1

        def aspect_2():
            list_2 = [(cn('初始界面'), s.initial_body_dict[db['initial_body']]), (cn('屏幕大小'), s.screen_size_dict[db['screen_size']]), (cn('屏幕方向'), s.screen_rotate_dict[db['screen_rotate']]), (cn('主题背景'), judge_dict[db['skinned']]), (cn('文本滚动条'), judge_dict[db['scrollbar']])]
            return list_2

        def aspect_3():
            list_3 = [(cn('默认名称'), cn(db['default_file_name'])), (cn('默认格式'), cn(db['format'])), (cn('设置工作目录'), cn(('%d个' % len(eval(db['work_dirs']))))), (cn('默认打开路径'), cn(db['default_fetch_dir'])), (cn('默认保存路径'), cn(db['default_save_dir'])), (cn('后缀限制'), cn(', '.join(db['ext'])))]
            return list_3

        def aspect_4():
            list_4 = [(cn('Python版本'), cn(db['py_version'])), (cn('默认编码'), cn(db['default_code'])), (cn('拓展插件'), (cn('%d个') % len(os.listdir(extend_iPro7.dir)))), (cn('模板管理'), (cn('%d个') % len(os.listdir(mould.dir)))), (cn('历史记录'), u''), (cn('帮助信息'), u''), (cn('关于作者'), cn('逆浪′'))]
            return list_4

        def aspect_scene():
            list_scene = [(cn('开始时间(时:分)'), (cn('%02d:%02d') % ((s.scene['start'] / 3600), ((s.scene['start'] % 3600) / 60)))), (cn('结束时间(时:分)'), (cn('%02d:%02d') % ((s.scene['end'] / 3600), ((s.scene['end'] % 3600) / 60)))), (cn('字体颜色'), cn(s.scene['font_color'])), (cn('关键字高亮'), s.circuit_dict[s.scene['open_highlight']]), (cn('高亮颜色'), cn(s.scene['highlight_color'])), (cn('高亮风格'), s.hl_style_dict[s.scene['highlight_style']]), (cn('主题背景'), judge_dict[s.scene['skinned']]), (cn('文本滚动条'), judge_dict[s.scene['scrollbar']])]
            return list_scene

        def tab_handle(aspect):
            aspects=[aspect_0, aspect_1, aspect_2, aspect_3, aspect_4]
            set_handles=[set_handle_0, set_handle_1, set_handle_2, set_handle_3, set_handle_4]
            ui.app.body.set_list(item(aspects[aspect]()), 0)
            ui.app.menu = [(cn('选择'), set_handles[aspect])]+default_menu
            ui.app.body.bind(63557, set_handles[aspect])

        def set_shortcut_key():
            action_name = [cn('查找文字'), cn('高级查找'), cn('查找替换'), cn('查找下个'), cn('跳转行数'), cn('跳至开头'), cn('跳至底部'), cn('行首'), cn('行末'), cn('上一页'), cn('下一页'), cn('窗口切换'), cn('关闭窗口'), cn('打开文件'), cn('打开历史'), cn('保存文件'), cn('新建文件'), cn('解释'), cn('测试'), cn('运行'), cn('缩进'), cn('函数浏览'), cn('插入模板'), cn('拓展'), cn('(未定义)')]
            action_list = ['seek', 'senior_seek', 'seek_replace', 'seek_next', 'to_line', 'to_start', 'to_end', 'to_linestart', 'to_lineend', 'last_page', 'next_page', 'change_window', 'kill_window', 'fetch_file', 'fetch_history', 'ask_save', 'build_window', 'shell', 'inspect', 'run_script', 'add_indentation', 'read_funcs', 'insert_mould', 'execute_extend', '未定义']
            choose_key = ui.popup_menu([cn(str(k) + ' ') + action_name[action_list.index(eval(("db['ct_%s']" % k)))] for k in range(1, 10) + [0]] + [cn('通话键 ') + action_name[action_list.index(db['ct_green'])], cn('确定键 ') + action_name[action_list.index(db['ct_ok'])], cn('*键 ') + action_name[action_list.index(db['ct_star'])], cn('#键 ') + action_name[action_list.index(db['ct_hash'])], cn('上 ') + action_name[action_list.index(db['ct_up'])], cn('下 ') + action_name[action_list.index(db['ct_down'])], cn('左 ') + action_name[action_list.index(db['ct_left'])], cn('右 ') + action_name[action_list.index(db['ct_right'])]], cn('拨号键 +'))
            if choose_key is None : 
                return None
            choose_action = ui.popup_menu(action_name, cn('动作'))
            if choose_action != None : 
                keys_list = [str(k) for k in range(1, 10) + [0]]
                keys_list.extend(['green', 'ok', 'star', 'hash', 'up', 'down', 'left', 'right'])
                s.write_shortcut_data(keys_list[choose_key], action_list[choose_action])
            set_shortcut_key()

        def set_shortcut_menu():
            action_names = [cn('查找文字'), cn('高级查找'), cn('查找替换'), cn('查找下个'), cn('跳转行数'), cn('跳至开头'), cn('跳至底部'), cn('行首'), cn('行末'), cn('上一页'), cn('下一页'), cn('窗口切换'), cn('关闭当前'), cn('关闭其它'), cn('打开文件'), cn('打开历史'), cn('保存文件'), cn('新建文件'), cn('解释'), cn('测试'), cn('运行'), cn('缩进'), cn('删除缩进'), cn('函数浏览'), cn('插入模板'), cn('拓展')]
            select = ui.multi_selection_list(action_names, style = 'checkbox')
            if select != ():
                db['shortcut_menu_list'] = select

        def set_scene():

            def go_back():
                db['scene'] = s.scene
                back(11, lst = aspect_0(), sk = set_handle_0, ti = 0, new = False)

            ui.app.exit_key_handler = go_back
            ui.app.menu = [(cn('选择'), set_handle_scene)]+default_menu
            ui.app.set_tabs([], None)
            ui.app.title = cn('情景模式')
            ui.app.body.set_list(item(aspect_scene()), 0)
            ui.app.body.bind(63557, set_handle_scene)

        def set_handle_scene():
            index = ui.app.body.current()
            if index == 0 : 
                ask = ui.query(cn('开始时间'), 'time', s.scene['start'])
                if ask is None : 
                    return None
                s.scene['start'] = ask
            elif index == 1 : 
                ask = ui.query(cn('结束时间'), 'time', s.scene['end'])
                if ask is None : 
                    return None
                else : 
                    if ask < s.scene['start'] : 
                        ui.note(cn('不能小于开始时间'), 'error')
                        return None
                    pass
                s.scene['end'] = ask
            elif index == 2 : 
                red = ui.query(cn('红'), 'number', eval(s.scene['font_color'])[0])
                if red is None : 
                    return None
                green = ui.query(cn('绿'), 'number', eval(s.scene['font_color'])[1])
                if green is None : 
                    return None
                blue = ui.query(cn('蓝'), 'number', eval(s.scene['font_color'])[2])
                if blue is None : 
                    return None
                color = [red, green, blue]
                for i in range(3):
                    if color[i] < 0 : 
                        color[i] = 0
                    elif color[i] > 255 : 
                        color[i] = 255
                s.scene['font_color'] = str(tuple(color))
            elif index == 3 : 
                s.scene['open_highlight'] ^= 1
                pass
            elif index == 4 : 
                red = ui.query(cn('红'), 'number', eval(s.scene['highlight_color'])[0])
                if red is None : 
                    return None
                green = ui.query(cn('绿'), 'number', eval(s.scene['highlight_color'])[1])
                if green is None : 
                    return None
                blue = ui.query(cn('蓝'), 'number', eval(s.scene['highlight_color'])[2])
                if blue is None : 
                    return None
                hl_color = [red, green, blue]
                for i in range(3):
                    if hl_color[i] < 0 : 
                        hl_color[i] = 0
                    elif hl_color[i] > 255 : 
                        hl_color[i] = 255
                s.scene['highlight_color'] = str(tuple(hl_color))
            elif index == 5 : 
                style_choose = ui.popup_menu(s.hl_style_dict.values(), cn('高亮风格'))
                if style_choose is not None : 
                    s.scene['highlight_style'] = s.hl_style_dict.keys()[style_choose]
                pass
            elif index == 6 : 
                s.scene['skinned'] ^= 1
                pass
            elif index == 7 : 
                s.scene['scrollbar'] ^= 1
                pass  
            ui.app.body.set_list(item(aspect_scene()), index)

        def set_handle_0():
            index = ui.app.body.current()
            if index == 0 : 
                red = ui.query(cn('红'), 'number', eval(db['font_color'])[0])
                if red is None : 
                    return None
                green = ui.query(cn('绿'), 'number', eval(db['font_color'])[1])
                if green is None : 
                    return None
                blue = ui.query(cn('蓝'), 'number', eval(db['font_color'])[2])
                if blue is None : 
                    return None
                color = [red, green, blue]
                for i in range(3):
                    if color[i] < 0 : 
                        color[i] = 0
                    elif color[i] > 255 : 
                        color[i] = 255
                db['font_color'] = str(tuple(color))
            elif index == 1 : 
                fonts_dict={'normal': cn('normal(常规)'), 'dense':cn('dense(密集)'), 'symbol':cn('symbol(记号)'), 'legend':cn('legend(图注)'), 'title':cn('title(标题)'), 'annotation':cn('annotation(注解)')}
                fonts_list = fonts_dict.values()+ui.available_fonts()
                try :
                    fonts_list.remove(u'Series 60 ZDigi')
                except ValueError : 
                    pass
                ask = ui.popup_menu(fonts_list, cn('字体风格'))
                if ask is None : 
                    return None
                if ask<6:db['font'] = fonts_dict.keys()[ask]
                else:db['font'] = fonts_list[ask]
            elif index == 2 : 
                size = ui.query(cn('文字大小'), 'number', int(db['font_size']))
                if size is None : 
                    return None
                db['font_size'] = size
            elif index == 3 : 
                choose = ui.popup_menu([cn('自定义'), cn('禁用')], cn('自动缩进'))
                if choose is None : 
                    return None
                elif choose == 0 : 
                    if db['indentation_length'] == 'off' : 
                        old_length = 4
                    else : 
                        old_length = int(db['indentation_length'])
                    ask_length = ui.query(cn('缩进长度'), 'number', old_length)
                    if ask_length is None : 
                        return None
                    elif ask_length < 1 : 
                        ask_length = 1
                    elif ask_length > 10 : 
                        ask_length = 10
                    db['indentation_length'] = str(ask_length)
                elif choose == 1 : 
                    db['indentation_length'] = 'off'
                pass
            elif index == 4 :  
                db['fast_fetch'] ^= 1
                pass
            elif index == 5 : 
                db['keyword_blank'] ^= 1
                pass
            elif index == 6 : 
                db['open_highlight'] ^= 1
                pass
            elif index == 7 : 
                red = ui.query(cn('红'), 'number', eval(db['highlight_color'])[0])
                if red is None : 
                    return None
                green = ui.query(cn('绿'), 'number', eval(db['highlight_color'])[1])
                if green is None : 
                    return None
                blue = ui.query(cn('蓝'), 'number', eval(db['highlight_color'])[2])
                if blue is None : 
                    return None
                hl_color = [red, green, blue]
                for i in range(3):
                    if hl_color[i] < 0 : 
                        hl_color[i] = 0
                    elif hl_color[i] > 255 : 
                        hl_color[i] = 255
                db['highlight_color'] = str(tuple(hl_color))
            elif index == 8 : 
                style_choose = ui.popup_menu(s.hl_style_dict.values(), cn('高亮风格'))
                if style_choose is not None : 
                    db['highlight_style'] = s.hl_style_dict.keys()[style_choose]
                pass
            elif index == 9 : 
                ask_n = ui.query(cn('高亮上限(KB)'), 'number', db['largest_highlight_file'])
                if ask_n is None : 
                    return None
                db['largest_highlight_file'] = ask_n
            elif index == 10 : 
                db['change_input_mode'] ^= 1
                pass
            elif index == 11 : 
                set_scene()
                return None
            ui.app.body.set_list(item(aspect_0()),index)

        def set_handle_1():
            index = ui.app.body.current()
            if index == 0 : 
                db['set_system'] = 1
                pass
            elif index == 1 : 
                db['inspect_add_lock'] ^= 1
                pass
            elif index == 2 : 
                choose=ui.popup_menu([cn("文件浏览器%d"%x) for x in [1, 2, 3]], cn("文件浏览器"))
                if choose!=None:
                    db['file_manager_mode'] = str(choose+1)
                pass
            elif index == 3 :
                db['autosave'] ^= 1
                pass
            elif index == 4 :
                ask_t = ui.query(cn('缓存间隔(分钟:秒钟),00:00为禁用'), 'time', db['autosave_time']*60.)
                if ask_t is None : 
                    return None
                elif ask_t == 0:
                    db['autosave'] = 0
                else:
                    db['autosave_time'] = int(ask_t/60)
            elif index == 5 : 
                set_shortcut_key()
            elif index == 6 :
                db['shortcut_menu'] ^= 1
                pass
            elif index == 7 : 
                ui.app.set_tabs([], None)
                set_shortcut_menu()
                ui.app.set_tabs([cn('文本'), cn('习惯'), cn('界面'), cn('路径'), cn('其他')], tab_handle)
                ui.app.activate_tab(1)
            elif index == 8 :
                db['mediakeys'] ^= 1
                pass
            ui.app.body.set_list(item(aspect_1()),index)

        def set_handle_2():
            index = ui.app.body.current()
            if index == 0 : 
                choose = ui.popup_menu(s.initial_body_dict.values(), cn('初始界面'))
                if choose is None : 
                    return None
                db['initial_body'] = s.initial_body_dict.keys()[choose]
            elif index == 1 : 
                choose = ui.popup_menu(s.screen_size_dict.values(), cn('屏幕大小'))
                if choose is None : 
                    return None
                else:
                    db['screen_size'] = s.screen_size_dict.keys()[choose]
                pass
            elif index == 2 :
                choose = ui.popup_menu(s.screen_rotate_dict.values(), cn('屏幕方向'))
                if choose is None : 
                    return None
                else:
                    db['screen_rotate'] = s.screen_rotate_dict.keys()[choose]
                pass
            elif index == 3 : 
                db['skinned'] ^= 1
                pass
            elif index == 4 : 
                db['scrollbar'] ^= 1
                pass
            ui.app.body.set_list(item(aspect_2()),index)

        def set_handle_3():
            index = ui.app.body.current()
            if index == 0 : 
                ask_name = ui.query(cn('默认文件名'), 'text', cn(db['default_file_name']))
                if ask_name is None : 
                    return None
                db['default_file_name'] = en(ask_name)
            elif index == 1 : 
                ask_format = ui.query(cn('默认格式'), 'text', cn(db['format'][1 : ]))
                if ask_format is None : 
                    return None
                db['format'] = en(u'.' + ask_name)
            elif index == 2 : 
                work_dirs = eval(db['work_dirs'])
                if work_dirs != [] : 
                    ask = ui.popup_menu([cn('添加目录'), cn('删除目录')], cn('工作目录'))
                else : 
                    ask = ui.popup_menu([cn('添加目录')], cn('工作目录'))
                if ask == 0 : 
                    ui.app.set_tabs([], None)
                    ask_work_dir = file_manager.AskDir(auto_return_ui = False)
                    back(2, lst = aspect_3(), sk = set_handle_3, ti = 3)
                    if ask_work_dir is None : 
                        return None
                    try :
                        work_dirs.remove(ask_work_dir)
                    except ValueError : 
                        pass
                    work_dirs.append(ask_work_dir)
                    db['work_dirs'] = str(work_dirs)
                elif ask == 1 : 
                    ask = ui.popup_menu([cn(i) for i in work_dirs], cn('删除工作目录'))
                    if ask is not None : 
                        del work_dirs[ask]
                        db['work_dirs'] = str(work_dirs)
                    pass
                pass
            elif index == 3 : 
                ask = ui.popup_menu([cn('更改'), cn('清除')], cn('默认打开路径'))
                if ask is None : 
                    return None
                elif ask == 1 : 
                    db['default_fetch_dir'] = ''
                    ui.app.body.set_list(item(aspect_3()), 3)
                    return None
                ui.app.set_tabs([], None)
                default_fetch_dir = file_manager.AskDir(auto_return_ui = False)
                back(3, lst = aspect_3(), sk = set_handle_3, ti = 3)
                if default_fetch_dir is None : 
                    return None
                db['default_fetch_dir'] = default_fetch_dir
            elif index == 4 : 
                ask = ui.popup_menu([cn('更改'), cn('清除')], cn('默认保存路径'))
                if ask is None : 
                    return None
                elif ask == 1 : 
                    db['default_save_dir'] = ''
                    ui.app.body.set_list(aspect_2(), 4)
                    return None
                ui.app.set_tabs([], None)
                default_save_dir = file_manager.AskDir(auto_return_ui = False)
                back(4, lst = aspect_3(), sk = set_handle_3, ti = 3)
                if default_save_dir is None : 
                    return None
                db['default_save_dir'] = default_save_dir
            elif index == 5 : 
                ext = db['ext']
                if ext != [] : 
                    ask = ui.popup_menu([cn('添加限制'), cn('删除限制')], cn('后缀限制'))
                else : 
                    ask = ui.popup_menu([cn('添加限制')], cn('后缀限制'))
                if ask == 0 : 
                    ask_ext = ui.query(cn('添加限制'), 'text')
                    if ask_ext is None : 
                        return None
                    ask_ext = en(ask_ext)
                    try :
                        ext.remove(ask_ext)
                    except ValueError : 
                        pass
                    ext.append(ask_ext)
                    db['ext'] = ext
                elif ask == 1 : 
                    ask = ui.popup_menu([cn(i) for i in ext], cn('删除限制'))
                    if ask is not None : 
                        del ext[ask]
                        db['ext'] = ext
                    pass
                pass
            ui.app.body.set_list(item(aspect_3()),index)

        def set_handle_4():
            index = ui.app.body.current()
            if index == 0:
                if db['py_version'] == '1.45':
                    db['py_version'] = '2.0'
                else:
                    db['py_version'] = '1.45'
                ui.app.body.set_list(item(aspect_4()),index)
                pass
            if index == 1 : 
                choose = ui.popup_menu(s.codes_list, cn('默认编码(%s)'%db['default_code']))
                if choose is not None : 
                    db['default_code'] = en(s.codes_list[choose])
                ui.app.body.set_list(item(aspect_4()),index)
                pass
            elif index == 2 : 
                ui.app.set_tabs([], None)
                extend_iPro7.manager(back_callback = lambda  :  back(1) )
            elif index == 3 : 
                ui.app.set_tabs([], None)
                mould.manager(back_callback = lambda  :  back(2) )
            elif index == 4 : 
                ui.app.set_tabs([], None)
                manager = File_Manager(disk + '\\System\\iPro7\\file_manager_icons.mbm')
                manager.AskFile(path = '历史文件\\', history_read_only = True, body_process = False)
                del manager
                ui.app.set_tabs([cn('文本'), cn('习惯'), cn('界面'), cn('路径'), cn('其他')], tab_handle)
                ui.app.activate_tab(4)
            elif index == 5 : 
                s.help()
            elif index == 6 : 
                s.vendor()

        def back(index, lst = None, sk = set_handle_3, ti = 3, new = True):
            if lst is None : 
                lst = aspect_3()
            if new:
                lb = ui.Listbox2(item(lst),double=True)
                lb.set_current(index)
                ui.app.body = lb
            else:
                ui.app.body.set_list(item(lst), index)
            ui.app.title = cn('设置')
            ui.app.body.bind(63557, sk)
            ui.app.set_tabs([cn('文本'), cn('习惯'), cn('界面'), cn('路径'), cn('其他')], tab_handle)
            ui.app.activate_tab(ti)
            ui.app.menu = [(cn('选择'), sk)]+default_menu
            ui.app.exit_key_handler = return_ui

        def return_ui():
            global file_manager
            ui.app.title = cn('请稍候...')
            s.read_db()
            if db['file_manager_mode'] == '1' : 
                file_manager = File_Manager(disk + '\\System\\iPro7\\file_manager_icons.mbm')
            elif  db['file_manager_mode']=='2': 
                file_manager = File_Manager2()
            elif  db['file_manager_mode']=='3': 
                file_manager = File_Manager3()
            e32.ao_yield()
            s.update_ui()

        ui.app.body = None
        ui.app.screen = 'normal'
        ui.app.body = ui.Listbox2(item(aspect_0()), double=True)
        ui.app.body.bind(63557, set_handle_0)
        ui.app.body.bind(42, s.last_page)
        ui.app.body.bind(35, s.next_page)
        ui.app.title = cn('设置')
        ui.app.set_tabs([cn('文本'), cn('习惯'), cn('界面'), cn('路径'), cn('其他')], tab_handle)
        default_menu = [(cn('上一页[*]'), s.last_page), (cn('下一页[#]'), s.next_page), (cn('备份设置'), backup), (cn('恢复设置'), recover), (cn('帮助'), s.help), (cn('返回'), return_ui)]
        ui.app.menu = [(cn('选择'), set_handle_0)]+default_menu
        ui.app.exit_key_handler = return_ui

    def help(s):
        import globalui
        open_help = open(disk + '\\System\\iPro7\\help', 'r')
        read_help = open_help.read().decode('u8')
        open_help.close()
        globalui.global_msg_query(read_help, cn('帮助'))

    def vendor(s):
        import globalui
        globalui.global_msg_query((cn('iPro7_v%s\n%s\nCopyright © 2010-2012 逆浪′\n逆浪′(乐讯ID: 18710035)开发。\nzl@sun (乐讯ID:32826999)修改更新。\n乐讯开发论坛(http://py.t.lexun.com)欢迎您。') % (cn(__version__), cn(__date__))), cn('作者'))

    def exit(s):
        cache = 0
        s.contents[s.current_w] = s.w.get()
        s.poss[s.current_w] = s.w.get_pos()
        if len(s.contents) == 1 : 
            if s.contents[0] != s.initial_contents[0] : 
                ask = ui.popup_menu([cn('保存'), cn('缓存'), cn('不保存')], cn('即将退出，保存文件?'))
                if ask is None : 
                    return None
                elif ask == 0 : 
                    if  not (s.ask_save()) : 
                        return None
                elif ask == 1:
                    cache=1
            else:
                ask = ui.query(cn('要退出吗?'), 'query')
                if ask == None: return None
        else : 
            ask = ui.popup_menu([cn('缓存所有文件'), cn('放弃所有文件')], cn('缓存文件'))
            if ask is None : 
                return None
            elif ask == 0 : 
                cache = 1
            pass
        if not cache:
            sys.exitfunc = lambda  : None 
        try :
            ao_lock.signal()
        except :
            pass
        windows_db['contents'] = ['']
        windows_db['file_paths'] = ['']
        windows_db['poss'] = [0]
        windows_db['windows'] = [cn('新建文件')]
        windows_db['codes'] = [db['default_code']]
        windows_db['current_w'] = 0
        windows_db['last_file_path'] = s.file_paths[s.current_w]
        windows_db['last_pos'] = s.poss[s.current_w]
        windows_db['last_code'] = s.codes[s.current_w]
        import appswitch
        if (appswitch.switch_to_bg(u'Inspect') or appswitch.switch_to_bg(u'Inspect2')) and ui.query(cn('正在进行测试，关闭当前测试？'), 'query') : 
            appswitch.end_app(u'Inspect')
            appswitch.end_app(u'Inspect2')
        if (appswitch.switch_to_bg(u'Shell') or  appswitch.switch_to_bg(u'Shell2')) and ui.query(cn('解释器正在运行，关闭解释器？'), 'query') : 
            appswitch.end_app(u'Shell')
            appswitch.end_app(u'Shell2')
        ui.app.set_exit()

    def del_attributes(s):
        for a in dir(s):
            try :
                exec ('del s.%s' % a, {'s' : s})
            except :
                pass

    def cache(s):
        if s.contents != [] : 
            s.contents[s.current_w] = s.w.get()
            s.poss[s.current_w] = s.w.get_pos()
            windows_db.set_items(contents = s.contents, current_w = s.current_w, windows = s.windows, file_paths = s.file_paths, codes = s.codes, poss = s.poss, last_file_path = s.file_paths[s.current_w], last_pos = s.poss[s.current_w], last_code = s.codes[s.current_w])
        try :
            ao_lock.signal()
        except :
            pass


class Mould(object, ) :

    def __init__(s, dir, pos_dir):
        s.dir = dir
        s.pos_dir = pos_dir
        if  not (os.path.isdir(dir)) : 
            try :
                os.makedirs(dir)
            except :
                ui.note(cn('模板功能出错'), 'error')
            pass
        if  not (os.path.isdir(pos_dir)) : 
            try :
                os.makedirs(pos_dir)
            except :
                ui.note(cn('模板功能出错'), 'error')
            pass

    def _add_mould(s):
        ask_mould = file_manager.AskFile(ext = ['.py', '.txt'], dirs = eval(db['work_dirs']), multi = False)
        if ask_mould == [] : 
            return None
        ask_mould = ask_mould[0]
        mould_path = cn(s.dir) + (u'%s.py' % cn(os.path.splitext(os.path.basename(ask_mould))[0]))
        while True : 
            if os.path.exists(en(mould_path)) : 
                ask_cover = ui.popup_menu([cn('重命名'), cn('覆盖')], cn('同名模板已存在'))
                if ask_cover is None : 
                    return None
                elif ask_cover == 0 : 
                    name = ui.query(cn('模板名'), 'text')
                    if name is None : 
                        return None
                    mould_path = s.dir + name + u'.py'
                else : 
                    break
                pass
            else : 
                break
        try :
            e32.file_copy(mould_path, ask_mould)
            s.mould_list.insert(0, os.path.splitext(os.path.basename(mould_path))[0])
            s.lb.insert(0, ui.Item(s.mould_list[0]))
            s.lb.set_current(0)
        except :
            ui.note(cn('无法添加'), 'error')

    def _edit_pos(s):
        try :
            f = open(s.dir + en(s.lb.current_item().__dict__['title']) + '.py')
            try :
                length = len(f.read().decode('u8'))
            finally :
                f.close()
        except :
            ui.note(cn('模板错误'), 'error')
            return None
        try :
            f = open(s.pos_dir + en(s.lb.current_item().__dict__['title']) + '.py')
            try :
                old_pos = int(f.read())
            finally :
                f.close()
        except :
            old_pos = length
        ask = ui.query(cn('光标位置'), 'number', old_pos)
        if ask is None : 
            return None
        elif ask > length : 
            ask = length
            ui.note(cn('光标位置超出模板长度，已自动更改为模板长度'))
        try :
            f = open(s.pos_dir + en(s.lb.current_item().__dict__['title']) + '.py', 'w')
            try :
                f.write(str(ask))
            finally :
                f.close()
        except :
            ui.note(cn('无法保存设置'), 'error')

    def _edit(s):
        try :
            f = open(s.dir + en(s.lb.current_item().__dict__['title']) + '.py')
        except :
            ui.note(cn('无法打开编辑'), 'error')
            return None
        try :
            try :
                fr = f.read().decode('u8').replace(u'\r\n', u'\n')
            finally :
                f.close()
        except :
            ui.note(cn('无法打开编辑'), 'error')
            return None

        old_title = ui.app.title
        old_menu = ui.app.menu
        old_exit_key = ui.app.exit_key_handler
        old_body = ui.app.body
        def edit_pos():
            try :
                f = open(s.pos_dir + en(s.lb.current_item().__dict__['title']) + '.py', 'w')
                try :
                    f.write(str(w.get_pos()))
                    ui.note((cn('光标位置已更改为\n%d') % w.get_pos()), 'conf')
                finally :
                    f.close()
            except :
                ui.note(cn('无法保存设置'), 'error')

        def back(ask = True):
            if ask and w.get() != initial : 
                ask_save = ui.popup_menu([cn('保存'), cn('取消')], cn('文件已修改'))
                if ask_save is None : 
                    return None
                elif ask_save == 0 : 
                    try :
                        f = open(s.dir + en(s.lb.current_item().__dict__['title']) + '.py', 'w')
                    except :
                        ui.note(cn('无法保存'), 'error')
                        return None
                    try :
                        f.write(w.get().replace(u'\u2029', u'\n').encode('u8'))
                        f.close()
                    except :
                        ui.note(cn('文件错误'), 'error')
                        return None
                    pass
                pass
            ui.app.title = old_title
            ui.app.body = old_body
            ui.app.menu = old_menu
            ui.app.exit_key_handler = old_exit_key
            ui.app.body.bind(8, s._del_mould)

        ui.app.title = s.lb.current_item().__dict__['title']
        ui.app.body = w = ui.Text(scrollbar=1)
        initial = fr.replace(u'\n', u'\u2029')
        try :
            w.set(fr)
        except :
            ui.note(cn('无法打开编辑'), 'error')
            back(ask = False)
            return None
        ui.app.menu = [(cn('设定光标'), edit_pos), (cn('返回'), back)]
        ui.app.exit_key_handler = back

    def _rename(s):
        ask = ui.query(cn('重命名'), 'text', s.lb.current_item().__dict__['title'])
        if ask is None : 
            return None
        try :
            os.rename(s.dir + en(s.lb.current_item().__dict__['title']) + '.py', s.dir + en(ask) + '.py')
            try :
                os.rename(s.pos_dir + en(s.lb.current_item().__dict__['title']) + '.py', s.dir + en(ask) + '.py')
            except :
                pass
        except :
            ui.note(cn('无法重命名'), 'error')
            return None
        s.lb.current_item().__dict__['title'] = ask
        s.lb[s.lb.current()] = s.lb[s.lb.current()]

    def _del_mould(s):
        if len(s.lb) == 0 : 
            return None
        index = s.lb.current()
        if ui.query((cn("删除\n'%s'？") % s.mould_list[index]), 'query') : 
            try :
                os.remove(s.dir + en(s.mould_list[index] + u'.py'))
                try :
                    os.remove(s.pos_dir + en(s.mould_list[index] + u'.py'))
                except :
                    pass
                if index == (len(s.lb) - 1) : 
                    s.lb.set_current((index - 1))
                del s.lb[index]
                del s.mould_list[index]
            except :
                ui.note(cn('无法删除'), 'error')
            pass

    def _del_all_mould(s):
        if ui.query(cn('删除所有模板？'), 'query') : 
            new_mould_list = []
            for m in s.mould_list:
                try :
                    os.remove(s.dir + en(m + u'.py'))
                except :
                    ui.note((cn("无法删除\n'%s'") % m), 'error')
                    new_mould_list.append(m)
            del s.mould_list[:]
            s.mould_list.extend(new_mould_list)
            del s.lb[:]
            s.lb.extend([ui.Item(x) for x in s.mould_list])

    def press(s):
        if s.first:
            s.first=False
            return 
        list = [cn('编辑'), cn('光标'), cn('重命名'), cn('删除')]
        index=ui.popup_menu(list, cn('操作'))
        if index==None:return 
        if index==0:s._edit()
        if index==1:s._edit_pos()
        if index==2:s._rename()
        if index==3:s._del_mould()

    def manager(s, back_callback):
        s.first=True
        s.lb = ui.Listbox2([],s.press)
        s.mould_list = [cn(os.path.splitext(x)[0]) for x in os.listdir(s.dir)]
        s.lb.extend([ui.Item(x) for x in s.mould_list])
        ui.app.body = s.lb
        ui.app.title = cn('模板管理')
        ui.app.body.bind(8, s._del_mould)
        ui.app.exit_key_handler = back_callback
        ui.app.menu = [(cn('添加'), s._add_mould), (cn('编辑'), s._edit), (cn('光标'), s._edit_pos), (cn('重命名'), s._rename), (cn('删除(8)'), s._del_mould), (cn('清空'), s._del_all_mould)]


class Extend_iPro7(object, ) :

    def __init__(s, dir, help_dir):
        s.dir = dir
        s.help_dir = help_dir
        if  not (os.path.isdir(dir)) : 
            try :
                os.makedirs(dir)
            except :
                ui.note(cn('拓展功能出错'), 'error')
            pass
        if  not (os.path.isdir(help_dir)) : 
            try :
                os.makedirs(help_dir)
            except :
                ui.note(cn('拓展功能出错'), 'error')
            pass

    def read_info(s, name):
        try :
            f = open(s.help_dir + name, 'r')
        except :
            return cn('未知')
        try :
            try :
                return f.read().decode('u8')
            finally :
                f.close()
        except :
            return cn('未知')

    def _install_extend(s):
        import zipfile
        import globalui
        if  not (os.path.isdir(s.dir)) : 
            os.makedirs(s.dir)
        ask = file_manager.AskFile(ext = ['.zip'], multi = False, dirs = eval(db['work_dirs']), able_history = False)
        if ask == [] : 
            return None
        else : 
            ask = cn(ask[0])
        try :
            f = zipfile.ZipFile(en(ask), 'r')
        except :
            ui.note(cn('Zip文件有误'), 'error')
            return None
        if f.testzip() is not None : 
            ui.note(cn('Zip文件已损坏'), 'error')
            f.close()
            return None
        namelist = [n for n in f.namelist() if os.path.splitext(n)[-1].lower() in ('.py', '.pyc') ]
        if namelist == [] : 
            ui.note(cn('未找到有效插件'), 'error')
            return None
        e32.ao_yield()
        for name in namelist:
            path = s.dir + name
            is_cover = False
            try :
                current_info = (f.read(os.path.splitext(name)[0] + '.txt')).decode('u8')
            except :
                current_info = cn('未知')
            if os.path.isfile(path) : 
                ask_cover = globalui.global_msg_query((cn('原版本:\n%s\n现版本:\n%s\n是否覆盖安装？') % (s.read_info(os.path.splitext(name)[0] + '.txt'), current_info)), (cn("'%s'已存在") % cn(name)))
                if ask_cover : 
                    is_cover = True
                else : 
                    return None
                pass
            elif  not (globalui.global_msg_query(current_info, cn(name))) : 
                return None
            try :
                fe = open(path, 'w')
            except :
                ui.note((cn('安装失败\n%s') % cn(name)), 'error')
                return None
            try :
                try :
                    fe.write(f.read(name))
                finally :
                    fe.close()
            except :
                ui.note((cn('安装失败\n%s') % cn(name)), 'error')
                return None
            if  not (is_cover) : 
                s.extend_list.insert(0, cn(name))
                s.lb.insert(0, ui.Item(s.extend_list[0]))
            s.lb.set_current(0)
            infoname = os.path.splitext(name)[0] + '.txt'
            if infoname not in f.namelist() : 
                continue
            try :
                if  not (os.path.isdir(s.help_dir)) : 
                    os.makedirs(s.help_dir)
                fi = open(s.help_dir + infoname, 'w')
            except :
                ui.note((cn('无法载入插件信息\n%s') % infoname))
                continue
            try :
                try :
                    fi.write(f.read(infoname))
                finally :
                    fi.close()
            except :
                ui.note((cn('无法载入插件信息\n%s') % infoname))
                continue
        ui.note(cn('安装完成，重启软件生效。'), 'conf')

    def _uninstall_extend(s):
        if len(s.lb) == 0 : 
            return None
        index = s.lb.current()
        if ui.query((cn("卸载插件\n'%s'？") % s.extend_list[index]), 'query') : 
            try :
                os.remove(s.dir + en(s.extend_list[index]))
                try :
                    os.remove(s.help_dir + en(os.path.splitext(s.extend_list[index])[0]) + '.txt')
                except :
                    pass
                if index == (len(s.lb) - 1) : 
                    s.lb.set_current((index - 1))
                del s.lb[index]
                del s.extend_list[index]
            except :
                ui.note(cn('无法卸载'), 'error')
            pass

    def _uninstall_all_extend(s):
        if len(s.lb) == 0 : 
            return None
        if ui.query(cn('卸载所有插件？'), 'query') : 
            new_extend_list = []
            for m in s.extend_list:
                try :
                    os.remove(s.dir + en(m))
                    try :
                        os.remove(s.help_dir + en(os.path.splitext(m)[0]) + '.txt')
                    except :
                        pass
                except :
                    ui.note((cn("无法卸载\n'%s'") % m), 'error')
                    new_extend_list.append(m)
            del s.extend_list[:]
            s.extend_list.extend(new_extend_list)
            del s.lb[:]
            s.lb.extend([ui.Item(x) for x in s.extend_list])

    def manager(s, back_callback):
        s.lb = ui.Listbox2([])
        s.extend_list = [cn(x) for x in os.listdir(s.dir)]
        s.lb.extend([ui.Item(x) for x in s.extend_list])
        ui.app.body = s.lb
        ui.app.title = cn('拓展插件')
        ui.app.body.bind(8, s._uninstall_extend)
        def read_detail():
            if len(s.lb) == 0 : 
                return None
            e32.ao_yield()
            import globalui
            globalui.global_msg_query(s.read_info(os.path.splitext(s.extend_list[s.lb.current()])[0] + '.txt'), s.extend_list[s.lb.current()])

        ui.app.body.bind(63557, read_detail)
        ui.app.exit_key_handler = back_callback
        ui.app.menu = [(cn('详情'), read_detail), (cn('安装插件'), s._install_extend), (cn('卸载插件'), s._uninstall_extend), (cn('全部卸载'), s._uninstall_all_extend)]

import cfileman
CMan = cfileman.FileMan()
clistdir = lambda path : CMan.listdir(cn(path), cfileman.EAttMatchMask, cfileman.ESortByName)

class File_Manager(object, ) :

    def __init__(s, icons_path=None):
        s.lock = e32.Ao_lock()
        if icons_path:
            s.icon=1
            s.icons_path = cn(icons_path)
            s.disk_icon = ui.Icon(s.icons_path, 0, 1)
            s.dir_icon = ui.Icon(s.icons_path, 2, 3)
            s.file_icon = ui.Icon(s.icons_path, 4, 5)
            s.zip_icon = ui.Icon(s.icons_path, 6, 7)
            s.lb = ui.Listbox2(icons = True, markable = True)
        else:
            s.icon=0
            s.icons_path = None
            s.disk_icon = None
            s.dir_icon = None
            s.file_icon = None
            s.zip_icon = None
            s.lb = ui.Listbox2(icons = False, markable = True)

    def prepare(s):
        s.old_body = ui.app.body
        if s.body_process : 
            ui.app.body = None
        s.paths_list = []
        s.multi = False
        s.history_read_only = False
        s.waiting = True
        s.loop = 0
        s.old_exit_key = ui.app.exit_key_handler
        s.old_menu = ui.app.menu
        s.old_title = ui.app.title
        s.old_screen = ui.app.screen
        s.old_focus = ui.app.focus
        if ui.app.screen != 'normal' : 
            ui.app.screen = 'normal'
        ui.app.title = u''
        ui.app.focus = None
        try :
            s.lb.set_current(0)
        except :
            pass
        s.lb.clear()
        s.lb.bind(EKeySelect, s.forward)
        s.lb.bind(EKeyLeftArrow, s.backward)
        s.lb.bind(EKeyRightArrow, s.forward)
        s.lb.bind(EKeyStar, s.last_page)
        s.lb.bind(EKeyHash, s.next_page)
        try :
            s.lb.bind(EKey1, s.detail)
            s.lb.bind(EKey2, s._mark_all)
            s.lb.bind(EKey3, s._clear_mark)
            s.lb.bind(EKey4, s.makedir)
            s.lb.bind(EKey5, s._mark)
            s.lb.bind(EKey6, program.shell)
            s.lb.bind(EKey7, s.rename)
            s.lb.bind(EKey8, s.filter_ext)
            s.lb.bind(EKey9, s.run)
            s.lb.bind(EKey0, s.filter)
        except :
            pass
        try :
            s.lb.bind(8, s.delete)
        except :
            pass
        ui.app.exit_key_handler = s.exit_key

    def _prepare_quit(s):
        ui.app.exit_key_handler = s.old_exit_key
        ui.app.menu = s.old_menu

    def last_page(s):
        s.lb.page_up()

    def next_page(s):
        s.lb.page_down()


    def _find(s, path):
        s.menu()
        s.last_current = 0
        if path == '' : 
            try :
                s.last_current = s.root.index(s.last_path[ : -1])
            except :
                pass
            s.last_path = path
            return s.root_list
        list = []
        if s.mode == 'dir' : 
            try :
                listdir = clistdir(path)
            except :
                listdir = []
            for i in listdir[0]:
                    list.append(ui.Item(i, icon = s.dir_icon))
            pass
        else : 
            try :
                listdir = clistdir(path)
            except :
                listdir = []
            for i in listdir[0]:
                list.append(ui.Item(i, icon = s.dir_icon, marked = 0))
            for i in listdir[1]:
                if s.ext == [] or os.path.splitext(i)[-1].lower() in s.ext : 
                    if i.endswith('.zip') : 
                        list.append(ui.Item(i, icon = s.zip_icon, marked = 0))
                    else : 
                        list.append(ui.Item(i, icon = s.file_icon, marked = 0))
                    pass
            pass
        try :
            if len(s.last_path.split('\\')) >= 2 : 
                for i in list:
                    if i.__dict__['title'] == cn(s.last_path.split('\\')[-2]) : 
                        s.last_current = list.index(i)
                pass
        except :
            s.last_current = 0
        s.last_path = path
        return list

    def filter_ext(s):
        if s.mode != 'file' or s.path == '历史文件\\' : 
            return None
        ask = ui.popup_menu([cn('添加'), cn('删除'), cn('清空')], cn('后缀限制'))
        if ask == 0 : 
            ask_ext = ui.query(cn("添加后缀(无需加'.')"), 'text')
            if ask_ext is not None : 
                s.ext.append('.' + en(ask_ext))
                s.lb.set_list(s._find(s.path), 0)
            pass
        elif ask == 1 : 
            if s.ext == [] : 
                ui.note(cn('未设定限制'))
                return None
            ask_del = ui.popup_menu([cn(i) for i in s.ext], cn('删除后缀'))
            if ask_del is not None : 
                del s.ext[ask_del]
                s.lb.set_list(s._find(s.path), 0)
            pass
        elif ask == 2 : 
            if ui.query(cn('清空后缀限制？'), 'query') : 
                del s.ext[:]
                s.lb.set_list(s._find(s.path), 0)
            pass

    def _mark(s):
        if  not (s.mode == 'dir' or s.path == '' or s.multi) : 
            return None
        current = s.lb.current()
        if  s.path != '历史文件\\' and not(os.path.isfile(s.path + en(s.lb[current].__dict__['title']))) : 
            return None
        try :
            if s.lb[current].__dict__['marked'] == 0 : 
                s.lb[current].__dict__['marked'] = 1
            else : 
                s.lb[current].__dict__['marked'] = 0
        except KeyError : 
            s.lb[current].__dict__['marked'] = 1
        s.lb[current] = s.lb[current]

    def _mark_all(s):
        if  not (s.mode == 'dir' or s.path == '' or s.multi) : 
            return None
        s.lb.begin_update()
        for i in range(len(s.lb)):
            if s.path == '历史文件\\' : 
                s.lb[i].__dict__['marked'] = 1
                s.lb[i] = s.lb[i]
            elif os.path.isfile(s.path + en(s.lb[i].__dict__['title'])) : 
                s.lb[i].__dict__['marked'] = 1
                s.lb[i] = s.lb[i]
        s.lb.end_update()

    def _clear_mark(s):
        if  not (s.mode == 'dir' or s.path == '' or s.multi) : 
            return None
        s.lb.begin_update()
        for i in range(len(s.lb)):
            s.lb[i].__dict__['marked'] = 0
            s.lb[i] = s.lb[i]
        s.lb.end_update()

    def _del(s, current):
        if current == (len(s.lb) - 1) and len(s.lb) != 1 : 
            s.lb.set_current((current - 1))
        del s.lb[current]

    def select(s, add = True, ask_multi = True):
        if len(s.lb) == 0 : 
            if  not (add) : 
                s.paths_list.append(s.path)
                s._prepare_quit()
                s.lock_signal()
            return None
        temp_path = s.path
        current = s.lb.current()
        if  s.path == '历史文件\\' and not(s.history_read_only) : 
            if s.lb.marked_items() == [] : 
                s.path = en(s.lb[current].__dict__['title'])
                s.paths_list.append(s.path)
                s._prepare_quit()
                s.lock_signal()
                return None
            elif not (ask_multi) : 
                s.paths_list.extend([en(i.__dict__['title']) for i in s.lb.marked_items()])
                s._prepare_quit()
                s.lock_signal()
                return None
            pass
        if  not (s.lb.marked_items() != [] and ask_multi) : 
            s.paths_list.extend([s.path + en(i.__dict__['title']) for i in s.lb.marked_items()])
            s._prepare_quit()
            s.lock_signal()
            return None
        if s.lb.marked_items() != [] : 
            if  s.path == '历史文件\\' or not(os.path.isdir(s.path + en(s.lb[current].__dict__['title']))) : 
                if s.path == '历史文件\\' and s.history_read_only : 
                    first_event = cn('删除')
                else : 
                    first_event = cn('打开')
                try :
                    if s.lb.current_item().__dict__['marked'] == 0 : 
                        ask = ui.popup_menu([first_event, cn('标记文件'), cn('全部标记'), cn('全部取消')], cn('标记'))
                    else : 
                        ask = ui.popup_menu([first_event, cn('取消标记'), cn('全部标记'), cn('全部取消')], cn('标记'))
                except KeyError : 
                    s.lb.current_item().__dict__['marked'] = 0
                    ask = ui.popup_menu([first_event, cn('标记文件'), cn('全部标记'), cn('全部取消')], cn('标记'))
                if ask == 0 : 
                    if s.path == '历史文件\\' : 
                        if  not (s.history_read_only) : 
                            s.paths_list.extend([en(i.__dict__['title']) for i in s.lb.marked_items()])
                        else : 
                            s.delete()
                        pass
                    else : 
                        s.paths_list.extend([s.path + en(i.__dict__['title']) for i in s.lb.marked_items()])
                    s._prepare_quit()
                    s.lock_signal()
                    return None
                elif ask == 1 : 
                    s._mark()
                elif ask == 2 : 
                    s._mark_all()
                elif ask == 3 : 
                    s._clear_mark()
                pass
            else : 
                ask = ui.popup_menu([cn('打开'), cn('全部标记'), cn('全部取消')], cn('标记'))
                if ask == 0 : 
                    s.paths_list.extend([s.path + en(i.__dict__['title']) for i in s.lb.marked_items()])
                    s._prepare_quit()
                    s.lock_signal()
                    return None
                elif ask == 1 : 
                    s._mark_all()
                elif ask == 2 : 
                    s._clear_mark()
                pass
            return None
        if add : 
            s.path += en(s.lb[current].__dict__['title'])
        else : 
            s.paths_list.append(s.path)
            s._prepare_quit()
            s.lock_signal()
            return None
        if s.path == '历史文件' : 
            s.path += '\\'
            s.history_manager()
            return None
        elif  not (os.path.exists(s.path)) : 
            s.path = temp_path
            ui.note(cn('路径不存在'), 'error')
            s._del(current)
            return None
        elif s.mode == 'dir' and os.path.isfile(s.path) : 
            ui.note(cn('路径已过时。/n正在刷新...'), 'info')
            s.path = temp_path
            s.lb.set_list(s._find(s.path), 0)
        if s.mode == 'file' and os.path.isfile(s.path) : 
            s.paths_list.append(s.path)
            s._prepare_quit()
            s.lock_signal()
            return None
        else : 
            if  not (s.path.endswith('\\')) : 
                s.path += '\\'
            if s.mode == 'dir' : 
                s.paths_list.append(s.path)
                s._prepare_quit()
                s.lock_signal()
                return None
            pass
        ui.app.title = cn(s.path)

    def forward(s):
        if s.history_read_only : 
            s.select()
            return None
        if len(s.lb) == 0 : 
            return None
        temp_path = s.path
        current = s.lb.current()
        if s.path == '历史文件\\' : 
            if s.lb.marked_items() == [] : 
                s.path = en(s.lb[current].__dict__['title'])
                s.paths_list.append(s.path)
                s._prepare_quit()
                s.lock_signal()
                return None
            pass
        if s.lb.marked_items() != [] : 
            s.select()
            return None
        s.path += en(s.lb[current].__dict__['title'])
        if s.path == '历史文件' : 
            s.path += '\\'
            s.history_manager()
            return None
        elif  not (os.path.exists(s.path)) : 
            s.path = temp_path
            ui.note(cn('路径不存在'), 'error')
            s._del(current)
            return None
        elif s.mode == 'dir' and os.path.isfile(s.path) : 
            ui.note(cn('路径已过时。/n正在刷新...'), 'info')
            s.path = temp_path
            s.lb.set_list(s._find(s.path), 0)
        elif s.mode == 'file' and os.path.isfile(s.path) : 
            s.paths_list.append(s.path)
            s._prepare_quit()
            s.lock_signal()
            return None
        if  not (s.path.endswith('\\')) : 
            s.path += '\\'
        s.lb.set_list(s._find(s.path), 0)
        ui.app.title = cn(s.path)

    def backward(s):
        if s.history_read_only : 
            s.quit()
            return None
        s.menu()
        if s.path == '' : 
            return None
        elif s.path[ : -1] in s.root : 
            if s.path == '历史文件\\' : 
                history._update()
            s.path = ''
            s.lb.set_list(s._find(s.path), s.last_current, 0)
            ui.app.title = cn(s.path)
        else : 
            s.path = '\\'.join(s.path.split('\\')[ : -2]) + '\\'
            s.lb.set_list(s._find(s.path), s.last_current)
            ui.app.title = cn(s.path)

    def exit_key(s):
        if s.path == '' : 
            s.quit()
        else : 
            s.backward()

    def delete(s):
        if len(s.lb) == 0 : 
            return None
        if s.path == '历史文件\\' : 
            if history.list == [] : 
                return None
            if s.lb.marked_items() == [] : 
                index = s.lb.current()
                item = history.list[index]
                ask = ui.popup_menu([cn('仅删除记录'), cn('同时删除原文件')], item)
                if ask is not None : 
                    if ask == 1 and os.path.isfile(en(item)) : 
                        try :
                            os.remove(en(item))
                        except :
                            ui.note((cn('无法删除\n%s') % item), 'error')
                            return None
                        pass
                    del history.list[index]
                    if index == (len(s.lb) - 1) and index != 0 : 
                        s.lb.set_current((index - 1))
                    del s.lb[index]
                pass
            else : 
                ask = ui.popup_menu([cn('仅删除记录'), cn('同时删除原文件')], (cn('%d个标记') % len(s.lb.marked_items())))
                if ask is None : 
                    return None
                current = s.lb.current()
                for i in s.lb.marked_items():
                    try :
                        if ask == 1 : 
                            os.remove(en(i.__dict__['title']))
                        history.list.remove(en(i.__dict__['title']))
                    except :
                        ui.note((cn('无法删除\n%s') % i.__dict__['title']), 'error')
                        break
                s.lb.set_list([ui.Item(i, icon = s.file_icon) for i in history.get_list()])
                if current >= len(s.lb) and len(s.lb) != 0 : 
                    s.lb.set_current((len(s.lb) - 1))
                history._update()
            return None
        path = s.path + en(s.lb[s.lb.current()].__dict__['title'])
        if path == '历史文件' : 
            ask = ui.popup_menu([cn('仅清空记录'), cn('同时删除原文件')], cn('历史记录'))
            if ask is not None : 
                if ask == 1 : 
                    for f in history.list:
                        if os.path.isfile(en(f)) : 
                            try :
                                os.remove(en(f))
                            except :
                                ui.note((cn('无法删除\n%s') % f), 'error')
                                return None
                            pass
                    pass
                del history.list[:]
                history._update()
            return None
        elif s.lb.current_item() in s.root_list : 
            return None
        if s.lb.marked_items() != [] : 
            if ui.query((cn('删除%s个标记文件？') % len(s.lb.marked_items())), 'query') : 
                current = s.lb.current()
                for i in s.lb.marked_items():
                    try :
                        os.remove(s.path + en(i.__dict__['title']))
                    except :
                        ui.note((cn('无法删除\n%s') % i.__dict__['title']), 'error')
                        break
                s.lb.set_list(s._find(s.path))
                if current > (len(s.lb) - 1) and len(s.lb) != 0 : 
                    s.lb.set_current((len(s.lb) - 1))
                pass
            pass
        elif ui.query((cn('删除\n%s') % s.lb[s.lb.current()].__dict__['title']), 'query') : 
            try :
                if os.path.isfile(path) : 
                    os.remove(path)
                elif os.listdir(path) == [] : 
                    os.rmdir(path)
                else : 
                    ui.note((cn("无法删除，\n'%s'不为空文件夹") % s.lb[s.lb.current()].__dict__['title']), 'error')
                    return None
            except :
                ui.note((cn('无法删除\n%s') % s.lb[s.lb.current()].__dict__['title']), 'error')
                return None
            s._del(s.lb.current())

    def filter(s):
        if s.path == '' : 
            return None
        ask = ui.query(cn('过滤内容'), 'text')
        if ask is None : 
            return None
        s.lb.set_list([x for x in s.lb if x.__dict__['title'].lower().find(ask.lower()) >= 0 ], 0)

    def run(s):
        if s.path == '历史文件\\' : 
            program.run_script(path = en(s.lb.current_item().__dict__['title']))
        elif os.path.isfile(s.path + en(s.lb.current_item().__dict__['title'])) : 
            program.run_script(path = s.path + en(s.lb.current_item().__dict__['title']))

    def makedir(s):
        if s.path == '' or s.path == '历史文件\\' : 
            return None
        ask = ui.query(cn('新建文件夹'), 'text')
        if ask is None : 
            return None
        try :
            os.makedirs(s.path + en(ask))
        except :
            ui.note(cn('无法新建文件夹'), 'error')
            return None
        if len(s.lb) != 0 : 
            s.lb.insert(0, ui.Item(ask, icon = s.dir_icon, marked = False))
            s.lb.set_current(0)
        else : 
            s.lb.extend([ui.Item(ask, icon = s.dir_icon, marked = False)])

    def rename(s):
        if s.path == '' or s.path == '历史文件\\' : 
            return None
        ask = ui.query(cn('重命名'), 'text', s.lb.current_item().__dict__['title'])
        if ask is None : 
            return None
        try :
            os.rename(s.path + en(s.lb.current_item().__dict__['title']), s.path + en(ask))
        except :
            ui.note(cn('无法重命名'), 'error')
            return None
        s.lb.current_item().__dict__['title'] = ask
        s.lb[s.lb.current()] = s.lb[s.lb.current()]

    def detail(s):
        if s.path == '历史文件\\' : 
            path = s.lb[s.lb.current()].__dict__['title']
        else : 
            path = cn(s.path) + s.lb[s.lb.current()].__dict__['title']
        is_dir = path == cn('历史文件') and True or os.path.isdir(en(path))
        if  is_dir and path != cn('历史文件') and not(path.endswith(u'\\')) : 
            path += u'\\'
        try :
            import globalui
            e32.ao_yield()
            if is_dir : 
                globalui.global_msg_query((cn('路径: %s') % path), cn('文件夹详情'))
            else : 
                globalui.global_msg_query(u'\n'.join([(cn('路径: %s') % path), (cn('大小: %s') % program.get_file_size(en(path)))]), cn('文件详情'))
        except ImportError : 
            ui.note(path, 'info')

    def return_ui(s):
        ui.app.title = cn('请稍候...')
        e32.ao_yield()
        ui.app.body = s.old_body
        if s.old_screen != 'normal' : 
            ui.app.screen = s.old_screen
        ui.app.title = s.old_title
        ui.app.focus = s.old_focus

    def quit(s):
        s._clear_mark()
        s._prepare_quit()
        s.path = None
        s.lock_signal()

    def lock_signal(s):
        if s.auto_return_ui : 
            s.return_ui()
        if e32.s60_version_info >= (3, 0) and s.loop!=1: 
            s.lock.signal()
        else : 
            s.waiting = False

    def menu(s):
        if s.mode == 'dir' : 
            menu = [(cn('打开'), s.forward), (cn('详情[1]'), s.detail), (cn('上页[*]'), s.last_page), (cn('下页[#]'), s.next_page), (cn('退出'), s.quit)]
            if s.path != '' : 
                menu.insert(0, (cn('当前'), lambda  :  s.select(add = False) ))
                menu.insert(2, (cn('文件'), ((cn('重命名[7]'), s.rename), (cn('删除[C]'), s.delete), (cn('新建文件夹[4]'), s.makedir), (cn('解释器[6]'), program.shell))))
                menu.insert(3, (cn('过滤[0]'), s.filter))
            pass
        else : 
            menu = [(cn('打开'), lambda  :  s.select(ask_multi = False) ), (cn('详情[1]'), s.detail), (cn('上页[*]'), s.last_page), (cn('下页[#]'), s.next_page), (cn('退出'), s.quit)]
            if s.path != '' : 
                menu.insert(1, (cn('文件'), ((cn('运行[9]'), s.run), (cn('重命名[7]'), s.rename), (cn('删除[C]'), s.delete), (cn('新建文件夹[4]'), s.makedir), (cn('后缀限制[8]'), s.filter_ext), (cn('解释器[6]'), program.shell))))
                menu.insert(2, (cn('过滤[0]'), s.filter))
                if s.multi : 
                    menu.insert(2, (cn('标记'), ((cn('标记文件[5]'), s._mark), (cn('标记全部[2]'), s._mark_all), (cn('全部取消[3]'), s._clear_mark))))
                pass
            pass
        ui.app.menu = menu

    def history_manager(s):
        s.lb.set_list([ui.Item(i, icon = s.file_icon) for i in history.get_list()], 0)
        if ui.app.body != s.lb : 
            ui.app.body = s.lb
        ui.app.title = cn('历史文件')
        def clear_history():
            ask = ui.popup_menu([cn('仅清空记录'), cn('同时删除原文件')], cn('清空'))
            if ask is not None : 
                if ask == 1 : 
                    for f in history.list:
                        if os.path.isfile(en(f)) : 
                            try :
                                os.remove(en(f))
                            except :
                                ui.note((cn('无法删除\n%s') % f), 'error')
                                return None
                            pass
                    pass
                del history.list[:]
                del s.lb[:]

        ui.app.menu = [(cn('文件'), ((cn('运行[9]'), s.run), (cn('删除[C]'), s.delete), (cn('清空'), clear_history), (cn('解释器[6]'), program.shell))), (cn('过滤[0]'), s.filter), (cn('详情[1]'), s.detail), (cn('上页[*]'), s.last_page), (cn('下页[#]'), s.next_page), (cn('退出'), s.backward)]
        if s.multi : 
            ui.app.menu.insert(1, (cn('标记'), ((cn('标记文件[5]'), s._mark), (cn('标记全部[2]'), s._mark_all), (cn('全部取消[3]'), s._clear_mark))))
        if  not (s.history_read_only) : 
            ui.app.menu.insert(0, (cn('打开'), lambda  :  s.select(ask_multi = False) ))
        else : 
            ui.app.exit_key_handler = s.quit

    def AskDir(s, path = '', disks = e32.drive_list(), dirs = [], auto_return_ui = True, body_process = False):
        s.mode = 'dir'
        s.auto_return_ui = auto_return_ui
        s.body_process = body_process
        s.prepare()
        s.root = [en(i) for i in disks]
        s.path = path
        s.root_list = [ui.Item(cn(i), icon = s.disk_icon, marked = 0) for i in s.root]
        s.root_list.extend([ui.Item(cn(i), icon = s.dir_icon, marked = 0) for i in dirs])
        if s.path != '' : 
            if  not (s.path.endswith('\\')) : 
                s.path += '\\'
            if  not (os.path.isdir(s.path)) : 
                s.path = ''
            pass
        if  not (os.path.isdir(s.path)) : 
            s.path = ''
        s.menu()
        s.lb.extend(s._find(s.path))
        ui.app.title = cn(s.path)
        ui.app.body = s.lb
        if e32.s60_version_info >= (3, 0) : 
            try:
                s.lock.wait()
            except:
                s.loop=1
                while s.waiting : 
                    e32.ao_yield()
                    e32.ao_sleep(0.1)
            pass
        else : 
            s.loop=1
            while s.waiting : 
                e32.ao_yield()
                e32.ao_sleep(0.1)
            pass
        return s.path

    def AskFile(s, path = '', ext = [], disks = e32.drive_list(), dirs = [], multi = True, auto_return_ui = True, history_read_only = False, body_process = True, able_history = True):
        s.mode = 'file'
        s.body_process = body_process
        s.prepare()
        s.auto_return_ui = auto_return_ui
        s.history_read_only = history_read_only
        if able_history : 
            s.root = ['历史文件']
            s.root_list = [ui.Item(cn(s.root[0]), icon = s.dir_icon)]
            s.root.extend([en(i) for i in disks])
            s.root_list.extend([ui.Item(cn(i), icon = s.disk_icon) for i in s.root[1 : ]])
        else : 
            s.root = [en(i) for i in disks]
            s.root_list = [ui.Item(cn(i), icon = s.disk_icon) for i in s.root]
        s.path = path
        s.ext = [x.lower() for x in ext]
        s.multi = multi
        s.root_list.extend([ui.Item(cn(i), icon = s.dir_icon) for i in dirs])
        if s.path != '' : 
            if  not (s.path.endswith('\\')) : 
                s.path += '\\'
            if  s.path != '历史文件\\' and not(os.path.isdir(s.path)) : 
                s.path = ''
            pass
        if s.path == '历史文件\\':
            s.history_manager()
        else : 
            s.menu()
            s.lb.extend(s._find(s.path))
            ui.app.body = s.lb
            ui.app.title = cn(s.path)
        if e32.s60_version_info >= (3, 0) : 
            try:
                s.lock.wait()
            except Exception,con:
                s.loop=1
                while s.waiting : 
                    e32.ao_yield()
                    e32.ao_sleep(0.1)
        else : 
            s.loop=1
            while s.waiting : 
                e32.ao_yield()
                e32.ao_sleep(0.1)
            pass
        return s.paths_list


class File_Manager2(object, ) :

    def prepare(s):
        try :
            from keycapture import KeyCapturer as KeyCapturer
            s.select_capture = KeyCapturer(lambda p, :  s.select() )
            s.backward_capture = KeyCapturer(lambda p, :  s.backward() )
            s.next_page_capture = KeyCapturer(lambda p, :  s.next_page() )
            s.last_page_capture = KeyCapturer(lambda p, :  s.last_page() )
            s.select_capture.keys = (EKeyRightArrow, )
            s.backward_capture.keys = (EKeyLeftArrow, )
            s.next_page_capture.keys = (EKeyHash, )
            s.last_page_capture.keys = (EKeyStar, )
            s.capture_tuple = (s.select_capture, s.backward_capture, s.next_page_capture, s.last_page_capture)
        except :
            pass
        s.PM = ui.popup_menu

    def start_capture(s):
        try :
            map(lambda x, : x.start() , s.capture_tuple)
        except :
            pass
        ui.app.bind_mediakeys(s.last_page, s.next_page, lambda : s.last_page(1), lambda : s.next_page(1))

    def stop_capture(s):
        try :
            map(lambda x, : x.stop() , s.capture_tuple)
        except :
            pass
        ui.app.bind_mediakeys(program.last_page, program.next_page)

    def return_ui(s):
        pass

    def select(s):
        if s.list == [] : 
            return None
        else : 
            try :
                import keypress
                s.direction = 0
                keypress.simulate_key(EKeySelect, EKeySelect)
            except :
                pass
            pass

    def backward(s):
        if s.list == s.disks : 
            return None
        else : 
            try :
                import keypress
                s.direction = -1
                keypress.simulate_key(EKeySelect, EKeySelect)
            except :
                pass
            pass

    def next_page(s, i=6):
        try :
            import keypress
            map(lambda x, :  keypress.simulate_key(EKeyDownArrow, EKeyDownArrow) , range(i))
        except :
            pass

    def last_page(s, i=6):
        try :
            import keypress
            map(lambda x, :  keypress.simulate_key(EKeyUpArrow, EKeyUpArrow) , range(i))
        except :
            pass

    def focus(s, fg):
        if s.path != '历史文件\\' : 
            if fg : 
                s.prepare()
                s.start_capture()
            else : 
                s.stop_capture()
            pass
        elif fg : 
            s.prepare()
            s.stop_capture()

    def history_manager(s):
        history_list = [h for h in history.list if os.path.isfile(en(h)) ]
        list = [(u'%s(%s)' % (os.path.basename(i), os.path.dirname(i))) for i in history_list]
        if history_list == [] : 
            ui.note(cn('无历史记录'))
            return None
        ask = ui.popup_menu(list, cn('历史文件'))
        if ask is None : 
            return None
        else : 
            return history_list[ask]

    def AskDir(s, path = '', title = '选择目录'.decode('u8'), disks = e32.drive_list(), dirs = [], auto_return_ui = False, body_process = False):
        s.prepare()
        s.title = title
        s.disks = e32.drive_list()
        s.disks.extend([cn(i[0].upper() + i[1 : ]) for i in dirs])
        s.path = path
        if len(s.path) > 0 : 
            if  not (s.path.endswith('\\')) : 
                s.path += '\\'
            s.path = s.path[0].upper() + s.path[1 : ]
        if  not (os.path.isdir(s.path)) : 
            s.path = ''
        s.direction = 1
        s.old_focus = ui.app.focus
        ui.app.focus = s.focus
        s.start_capture()
        while True : 
            if s.path == '' : 
                s.find = s.disks
                s.list = s.disks
                s.choose = s.PM(s.list, s.title)
            else : 
                try :
                    s.find = clistdir(s.path)[0]
                except OSError : 
                        s.find = []
                s.list = [(u'[%s]' % i) for i in s.find]
                s.list.insert(0, (cn('/%s/') % cn(s.path.split('\\')[-2])))
                s.choose = s.PM(s.list, s.title)
                if s.choose is not None : 
                    s.choose -= 1
                pass
            if s.choose is None : 
                if  not (s.path == '') : 
                    s.direction = -1
                else : 
                    s.stop_capture()
                    ui.app.focus = s.old_focus
                    return None
                pass
            if s.choose == -1 and s.direction != -1 : 
                s.stop_capture()
                ui.app.focus = s.old_focus
                return s.path
            elif s.direction == 1 : 
                s.path += en(s.find[s.choose])
                if  not (s.path.endswith('\\')) : 
                    s.path += '\\'
                pass
            elif s.direction == 0 : 
                s.path += en(s.find[s.choose])
                if  not (s.path.endswith('\\')) : 
                    s.path += '\\'
                s.stop_capture()
                ui.app.focus = s.old_focus
                return s.path
            elif s.direction == -1 : 
                if s.path[ : -1] in s.disks : 
                    s.path = ''
                else : 
                    for i in range((len(s.path) - 2), -1, -1):
                        if s.path[i] == '\\' : 
                            s.path = s.path[ : (i + 1)]
                            break
                    pass
                pass
            s.direction = 1

    def AskFile(s, path = '', title = '选择文件'.decode('u8'), disks = e32.drive_list(), ext = [], dirs = [], auto_return_ui = False, body_process = False, history_read_only = False, multi = False, able_history = True):
        if multi:
            return s.AskFiles(path = path, title = title, disks = disks, dirs = dirs, auto_return_ui = auto_return_ui, body_process = body_process)
        s.prepare()
        s.title = title
        s.disks = e32.drive_list()
        s.disks.extend([cn(i[0].upper() + i[1 : ]) for i in dirs])
        s.history_read_only = history_read_only
        if able_history : 
            s.disks.insert(0, cn('历史文件'))
        s.path = path
        if s.path != '历史文件\\' : 
            if len(s.path) > 0 : 
                if  not (s.path.endswith('\\')) : 
                    s.path += '\\'
                s.path = path[0].upper() + path[1 : ]
            if  not (os.path.isdir(s.path)) : 
                s.path = ''
            pass
        s.ext = [x.lower() for x in ext]
        s.direction = 1
        s.old_focus = ui.app.focus
        ui.app.focus = s.focus
        s.start_capture()
        e32.ao_sleep(0.1)
        while True : 
            if s.path == '' : 
                s.find = s.find_dir = s.disks
                s.find_file = []
                s.list = s.find_dir
            elif s.path == '历史文件\\' : 
                ask_history = s.history_manager()
                if ask_history is None : 
                    s.path = ''
                    continue
                else : 
                    s.stop_capture()
                    ui.app.focus = s.old_focus
                    return [en(ask_history)]
                pass
            else : 
                s.find_dir, s.find_file=clistdir(s.path)
                if ext != []:
                    s.find_file = [x for x in  s.find_file if os.path.splitext(en(x))[-1].lower() in ext]
                s.find = list(s.find_dir) + list(s.find_file)
                s.list = [(u'[%s]' % i) for i in s.find_dir]
                s.list.extend(s.find_file)
            if s.list == [] : 
                import globalui
                s.stop_capture()
                globalui.global_msg_query(cn('无内容'), s.title)
                s.start_capture()
                s.choose = None
                s.direction = -1
            else : 
                s.choose = s.PM(s.list, s.title)
            if s.choose is None : 
                if s.path != '' : 
                    s.direction = -1
                else : 
                    s.stop_capture()
                    ui.app.focus = s.old_focus
                    return []
                pass
            if s.direction == 0 or s.direction == 1 : 
                s.path += en(s.find[s.choose])
                if s.find[s.choose] in s.find_file : 
                    s.stop_capture()
                    ui.app.focus = s.old_focus
                    return [s.path]
                else : 
                    if  not (s.path.endswith('\\')) : 
                        s.path += '\\'
                    s.direction = 1
                    continue
                pass
            elif s.direction == -1 : 
                if cn(s.path[ : -1]) in s.disks : 
                    s.path = ''
                else : 
                    for i in range((len(s.path) - 2), -1, -1):
                        if s.path[i] == '\\' : 
                            s.path = s.path[ : (i + 1)]
                            break
                    pass
                s.direction = 1

    def AskFiles(s, path = '', title = '选择文件所在文件夹'.decode('u8'), disks = e32.drive_list(), ext = [], dirs = [], auto_return_ui = False, body_process = False, history_read_only = False, able_history = True):
        while True:
            dir=s.AskDir(path = path, title = title, disks = disks, dirs = dirs, auto_return_ui = auto_return_ui, body_process = body_process)
            if dir==None:return None
            path = dir
            files=list(clistdir(path)[1])
            if ext != []:
                files = [x for x in files if os.path.splitext(en(x))[-1].lower() in ext]
            indexs = ui.multi_selection_list(files)
            if indexs == ():
                continue
            else:
                return [dir+en(files[x]) for x in indexs]


class File_Manager3(object,):

    def __init__(s):
        import fy_manager
        s.Mana=fy_manager.Manager
        s.man=s.Mana()

    def return_ui(s):
        pass

    def AskDir(s, path = '', disks = e32.drive_list(), dirs = [], auto_return_ui = True, body_process = False):
        s.Mana.workdir=[cn(x) for x in dirs]
        ui.app.bind_mediakeys(s.man.up_page, s.man.down_page)
        path=s.man.AskUser(path=path, find='dir')
        ui.app.bind_mediakeys(program.last_page, program.next_page)
        if path!=None:
            return en(path)
        else:
            return None
        
    def AskFile(s, path = '', ext = [], disks = e32.drive_list(), dirs = [], multi = True, auto_return_ui = True, history_read_only = False, body_process = True, able_history = True):
        if path.startswith("历史"):
            path=""
            his_list=history.get_list()
            s.Mana.max_recents=len(his_list)
            s.Mana.recents=his_list
            s.Mana.workdir=[cn(x)[:-1] for x in dirs]
            ui.app.bind_mediakeys(s.man.up_page, s.man.down_page)
            path=s.man.AskUser(path=path, find='file', ext=ext, mark=False)
            ui.app.bind_mediakeys(program.last_page, program.next_page)
            if path!=None:
                return [en(path)]
            else:
                return []
        else:
            s.Mana.workdir=[cn(x)[:-1] for x in dirs]
            ui.app.bind_mediakeys(s.man.up_page, s.man.down_page)
            path=s.man.AskUser(path=path, find='file', ext=ext, mark=multi)
            ui.app.bind_mediakeys(program.last_page, program.next_page)
            if path!=None:
                return map(en, path)
            else:
                return []


class Read_Funcs(object, ) :

    def prepare(s):
        try :
            from keycapture import KeyCapturer
            s.next_page_capture = KeyCapturer(lambda p, :  s.next_page() )
            s.last_page_capture = KeyCapturer(lambda p, :  s.last_page() )
            s.next_page_capture.keys = (EKeyHash, )
            s.last_page_capture.keys = (EKeyStar, )
            s.capture_tuple = (s.next_page_capture, s.last_page_capture)
        except :
            pass

    def start_capture(s):
        try :
            map(lambda x, : x.start() , s.capture_tuple)
        except :
            pass

    def stop_capture(s):
        try :
            map(lambda x, : x.stop() , s.capture_tuple)
        except :
            pass

    def next_page(s, i=6):
        try :
            import keypress
            map(lambda x, :  keypress.simulate_key(EKeyDownArrow, EKeyDownArrow) , range(i))
        except :
            pass

    def last_page(s, i=6):
        try :
            import keypress
            map(lambda x, :  keypress.simulate_key(EKeyUpArrow, EKeyUpArrow) , range(i))
        except :
            pass

    def focus(s, fg):
        if fg : 
            s.prepare()
            s.start_capture()
        else : 
            s.stop_capture()

    def read_funcs(s):
        s.get = ui.app.body.get()
        history = [(0, len(s.get))]
        func_path = []
        s.pos_start, s.pos_end = history[-1]
        funcs_dict = s._find()
        if funcs_dict == {} : 
            ui.note(cn('无内容'))
            return None
        poss_list = funcs_dict.keys()
        poss_list.sort()
        funcs_list = [funcs_dict[k] for k in poss_list]
        s.prepare()
        s.start_capture()
        old_focus = ui.app.focus
        ui.app.focus = s.focus
        while True : 
            if func_path == [] : 
                s.choose = ui.selection_list(funcs_list)
            else : 
                s.choose = ui.selection_list([func_path[-1][0]] + funcs_list)
                if s.choose == 0 : 
                    ui.app.body.set_pos(func_path[-1][1])
                    ui.app.focus = old_focus
                    s.stop_capture()
                    return None
                elif s.choose is not None : 
                    s.choose -= 1
                pass
            if s.choose is not None : 
                s.pos_start = poss_list[s.choose] + len(funcs_list[s.choose])
                if (s.choose + 1) != len(poss_list) : 
                    s.pos_end = poss_list[(s.choose + 1)]
                history.append((s.pos_start, s.pos_end))
                func_path.append((u'/' + funcs_list[s.choose] + u'/', poss_list[s.choose]))
            else : 
                history.pop()
                if history == [] : 
                    ui.app.focus = old_focus
                    s.stop_capture()
                    return None
                func_path.pop()
                s.pos_start, s.pos_end = history[-1]
            funcs_dict = s._find()
            poss_list = funcs_dict.keys()
            poss_list.sort()
            funcs_list = [funcs_dict[k] for k in poss_list]

    def _find(s):
        text = s.get[s.pos_start : s.pos_end]
        if s.pos_start == 0 : 
            t_text = u'\u2029' + text
            find = [i for i in [t_text.find(u'\u2029def '), t_text.find(u'\u2029class ')] if i >= 0 ]
        else : 
            find = [i for i in [text.find(u'def '), text.find(u'class ')] if i >= 0 ]
        if find == [] : 
            return {}
        find.sort()
        find = find[0]
        blank = u''
        for i in range((find - 1), -1, -1):
            if text[i] == u' ' : 
                blank += u' '
            else : 
                break
        func_signal = [u'\u2029' + blank + u'class ', u'\u2029' + blank + u'def ']
        funcs_dict = {}
        if text.startswith(blank + u'def ') or text.startswith(blank + u'class ') : 
            funcs_dict[0] = text.split(u':')[0]
        for p in range(2):
            start = 0
            while True : 
                k = text[start : ].find(func_signal[p])
                if k >= 0 : 
                    funcs_dict[(s.pos_start + start + k + len(blank) + 1)] = (text[(start + k + len(blank) + 1) : ]).split(u':')[0]
                    start += k + len(func_signal[p])
                else : 
                    break
        return funcs_dict



def initialize():
    s60_version = e32.s60_version_info
    if s60_version > (3, 0) : 
        db['file_manager_mode'] = '2'
    elif s60_version < (3, 0) : 
        db['fast_fetch'] = 0

ao_lock = e32.Ao_lock()
disk = sys.argv[0][ : 2]
db = Database(disk + '\\System\\iPro7\\settings.ini')
if  not (os.path.isfile(disk + '\\System\\iPro7\\windows.bin')) : 
    windows_db = Database(disk + '\\System\\iPro7\\windows.bin')
    windows_db['contents'] = ['']
    windows_db['file_paths'] = ['']
    windows_db['poss'] = [0]
    windows_db['windows'] = [cn('新建文件')]
    windows_db['codes'] = [db['default_code']]
    windows_db['current_w'] = 0
    windows_db['last_file_path'] = ''
    windows_db['last_pos'] = 0
    windows_db['last_code'] = db['default_code']
else : 
    windows_db = Database(disk + '\\System\\iPro7\\windows.bin')
if os.path.isfile(disk + '\\System\\iPro7\\initialize') : 
    initialize()
    try :
        os.remove(disk + '\\System\\iPro7\\initialize')
    except :
        pass
    pass
del initialize
history = History(disk + '\\System\\iPro7\\history')
if db['file_manager_mode'] == '1' : 
    icon = disk + '\\System\\iPro7\\file_manager_icons.mbm'
    file_manager = File_Manager(icon)
elif db['file_manager_mode'] == '2' : 
    file_manager = File_Manager2()
elif db['file_manager_mode'] == '3' : 
    file_manager = File_Manager3()
mould = Mould(disk + '\\System\\iPro7\\Mould\\', disk + '\\System\\iPro7\\Mould_Pos\\')
extend_iPro7 = Extend_iPro7(disk + '\\System\\iPro7\\Extend\\', disk + '\\System\\iPro7\\Extend_Help\\')
program = Program()
if __name__ == '__main__' : 
    program.start()