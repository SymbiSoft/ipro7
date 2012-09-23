#######wap.wapele.cn#######
#######中文名好听########
#######decompile2########
import e32
import os
try :
    from _appuifw import *
except :
    from appuifw import *

import _appuifw2
version = '1.00.0'
version_info = tuple(version.split('.'))
def schedule(target, *args, **kwargs):
    e32.ao_sleep(0, lambda  :  target(*args, **kwargs) )


class Item(object, ) :

    __module__ = __name__
    def __init__(self, title, **kwargs):
        kwargs['title'] = title
        self.__dict__.update(kwargs)
        self._Item__observers = []


    def add_observer(self, observer):
        from weakref import ref
        if ref(observer) not in self._Item__observers : 
            self._Item__observers.append(ref(observer, self._Item__del_observer))


    def remove_observer(self, observer):
        from weakref import ref as ref
        self._Item__del_observer(ref(observer))


    def _Item__del_observer(self, ref):
        try :
            self._Item__observers.remove(ref)
        except ValueError : 
            pass


    def __getattribute__(self, name):
        if  not (name.startswith('_')) : 
            for obref in self._Item__observers:
                ob = obref()
                if hasattr(ob, 'handle_item_getattr') : 
                    ob.handle_item_getattr(self, name)
            pass
        return object.__getattribute__(self, name)


    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if  not (name.startswith('_')) : 
            for obref in self._Item__observers:
                ob = obref()
                if hasattr(ob, 'handle_item_setattr') : 
                    ob.handle_item_setattr(self, name)
            pass


    def __repr__(self):
        return ('%s(%s)' % (self.__class__.__name__, repr(self.title)))



class Listbox2(list, ) :

    __module__ = __name__
    def __init__(self, items = [], select_callback = None, double = False, icons = False, markable = False):
        if double : 
            if icons : 
                mode = 3
            else : 
                mode = 1
            pass
        elif icons : 
            mode = 2
        else : 
            mode = 0
        if markable : 
            flags = 16385
        else : 
            flags = 0
        self._Listbox2__update_level = 0
        self._Listbox2__update_mode = 0
        self._Listbox2__double = double
        self._Listbox2__icons = icons
        self._Listbox2__markable = markable
        list.__init__(self, items)
        self._uicontrolapi = _appuifw2.Listbox2_create(mode, flags, select_callback)
        for item in self:
            self._Listbox2__item_check(item)
            self._Listbox2__ui_insert(-1, item)
            item.add_observer(self)
        self._Listbox2__update_level = 0
        self._Listbox2__update_mode = 0


    def _Listbox2__ui_insert(self, pos, item):
        if self._Listbox2__double : 
            s = (u'%s\t%s' % (item.title, getattr(item, 'subtitle', u'')))
        else : 
            s = item.title
        if self._Listbox2__icons : 
            try :
                i = item.icon
            except AttributeError : 
                raise TypeError('this listbox requires icons')
            pass
        else : 
            i = None
        api = self._uicontrolapi
        self.begin_update()
        try :
            self._Listbox2__update_init(1)
            pos = _appuifw2.Listbox2_insert(api, pos, s, i)
            if self._Listbox2__markable : 
                for i in xrange(0, len(self)):
                    try :
                        _appuifw2.Listbox2_select(api, i, self[i].__dict__['marked'])
                    except KeyError : 
                        pass
                _appuifw2.Listbox2_select(api, pos, getattr(item, 'marked', False))
        finally :
            self.end_update()


    def _Listbox2__ui_delete(self, pos, count = 1, update = True):
        api = self._uicontrolapi
        if update : 
            self.begin_update()
        try :
            self._Listbox2__update_init(2)
            if self._Listbox2__markable : 
                for i in xrange(pos + count, len(self)):
                    _appuifw2.Listbox2_select(api, (i - count), _appuifw2.Listbox2_select(api, i))
                pass
            _appuifw2.Listbox2_delete(api, pos, count)
        finally :
            if update : 
                self.end_update()
            pass


    def _Listbox2__item_check(self, item):
        if  not (isinstance(item, Item)) : 
            raise TypeError('items must be Item class instances')


    def handle_item_getattr(self, item, name):
        try :
            pos = self.index(item)
        except ValueError : 
            return None
        if name == 'current' : 
            item.__dict__[name] = self.current() == pos
        elif name == 'marked' : 
            item.__dict__[name] = _appuifw2.Listbox2_select(self._uicontrolapi, pos)


    def handle_item_setattr(self, item, name):
        try :
            pos = self.index(item)
        except ValueError : 
            return None
        if name == 'current' : 
            if item.__dict__[name] : 
                self.set_current(pos)
            else : 
                item.__dict__[name] = self.current() == pos
            pass
        elif name == 'marked' : 
            self.begin_update()
            try :
                _appuifw2.Listbox2_select(self._uicontrolapi, pos, item.__dict__[name])
            finally :
                self.end_update()
            pass
        elif name in ('title', 'subtitle', 'icon') : 
            self.__setitem__(pos, item)


    def begin_update(self):
        self._Listbox2__update_level += 1


    def end_update(self):
        if self._Listbox2__update_level == 0 : 
            return None
        self._Listbox2__update_level -= 1
        if self._Listbox2__update_level == 0 : 
            self._Listbox2__update_process()
            self._Listbox2__update_mode = 0
            app.refresh()


    def _Listbox2__update_init(self, mode):
        if mode != self._Listbox2__update_mode : 
            self._Listbox2__update_process()
            self._Listbox2__update_mode = mode


    def _Listbox2__update_process(self):
        if self._Listbox2__update_mode == 1 : 
            _appuifw2.Listbox2_finish_insert(self._uicontrolapi)
        elif self._Listbox2__update_mode == 2 : 
            _appuifw2.Listbox2_finish_delete(self._uicontrolapi)


    def clear(self):
        del self[:]


    def append(self, item):
        self._Listbox2__item_check(item)
        self._Listbox2__ui_insert(-1, item)
        item.add_observer(self)
        list.append(self, item)


    def extend(self, lst, update = True):
        if update : 
            self.begin_update()
        try :
            for item in lst:
                self._Listbox2__item_check(item)
                self._Listbox2__ui_insert(-1, item)
                item.add_observer(self)
            list.extend(self, lst)
        finally :
            if update : 
                self.end_update()
            pass


    def set_list(self, lst, pos = None, visible = None):
        self.begin_update()
        try:
            _appuifw2.Listbox2_current(self._uicontrolapi, 0)
        except:
            pass
        del self[:]
        self.extend(lst, update = False)
        if pos is not None : 
            try :
                self.set_current(pos)
            except :
                pass
            pass
        if visible is not None : 
            try :
                self.make_visible(visible)
            except :
                pass
            pass
        self.end_update()


    def insert(self, pos, item):
        self._Listbox2__item_check(item)
        list.insert(self, pos, item)
        if pos < 0 : 
            pos = 0
        elif pos > len(self) : 
            pos = -1
        self._Listbox2__ui_insert(pos, item)
        item.add_observer(self)


    def remove(self, item):
        pos = list.index(self, item)
        list.remove(self, item)
        self._Listbox2__ui_delete(pos)
        item.remove_observer(self)


    def pop(self, pos = -1):
        item = list.pop(self, pos)
        if pos < 0 : 
            pos = (len(self) + pos + 1)
        elif pos >= len(self) : 
            pos = -1
        self._Listbox2__ui_delete(pos)
        item.remove_observer(self)
        return item


    def _Listbox2__defcmpfunc(item1, item2):
        s1 = (u'%s%s' % (item1.title, getattr(item1, 'text', u''))).lower()
        s2 = (u'%s%s' % (item2.title, getattr(item2, 'text', u''))).lower()
        return  - s1 < s2


    def sort(self, cmpfunc = _Listbox2__defcmpfunc):
        list.sort(self, cmpfunc)
        self.begin_update()
        try :
            self._Listbox2__ui_delete(0, len(self))
            for item in self:
                self._Listbox2__ui_insert(-1, item)
        finally :
            self.end_update()


    def reverse(self):
        list.reverse(self)
        self.begin_update()
        try :
            self._Listbox2__ui.delete(0, len(self))
            for item in self:
                self._Listbox2__ui_insert(-1, item)
        finally :
            self.end_update()


    def current(self):
        pos = _appuifw2.Listbox2_current(self._uicontrolapi)
        if pos is None : 
            raise IndexError('no item selected')
        return pos


    def set_current(self, pos):
        if pos < 0 : 
            pos += len(self)
        self.begin_update()
        try :
            _appuifw2.Listbox2_current(self._uicontrolapi, pos)
        finally :
            self.end_update()


    def current_item(self):
        return self[self.current()]

    def page_up(self):
        current = self.current()
        if current == 0 : 
            self.set_current(len(self)-1)
        elif current < 7 : 
            self.set_current(0)
        else : 
            self.set_current((current - 7))

    def page_down(self):
        current = self.current()
        if current == (len(self) - 1) : 
            self.set_current(0)
        elif current > (len(self) - 8) : 
            self.set_current((len(self) - 1))
        else : 
            self.set_current((current + 7))

    def top(self):
        if  not (len(self)) : 
            raise IndexError('list is empty')
        return _appuifw2.Listbox2_top(self._uicontrolapi)


    def set_top(self, pos):
        if pos < 0 : 
            pos += len(self)
        if  not (0 <= pos < len(self)) : 
            raise IndexError('index out of range')
        self.begin_update()
        try :
            _appuifw2.Listbox2_top(self._uicontrolapi, pos)
        finally :
            self.end_update()


    def top_item(self):
        return self[self.top()]


    def bottom(self):
        if  not (len(self)) : 
            raise IndexError('list is empty')
        return _appuifw2.Listbox2_bottom(self._uicontrolapi)


    def bottom_item(self):
        return self[self.bottom()]


    def make_visible(self, pos):
        if pos < 0 : 
            pos += len(self)
        if  not (0 <= pos < len(self)) : 
            raise IndexError('index out of range')
        self.begin_update()
        try :
            _appuifw2.Listbox2_make_visible(self._uicontrolapi, pos)
        finally :
            self.end_update()


    def bind(self, event_code, callback):
        _appuifw2.bind(self._uicontrolapi, event_code, callback)


    def marked(self):
        return _appuifw2.Listbox2_selection(self._uicontrolapi)


    def marked_items(self):
        return [self[x] for x in self.marked()]


    def clear_marked(self):
        _appuifw2.Listbox2_clear_selection(self._uicontrolapi)


    def empty_list_text(self):
        return _appuifw2.Listbox2_empty_text(self._uicontrolapi)


    def set_empty_list_text(self, text):
        self.begin_update()
        try :
            _appuifw2.Listbox2_empty_text(self._uicontrolapi, text)
        finally :
            self.end_update()

    if e32.s60_version_info >= (3, 0) : 

        def highlight_rect(self):
            return _appuifw2.Listbox2_highlight_rect(self._uicontrolapi)

        pass

    def __setitem__(self, pos, item):
        olditem = self[pos]
        self._Listbox2__item_check(item)
        list.__setitem__(self, pos, item)
        olditem.remove_observer(self)
        if pos < 0 : 
            pos = len(self) + pos
        self.begin_update()
        try :
            self._Listbox2__ui_delete(pos)
            self._Listbox2__ui_insert(pos, item)
        finally :
            self.end_update()
        item.add_observer(self)


    def __delitem__(self, pos):
        item = self[pos]
        list.__delitem__(self, pos)
        item.remove_observer(self)
        if pos < 0 : 
            pos = len(self) + pos
        self._Listbox2__ui_delete(pos)


    def __setslice__(self, i, j, items):
        olditems = self[i : j]
        list.__setslice__(self, i, j, items)
        for item in olditems:
            item.remove_observer(self)
        ln = len(self)
        i = min(ln, max(0, i))
        j = min(ln, max(i, j))
        self.begin_update()
        try :
            self._Listbox2__ui_delete(i, (j - i))
            for pos in xrange(i, i + len(items)):
                self._Listbox2__ui_insert(pos, self[pos])
        finally :
            self.end_update()


    def __delslice__(self, i, j):
        items = self[i : j]
        size = len(self)
        list.__delslice__(self, i, j)
        for item in items:
            item.remove_observer(self)
        i = min(size, max(0, i))
        j = min(size, max(i, j))
        self._Listbox2__ui_delete(i, (j - i))


    def __repr__(self):
        return ('<%s instance at 0x%08X; %d items>' % (self.__class__.__name__, id(self), len(self)))



class Listbox(object, ) :

    __module__ = __name__
    def __init__(self, items, select_callback = None):
        self._Listbox__set_items(items, just_check = True)
        self._uicontrolapi = _appuifw2.Listbox2_create(self._Listbox__mode, 0, select_callback)
        self._Listbox__set_items(items)


    def _Listbox__set_items(self, items, just_check = False):
        if  not (isinstance(items, list)) : 
            raise TypeError('argument 1 must be a list')
        if  not (items) : 
            raise ValueError('non-empty list expected')
        item = items[0]
        mode = 0
        if isinstance(item, tuple) : 
            if len(item) == 2 : 
                if isinstance(item[1], unicode) : 
                    mode = 1
                else : 
                    mode = 2
                pass
            elif len(item) == 3 : 
                mode = 3
            else : 
                raise ValueError('tuple must include 2 or 3 elements')
            pass
        if just_check : 
            self._Listbox__mode = mode
        else : 
            if mode != self._Listbox__mode : 
                raise ValueError('changing of listbox type not permitted')
            api = self._uicontrolapi
            _appuifw2.Listbox2_delete(api)
            if mode == 0 : 
                for item in items:
                    _appuifw2.Listbox2_insert(api, -1, item)
                pass
            elif mode == 1 : 
                for item in items:
                    _appuifw2.Listbox2_insert(api, -1, (u'%s\t%s' % (item[0], item[1])))
                pass
            elif mode == 2 : 
                for item in items:
                    _appuifw2.Listbox2_insert(api, -1, item[0], item[1])
                pass
            else : 
                for item in items:
                    _appuifw2.Listbox2_insert(api, -1, (u'%s\t%s' % (item[0], item[1])), item[2])
                pass
            _appuifw2.Listbox2_finish_insert(api)
            app.refresh()


    def bind(self, event_code, callback):
        _appuifw2.bind(self._uicontrolapi, event_code, callback)


    def current(self):
        return _appuifw2.Listbox2_current(self._uicontrolapi)


    def set_list(self, items, current = 0):
        app.begin_refresh()
        try:
            _appuifw2.Listbox2_current(self._uicontrolapi, 0)
        except:
            pass
        try :
            self._Listbox__set_items(items)
            current = min((len(items) - 1), max(0, current))
            _appuifw2.Listbox2_current(self._uicontrolapi, current)
        finally :
            app.end_refresh()



class Text(object, ) :

    __module__ = __name__
    def __init__(self, text = u'', move_callback = None, edit_callback = None, skinned = False, scrollbar = False, word_wrap = True, t9 = True, indicator = True, fixed_case = False, flags = 37128, editor_flags = 0, input_mode = None):
        if  not (word_wrap) : 
            flags |= 32
        self._uicontrolapi = _appuifw2.Text2_create(flags, scrollbar, skinned, move_callback, edit_callback)
        if input_mode is not None : 
            try :
                _appuifw2.Text2_set_input_mode(self._uicontrolapi, input_mode)
            except :
                pass
            pass
        if text : 
            self.set(text)
            self.set_pos(0)
        if  not (t9) : 
            editor_flags |= 2
        if  not (indicator) : 
            editor_flags |= 4
        if fixed_case : 
            editor_flags |= 1
        if editor_flags : 
            _appuifw2.Text2_set_editor_flags(self._uicontrolapi, editor_flags)


    def add(self, text):
        _appuifw2.Text2_add_text(self._uicontrolapi, text)


    def insert(self, pos, text):
        _appuifw2.Text2_insert_text(self._uicontrolapi, pos, text)


    def bind(self, event_code, callback):
        _appuifw2.bind(self._uicontrolapi, event_code, callback)


    def clear(self):
        _appuifw2.Text2_clear_text(self._uicontrolapi)


    def delete(self, pos = 0, length = -1):
        _appuifw2.Text2_delete_text(self._uicontrolapi, pos, length)


    def apply(self, pos = 0, length = -1):
        _appuifw2.Text2_apply(self._uicontrolapi, pos, length)


    def get_pos(self):
        return _appuifw2.Text2_get_pos(self._uicontrolapi)


    def set_pos(self, cursor_pos, select = False):
        _appuifw2.Text2_set_pos(self._uicontrolapi, cursor_pos, select)


    def len(self):
        return _appuifw2.Text2_text_length(self._uicontrolapi)


    def get(self, pos = 0, length = -1):
        return _appuifw2.Text2_get_text(self._uicontrolapi, pos, length)


    def set(self, text, fast = False):
        if fast and text!=u"":
            try :
                self.clear()
                try :
                    clipboard.backup()
                    clipboard.copy(text)
                    self.paste()
                finally :
                    clipboard.recover()
            except :
                self.clear()
                _appuifw2.Text2_set_text(self._uicontrolapi, text)
            pass
        else : 
            self.clear()
            _appuifw2.Text2_set_text(self._uicontrolapi, text)

    def page_up(self):
        self.move(EFPageUp)

    def page_down(self):
        self.move(EFPageDown)


    def __len__(self):
        return _appuifw2.Text2_text_length(self._uicontrolapi)


    def __getitem__(self, i):
        return _appuifw2.Text2_get_text(self._uicontrolapi, i, 1)


    def __setitem__(self, i, value):
        _appuifw2.Text2_delete_text(self._uicontrolapi, i, len(value))
        _appuifw2.Text2_insert_text(self._uicontrolapi, i, value)


    def __delitem__(self, i):
        _appuifw2.Text2_delete_text(self._uicontrolapi, i, 1)


    def __getslice__(self, i, j):
        ln = len(self)
        i = min(ln, max(0, i))
        j = min(ln, max(i, j))
        return _appuifw2.Text2_get_text(self._uicontrolapi, i, (j - i))


    def __setslice__(self, i, j, value):
        ln = len(self)
        i = min(ln, max(0, i))
        j = min(ln, max(i, j))
        _appuifw2.Text2_delete_text(self._uicontrolapi, i, (j - i))
        _appuifw2.Text2_insert_text(self._uicontrolapi, i, value)


    def __delslice__(self, i, j):
        ln = len(self)
        i = min(ln, max(0, i))
        j = min(ln, max(i, j))
        return _appuifw2.Text2_delete_text(self._uicontrolapi, i, (j - i))


    def get_selection(self):
        pos, anchor = _appuifw2.Text2_get_selection(self._uicontrolapi)
        i = min(pos, anchor)
        j = max(pos, anchor)
        return (pos, anchor, _appuifw2.Text2_get_text(self._uicontrolapi, i, (j - i)))


    def set_selection(self, pos, anchor):
        _appuifw2.Text2_set_selection(self._uicontrolapi, pos, anchor)


    def set_word_wrap(self, word_wrap):
        _appuifw2.Text2_set_word_wrap(self._uicontrolapi, word_wrap)


    def set_limit(self, limit):
        _appuifw2.Text2_set_limit(self._uicontrolapi, limit)


    def get_word_info(self, pos = -1):
        return _appuifw2.Text2_get_word_info(self._uicontrolapi, pos)


    def set_case(self, case):
        _appuifw2.Text2_set_case(self._uicontrolapi, case)


    def set_allowed_cases(self, cases):
        _appuifw2.Text2_set_allowed_cases(self._uicontrolapi, cases)


    def set_input_mode(self, mode):
        _appuifw2.Text2_set_input_mode(self._uicontrolapi, mode)


    def set_allowed_input_modes(self, modes):
        _appuifw2.Text2_set_allowed_input_modes(self._uicontrolapi, modes)


    def set_undo_buffer(self, pos = 0, length = -1):
        return _appuifw2.Text2_set_undo_buffer(self._uicontrolapi, pos, length)


    def move(self, direction, select = False):
        _appuifw2.Text2_move(self._uicontrolapi, direction, select)


    def move_display(self, direction):
        _appuifw2.Text2_move_display(self._uicontrolapi, direction)


    def xy2pos(self, coords):
        return _appuifw2.Text2_xy2pos(self._uicontrolapi, coords)


    def pos2xy(self, pos):
        return _appuifw2.Text2_pos2xy(self._uicontrolapi, pos)

    for name in ('color', 'focus', 'font', 'highlight_color', 'style', 'read_only', 'has_changed', 'allow_undo', 'indicator_text'):
        exec ('%s = property(lambda self: _appuifw2.Text2_get_%s(self._uicontrolapi),lambda self, value: _appuifw2.Text2_set_%s(self._uicontrolapi, value))' % (name, name, name))
    for name in ('clear', 'select_all', 'clear_selection', 'undo', 'clear_undo', 'can_undo', 'can_cut', 'cut', 'can_copy', 'copy', 'can_paste', 'paste'):
        exec ('%s = lambda self: _appuifw2.Text2_%s(self._uicontrolapi)' % (name, name))
    del name


EUpperCase = 1
ELowerCase = 2
ETextCase = 4
EAllCases = ((EUpperCase | ELowerCase) | ETextCase)
ENullInputMode = 0
ETextInputMode = 1
ENumericInputMode = 2
ESecretAlphaInputMode = 4
EKatakanaInputMode = 8
EFullWidthTextInputMode = 16
EFullWidthNumericInputMode = 32
EFullWidthKatakanaInputMode = 64
EHiraganaKanjiInputMode = 128
EHiraganaInputMode = 256
EHalfWidthTextInputMode = 512
EAllInputModes = ETextInputMode | ENumericInputMode | ESecretAlphaInputMode | EKatakanaInputMode | EFullWidthTextInputMode | EFullWidthNumericInputMode | EFullWidthKatakanaInputMode | EHiraganaKanjiInputMode | EHalfWidthTextInputMode
EFNoMovement = 0
EFLeft = 1
EFRight = 2
EFLineUp = 3
EFLineDown = 4
EFPageUp = 5
EFPageDown = 6
EFLineBeg = 7
EFLineEnd = 8
class Application(object, ) :
    __module__ = __name__
    from appuifw import app as _Application__app
    for name in dir(_Application__app):
        exec ('%s = _Application__app.%s' % (name, name))

    del name
    def __init__(self):
        if isinstance(app, self.__class__) : 
            raise TypeError(('%s already instantiated' % self.__class__.__name__))
        self._Application__tabs = ([], None)
        self._Application__tab_index = 0
        self._Application__menu = None
        self._Application__menu_id = 0
        self._Application__menu_key_handler = None
        self._Application__init_menu_handler = None
        self._Application__navi_text = u''
        self._Application__left_navi_arrow = False
        self._Application__right_navi_arrow = False
        self._Application__navi = None
        self._Application__menu_dyn_init_callback = _appuifw2.patch_menu_dyn_init_callback(self._Application__dyn_init_menu)
        self._Application__refresh_level = 0
        self._Application__refresh_pending = False
        self._Application__views = []
        self._mediakeys_listener = None
        self.mediakeys = False


    def begin_refresh(self):
        self._Application__refresh_level += 1


    def end_refresh(self):
        self._Application__refresh_level -= 1
        if self._Application__refresh_level <= 0 : 
            self._Application__refresh_level = 0
            if self._Application__refresh_pending : 
                _appuifw2.refresh()
                self._Application__refresh_pending = False
            pass


    def refresh(self):
        if self._Application__refresh_level == 0 : 
            _appuifw2.refresh()
        else : 
            self._Application__refresh_pending = True

    def bind_mediakeys(self, up = None, down = None, long_up = None, long_down = None):
        if not self.mediakeys or (up == None and down == None):
            return None
        if long_up == None :
            long_up = up
        if long_down == None :
            long_down = down
        def callback(k):
            if k == 21 : up()
            elif k == 1 : long_up()
            elif k == 22 : down()
            elif k == 3 : long_down()
        from mediakeys import New
        if self._mediakeys_listener != None:
            self._mediakeys_listener = None
        self._mediakeys_listener = New(callback)

    def set_tabs(self, tab_texts, callback):
        self._Application__app.set_tabs(tab_texts, callback)
        self._Application__tabs = (tab_texts, callback)
        self._Application__tab_index = 0


    def activate_tab(self, index):
        self._Application__app.activate_tab(index)
        self._Application__tab_index = index


    def _Application__get_body(self):
        return self._Application__app.body


    def _Application__set_body(self, value):
        self._Application__app.body = value


    def _Application__get_exit_key_handler(self):
        return self._Application__app.exit_key_handler


    def _Application__set_exit_key_handler(self, value):
        self._Application__app.exit_key_handler = value


    def _Application__get_menu(self):
        if id(self._Application__app.menu) != self._Application__menu_id : 
            return self._Application__app.menu
        return self._Application__menu


    def _Application__set_menu(self, value):
        self._Application__menu = value
        self._Application__update_menu()


    def _Application__dyn_init_menu(self):
        if self._Application__menu_key_handler is not None : 
            schedule(self._Application__menu_key_handler)
        if self._Application__init_menu_handler is not None : 
            self._Application__init_menu_handler()
        if id(self._Application__app.menu) == self._Application__menu_id : 
            self._Application__update_menu()


    def _Application__update_menu(self):
        if hasattr(self._Application__menu, 'as_fw_menu') : 
            self._Application__app.menu = self._Application__menu.as_fw_menu()
        elif self._Application__menu is None : 
            self._Application__app.menu = []
        else : 
            self._Application__app.menu = self._Application__menu
        self._Application__menu_id = id(self._Application__app.menu)


    def _Application__get_screen(self):
        return self._Application__app.screen


    def _Application__set_screen(self, value):
        self._Application__app.screen = value


    def _Application__get_title(self):
        return self._Application__app.title


    def _Application__set_title(self, value):
        self._Application__app.title = value


    def _Application__get_focus(self):
        return self._Application__app.focus


    def _Application__set_focus(self, value):
        self._Application__app.focus = value

    if e32.s60_version_info >= (3, 0) : 

        def _Application__get_orientation(self):
            return self._Application__app.orientation


        def _Application__set_orientation(self, value):
            self._Application__app.orientation = value

        pass

    def _Application__get_init_menu_handler(self):
        return self._Application__init_menu_handler


    def _Application__set_init_menu_handler(self, value):
        self._Application__init_menu_handler = value


    def _Application__get_menu_key_handler(self):
        return self._Application__menu_key_handler


    def _Application__set_menu_key_handler(self, value):
        self._Application__menu_key_handler = value


    def _Application__get_menu_key_text(self):
        return _appuifw2.command_text(3000)


    def _Application__set_menu_key_text(self, value):
        _appuifw2.command_text(3000, value)


    def _Application__get_exit_key_text(self):
        return _appuifw2.command_text(3009)


    def _Application__set_exit_key_text(self, value):
        _appuifw2.command_text(3009, value)


    def _Application__get_navi_text(self):
        return self._Application__navi_text


    def _Application__set_navi_text(self, value):
        self._Application__navi_text = value
        self._Application__set_navi()


    def _Application__get_left_navi_arrow(self):
        return self._Application__left_navi_arrow


    def _Application__set_left_navi_arrow(self, value):
        self._Application__left_navi_arrow = bool(value)
        self._Application__set_navi()


    def _Application__get_right_navi_arrow(self):
        return self._Application__right_navi_arrow


    def _Application__set_right_navi_arrow(self, value):
        self._Application__right_navi_arrow = bool(value)
        self._Application__set_navi()


    def _Application__set_navi(self):
        if self._Application__navi_text or self._Application__left_navi_arrow or self._Application__right_navi_arrow : 
            self._Application__navi = _appuifw2.set_navi(self._Application__navi_text, self._Application__left_navi_arrow, self._Application__right_navi_arrow)
        else : 
            self._Application__navi = None


    def _Application__get_view(self):
        try :
            return self._Application__views[-1]
        except IndexError : 
            return None


    def _Application__set_view(self, value):
        if  not (isinstance(value, View)) : 
            raise TypeError('expected a View object')
        if  not (self._Application__views) : 
            appview = View()
            for name in View.all_attributes:
                setattr(appview, name, getattr(self, name))
            appview.set_tabs(*self._Application__tabs)
            appview.activate_tab(self._Application__tab_index)
            try :
                self._Application__views.append(appview)
                appview.shown()
            except :
                del self._Application__views[0]
                raise 
            pass
        try :
            self._Application__views.append(value)
            self._Application__sync_view()
            self._Application__views[-2].hidden()
            value.shown()
        except :
            del self._Application__views[-1]
            if len(self._Application__views) == 1 : 
                del self._Application__views[0]
            raise 


    def _Application__pop_view(self, view = None):
        if view is None : 
            i = -1
        else : 
            try :
                i = self._Application__views.index(view)
            except ValueError : 
                return None
            pass
        curr = self.view
        try :
            self._Application__views.pop(i)
        except IndexError : 
            return None
        try :
            if self.view != curr : 
                self.view.shown()
                self._Application__sync_view()
                curr.hidden()
        finally :
            if len(self._Application__views) == 1 : 
                del self._Application__views[0]
            pass


    def _Application__sync_view(self):
        try :
            view = self._Application__views[-1]
        except IndexError : 
            return None
        for name in View.all_attributes:
            setattr(self, name, getattr(view, name))
        self.set_tabs(*view._View__tabs)
        self.activate_tab(view._View__tab_index)

    body = property(_Application__get_body, _Application__set_body)
    exit_key_handler = property(_Application__get_exit_key_handler, _Application__set_exit_key_handler)
    menu = property(_Application__get_menu, _Application__set_menu)
    screen = property(_Application__get_screen, _Application__set_screen)
    title = property(_Application__get_title, _Application__set_title)
    focus = property(_Application__get_focus, _Application__set_focus)
    if e32.s60_version_info >= (3, 0) : 
        orientation = property(_Application__get_orientation, _Application__set_orientation)
    init_menu_handler = property(_Application__get_init_menu_handler, _Application__set_init_menu_handler)
    menu_key_handler = property(_Application__get_menu_key_handler, _Application__set_menu_key_handler)
    menu_key_text = property(_Application__get_menu_key_text, _Application__set_menu_key_text)
    exit_key_text = property(_Application__get_exit_key_text, _Application__set_exit_key_text)
    navi_text = property(_Application__get_navi_text, _Application__set_navi_text)
    left_navi_arrow = property(_Application__get_left_navi_arrow, _Application__set_left_navi_arrow)
    right_navi_arrow = property(_Application__get_right_navi_arrow, _Application__set_right_navi_arrow)
    view = property(_Application__get_view, _Application__set_view)


app = Application()
class Clipboard(object, ) :

    __module__ = __name__
    def __init__(s):
        s.dir = 'd:\\System\\Data\\'
        s.backup_clipboard = ''
        s.head = '7\x00\x00\x10\x10:\x00\x10\x00\x00\x00\x00j\xfc{\x03'
        s.end = '\x00\x02\x1d:\x00\x10\x14\x00\x00\x00'


    def backup(s):
        if  not (os.path.isdir(s.dir)) : 
            try :
                os.makedirs(s.dir)
            except :
                return False
            pass
        if  not (os.path.isfile(s.dir + 'Clpboard.cbd')) : 
            try :
                (open(s.dir + 'Clpboard.cbd', 'w')).close()
            except :
                return False
            pass
        try :
            f = open(s.dir + 'Clpboard.cbd', 'rb')
            s.backup_clipboard = f.read()
            f.close()
        except :
            return False
        return True


    def recover(s):
        if  not (os.path.isdir(s.dir)) : 
            try :
                os.makedirs(s.dir)
            except :
                return False
            pass
        try :
            f = open(s.dir + 'Clpboard.cbd', 'wb')
            f.write(s.backup_clipboard)
            f.close()
        except :
            return False
        return True

    def copy(s, text):
        import struct
        if  not (os.path.isdir(s.dir)) : 
            os.makedirs(s.dir)
        f = open(s.dir + 'Clpboard.cbd', 'wb')
        f.write(s.head)
        f.write(struct.pack('l', (26 + (len(text) * 2))) + struct.pack('I', len(text)) + '\x0f')
        f.write(text.encode('utf_16_be').replace('\x00\n', ' )'))
        f.write(s.end)
        f.close()

clipboard = Clipboard()