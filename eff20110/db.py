import ui
import os
import e32
import marshal

zw = lambda x, : x.decode('u8') 
en = lambda y, : y.encode('u8') 


class Database(object, ) :

    __module__ = __name__
    def __init__(s, path):
        s.db_dict={}
        s._NULL = ''
        s._path = path
        if  not (os.path.isfile(s._path)) : 
            try :
                f = open(s._path, 'wb')
                marshal.dump(s._NULL, f)
                f.close()
            except :
                raise IOError('Path unavailable')
            pass
        else : 
            try :
                f = open(s._path, 'rb')
                s.db_dict = marshal.load(f)
                f.close()
            except :
                raise IOError('Path unavailable')
            pass

    def __del__(s):
        del s.db_dict

    def set_items(s, **i):
        s.db_dict.update(i)
        s._flush()

    def update(s, dict):
        s.db_dict.update(dict)
        s._flush()

    def clear(s):
        s.db_dict.clear()
        s._flush()

    def close(s):
        del s.db_dict

    def keys(s):
        return s.db_dict.keys()

    def values(s):
        return s.db_dict.values()

    def items(s):
        return s.db_dict.items()

    def _flush(s):
        try :
            f = open(s._path, 'wb')
            marshal.dump(s.db_dict, f)
            f.close()
        except :
            ui.note(zw('无法保存数据'), 'error')

    def __getitem__(s, k):
        return s.db_dict[k]

    def __setitem__(s, k, v):
        s.db_dict[k] = v
        s._flush()

    def __delitem__(s, k):
        del s.db_dict[k]
        s._flush()

    def backup(s, path):
        e32.file_copy(path, s._path)

    def recover(s, path):
        try :
            f = open(path, 'rb')
            tmp_dict = marshal.load(f)
            f.close()
        except :
            raise IOError('Path unavailable')
        s.update(tmp_dict)




class History(object, ) :

    __module__ = __name__
    def __init__(s, path):
        s.path = path
        if  not (os.path.exists(s.path)) : 
            open(s.path, 'w').close()
        f = open(s.path)
        s.list = [zw(p) for p in f.read().splitlines() if os.path.isfile(p) ]
        f.close()

    def _update(s):
        f = open(s.path, 'w')
        f.write('\n'.join([en(p) for p in s.list]))
        f.close()

    def write(s, p):
        if s.list.count(p) != 0 : 
            s.list.remove(p)
        s.list.insert(0, p)
        if len(s.list) > 30 : 
            s.list.pop()
        s._update()

    def remove(s, p):
        try :
            s.list.remove(p)
        except :
            pass
        s._update()

    def get_list(s):
        return [i for i in s.list if os.path.isfile(en(i)) ]

