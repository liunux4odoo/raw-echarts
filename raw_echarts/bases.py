from collections import OrderedDict
from copy import deepcopy
import uuid
import os
import simplejson as json
import base64
from datetime import date, time, datetime


def CustomAttributeError(obj, attr):
    return AttributeError('{} has no attribute: "{}"'.format(obj, attr))


class CustomJsonEncoder(json.JSONEncoder):
    '''
    encode date/time/datetime to isoformat, JsCode without quotes.
    '''

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._to_replace = {}

    def default(self, o):
        if isinstance(o, JsCode):
            key = uuid.uuid4().hex
            self._to_replace[key] = o.js
            return key
        elif isinstance(o, Image):
            return o.url or o.uri
        elif isinstance(o, (date, time, datetime)):
            return o.isoformat()
        elif isinstance(o, Empty):
            return super().default(None)
        elif isinstance(o, ODD):
            return o._data
        elif isinstance(o, RawOption):
            return o._data
        elif isinstance(o, Option):
            if o._as_array:
                return o._data.value_list
            else:
                return o._data
        return super().default(o)

    def encode(self, obj):
        content = super().encode(obj)
        for k, v in self._to_replace.items():
            content = content.replace('"{}"'.format(k), v)
        return content


def dumps(obj, indent=4, sort_keys=False, ensure_ascii=True):
    '''
    dump an option object to json
    '''
    return json.dumps(obj, ensure_ascii=ensure_ascii, cls=CustomJsonEncoder, indent=indent, sort_keys=sort_keys)


class _Config:
    '''
    some global config including:
            echarts js assets url
            type of notebook, notebook or lab
    '''
    __ins = None
    __inited = False

    def __new__(cls):
        if cls.__ins is None:
            cls.__ins = super().__new__(cls)
        return cls.__ins

    def __init__(self):
        if not self.__class__.__inited:
            self._data = {}
            self._callbacks = set()
            self.ECHARTS_ASSETS = 'http://127.0.0.1/assets/'
            # todo: support help text in different languages.
            self.LOCALE = 'CN'
            self.__class__.__inited = True

    def add_callback(self, callback=None):
        if callable(callback):
            self._callbacks.add(callback)

    def __getattr__(self, attr):
        return self._data.get(attr)

    def __setattr__(self, attr, val):
        if attr.startswith('_'):
            super().__setattr__(attr, val)
        else:
            old = self._data.get(attr)
            self._data[attr] = val
            for c in self._callbacks:
                c(attr, val, old)

    def __getitem__(self, key):
        return self._data.get(key)

    def __setitem__(self, key, val):
        self._data.__setitem__(key, val)


CONFIG = _Config()


class Empty:
    '''
    an 'empty' object like NoneType, but can give emtpy result when access it's attribute.
    '''
    _ins = None

    def __new__(cls):
        if cls._ins is None:
            cls._ins = super().__new__(cls)
        return cls._ins

    def __getattr__(self, attr):
        return None  # Empty()

    def __getitem__(self, key):
        return None  # Empty()

    def __eq__(self, rhs):
        if rhs is None:
            return True
        return False


def similar_param(k, l=[], threshold=1/3):
    '''
    automatically convert some short params to correct formation
    '''
    def p(x, y):
        m = 0
        if len(x) > len(y):
            x, y = y, x

        i = 0
        while True:
            if i >= len(x):
                break
            t = x[i]
            if t in y:
                m += 1
                x = x.replace(t, '', 1)
                y = y.replace(t, '', 1)
            else:
                i += 1
        return m/(m+len(x)+len(y))

    if k in ['type_', 'min_', 'max_']:
        return k[:-1]

    if not l or not isinstance(k, str):
        return k

    t = []
    for x in l:
        if x == k:
            t.append((3, x))
        elif isinstance(x, str):
            t.append((p(x.lower(), k.lower()), x))
        else:
            t.append((0, x))
    p, x = sorted(t)[-1]
    if p > threshold and len(k) <= len(x):
        k = x
    return k


class JsCode:
    '''
    wrap js code to json, same as pyecharts.
    '''

    def __init__(self, js):
        self.js = js
        self.js_code = '{p}{js}{p}'.format(p='--x_x--0_0--', js=js)


def LinearGradient(x0=0, y0=0, x1=0, y1=1, colors=[], globalCoord=False):
    '''
    wrapper of echarts.graphic.LinearGradient.
    colors could be list of colors, list of data pair, list of dict({offset:x,color:y} or {x:y}).
    '''
    offset = 0
    data = []
    for c in colors:
        if isinstance(c, (list, tuple)) and len(c) == 2:
            data.append({'offset': c[0], 'color': c[1]})
        elif isinstance(c, dict):
            if len(c) == 1 and isinstance(c.keys[0], (float, int)):
                data.append(
                    {'offset': c.keys()[0], 'color': c.values()[0]})
            else:
                data.append(c)
        else:
            data.append({'offset': offset, 'color': c})
            offset += 1

    max_offset = max([x['offset'] for x in data])
    if max_offset > 1:
        for x in data:
            x['offset'] = round(x['offset']/max_offset, 2)

    data = dumps(data, indent=None)
    globalCoord = dumps(globalCoord)
    js = f'''new echarts.graphic.LinearGradient({x0},{y0},{x1},{y1},{data},{globalCoord})'''
    return JsCode(js)


class Image:
    '''
    different types of image used in option:
    '''

    def __init__(self, url=None, file=None):
        self._url = url
        self._file = os.path.abspath(file)

    @property
    def url(self):
        if self._url:
            return 'image://'+self._url
        if self._file:
            return 'image://'+self._file

    @property
    def uri(self):
        if self._file:
            if self._file.endswith('.svg'):
                try:
                    r = etree.parse(self._file).get_root()
                    return 'path://'+r.findall('path', namespaces=r.nsmap)[0].get('d', '')
                except:
                    pass
            else:
                with open(file, 'br') as fp:
                    data = fp.read()
                ext = os.path.splitext(file)[-1][1:]
                return 'image://data:image/{};base64,{}'.format(ext, base64.urlsafe_b64encode(data).decode())


class ODD:
    '''
    wrapper of OrderedDict, features:
    '''

    def __init__(self, *args, **kw):
        self._data = OrderedDict(*args, **kw)
        self._inited = True

    def __getattr__(self, attr):
        if attr.startswith('__'):
            raise CustomAttributeError(self, attr)

        if attr in self._data.keys():
            return self._data[attr]

        raise CustomAttributeError(self, attr)

    def __getitem__(self, key):
        if isinstance(key, int):
            key = self.key(key)
        return self._data[key]

    def __setitem__(self, key, val):
        if isinstance(key, int):
            key = self.key(key)
        self._data[key] = val

    def __repr__(self):
        if '_inited' in self.__dict__:
            return dict(self._data).__repr__()
        return super().__repr__()

    def __len__(self):
        return len(self._data)

    def get(self, key):
        return self._data.get(key)

    def update(self, d, **kw):
        return self._data.update(d, **kw)

    def index(self, key_or_val, positive=False):
        dl = len(self._data)

        if isinstance(key_or_val, int):
            if key_or_val < 0 and positive:
                key_or_val += dl
            if -dl <= key_or_val < dl:
                return key_or_val

        if key_or_val in self._data.values():
            return list(self._data.values()).index(key_or_val)

        if key_or_val in self._data.keys():
            return list(self._data.keys()).index(key_or_val)

    def key(self, index=None, value=None):
        if index is not None:
            index = self.index(index)
        if value is not None:
            index = self.index(value)

        if index is not None:
            return list(self._data.keys())[index]

        return index

    def add(self, val, key=None, after=None, before=None):
        if key is None:
            key = uuid.uuid4().hex

        dl = len(self._data)
        index = dl

        if after is not None:
            t = self.index(after, True)
            if isinstance(index, int):
                index = t+1

        if before is not None:
            t = self.index(before)
            if isinstance(t, int):
                index = t

        if index == -1 or index >= dl:  # append
            self._data[key] = val
        elif index == 0 or index <= -dl:  # prepend
            self._data[key] = val
            self._data.move_to_end(key, False)
        else:
            items = list(self._data.items())
            self._data = OrderedDict(items[:index]+[(key, val)]+items[index:])
        return self

    def append(self, val):
        return self.add(val)

    def pop(self, key=-1):
        key = self.key(key)
        return self._data.pop(key)

    def clone(self):
        return type(self)(deepcopy(self._data).items())

    def items(self):
        return self._data.items()

    @property
    def key_list(self):
        return list(self._data.keys())

    @property
    def value_list(self):
        return list(self._data.values())


class Delegator:
    def __init__(self, *path):
        self.path = tuple([x._name if isinstance(
            x, OptionBase) else x for x in path])

    def __repr__(self):
        return 'Delegator{}'.format(str(self.path))

    def get_instance(self, obj, owner=None):
        if obj is None:
            return self
        else:
            for p in self.path:
                obj = getattr(obj, p)
        return obj

    def __get__(self, obj, owner):
        return self.get_instance(obj, owner)

    def __set__(self, obj, value):
        for p in self.path[:-1]:
            obj = getattr(obj, p)
        setattr(obj, self.path[-1], value)


class OptionMeta(type):
    '''
    add seperate `_meta` that holding all params and delegators to every Option class
    '''
    def __new__(cls, clsname, bases, attrs):
        attrs['_meta'] = ODD(params=ODD(), delegators=ODD())
        return super().__new__(cls, clsname, bases, attrs)

    def __init__(self, clsname, bases, attrs):
        super().__init__(clsname, bases, attrs)
        meta = attrs['_meta']

        for b in bases[-1::-1]:
            for k, v in b.__dict__.items():
                if 'OptionMeta' in str(type(type(v))):
                    meta['params'][v._name] = v
                elif 'Delegator' in str(type(v)):
                    meta['delegators'][k] = tuple(v.path)

        for k, v in attrs.items():
            if 'OptionMeta' in str(type(type(v))):
                meta['params'][v._name] = v
            elif 'Delegator' in str(type(v)):
                meta['delegators'][k] = tuple(v.path)


class OptionBase(metaclass=OptionMeta):
    '''
    base class for Options, acts as descritor and data carrier.
    '''
    PARAM_THRESHOLD = 1/3

    def __init__(self, value_choices=[], __doc__=None, data_key=None):
        self._parent = None
        self._name = None
        self._data_key = data_key
        self._owner = None
        self._data = None
        self._used = False
        self._as_array = False
        self._as_raw = False
        self._value_choices = value_choices

        for k, v in self._meta.params.items():
            self.__dict__[k] = v.clone(self)

        doc = ''

        if __doc__:
            if isinstance(__doc__, (list, tuple)):
                __doc__ = '\n\t'.join(__doc__)
            doc = doc+'\n\t'+__doc__
        if self._value_choices:
            doc += '\n\n\tavailable choices:\n\t'+str(self._value_choices)
        if doc:
            self.__doc__ = doc
        self._inited = True

    def __bool__(self):
        return True

    def _get_data_key(self):
        return self._data_key or self._name

    def set_parent(self, parent=None):
        self._parent = parent
        return self

    # act as descriptor
    def __set_name__(self, owner, name):
        self._owner = owner
        if self._name is None:
            self._name = name

    def __get__(self, obj, owner):
        if isinstance(obj, OptionBase):
            return obj.__dict__[self._name]
        else:
            return self

    def __set__(self, obj, value):
        if isinstance(obj, OptionBase):
            self.__get__(obj, self._owner).set(value, obj)

    def __delete__(self, obj):
        if isinstance(obj, OptionBase):
            self.__get__(obj, self._owner).unuse()
        return self

    # act as data carrier
    def __getattr__(self, attr):
        if attr.startswith('__'):
            raise CustomAttributeError(self, attr)

        if self._as_raw:
            try:
                ret = getattr(self._data, attr)
                if attr in ['append', 'insert', 'add', 'update']:
                    self.use()
                return ret
            except:
                raise CustomAttributeError(self, attr)
        elif self._as_array:
            if len(self._data) > 0 and attr in self._data[-1].key_list:
                try:
                    ret = getattr(self._data[-1], attr)
                    if attr in ['append', 'insert', 'add', 'update']:
                        self.use()
                    return ret
                except:
                    raise CustomAttributeError(self, attr)

        else:
            try:
                return self._data[attr]
            except:
                raise CustomAttributeError(self, attr)

    def __call__(self, d={}, **kw):
        if self._as_raw:
            self.set(d)
        else:
            self.opts(d, **kw)
        return self._parent

    def __len__(self):
        return len(self._data)

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, val):
        if isinstance(val, OptionBase):
            val = val._data

        if self._as_array:
            if len(self._data) > 0:
                self._data[-1][key] = val
        else:
            self._data[key] = val
        self.use()

    def _get_similar_param(self, param):
        return similar_param(param, self._meta['params'].key_list+self._meta['delegators'].key_list, self.PARAM_THRESHOLD)

    def _get_similar_value(self, value):
        return similar_param(value, self._value_choices, self.PARAM_THRESHOLD)

    def set(self, value, obj=None):
        if self._value_choices:
            value = self._get_similar_value(value)

        if isinstance(value, OptionBase):
            value = value._data
        else:
            vlaue = value

        obj = obj or self._parent
        if isinstance(obj, OptionBase):
            ins = obj.__dict__[self._name]
            if value is not ins:
                ins._data = value
            ins.use()
        else:
            if value is not ins:
                self._data = value
            self.use()

    def clone(self, new_parent=None):
        obj = type(self)()

        if isinstance(self._data, ODD):
            obj._data = self._data.clone()
        else:
            obj._data = deepcopy(self._data)
        obj._parent = new_parent
        obj._name = self._name
        obj._data_key = self._data_key
        obj._as_array = self._as_array
        obj._as_raw = self._as_raw
        obj._value_choices = self._value_choices

        return obj

    def use(self):
        parent = self._parent
        if isinstance(parent, OptionBase) and not self._used:
            parent.use()
            parent._data[self._get_data_key()] = self
            self._used = True

        return self

    def uses(self, *children):
        for c in children:
            c = self._get_similar_param(c)
            getattr(self, c).use()
        return self

    def unuse(self):
        parent = self._parent
        if isinstance(parent, OptionBase) and self._used:
            parent._data.pop(self._get_data_key())
            self._used = False
        return self._parent

    def _parse_kw(self, kw):
        d = {}
        params = self._meta['params'].key_list

        for k, v in kw.items():
            k = self._get_similar_param(k)
            v = self._get_similar_value(v)
            d[k] = v
        return d

    def opts(self, d={}, **kw):
        obj = self.use()
        if obj._as_array and len(obj) > 0:
            obj = obj[-1]

        if not isinstance(d, dict) and not kw:
            obj.set(d)
        else:
            kw = obj._parse_kw(kw)
            d = d or {}
            d = d.copy()
            d.update(kw)

            for k, v in d.items():
                if k in obj._meta.params.key_list+obj._meta.delegators.key_list:
                    getattr(obj, k).set(v)
                else:
                    obj._data.update({k: v})
        return obj

    def to_array(self, preserve_value=True):
        if not self._as_array:
            new_data = ODD()
            obj = self.clone()  # todo: set attribute of array element will not use parent automaticlly
            if preserve_value:
                key = None
                if isinstance(self._data, ODD) and 'name' in self._data.key_list:
                    key = self._data['name']
                new_data.add(obj, key)
            self._data = new_data
            self._as_array = True
        return self

    def to_object(self, preserve_value=-1):
        if self._as_array:
            new_data = ODD()
            if len(self._data) > 0 and preserve_value is not None:
                obj = self._data[preserve_value]
                new_data.update(deepcopy(obj._data))
                for k, v in obj._data.items():
                    if isinstance(v, OptionBase):
                        v._parent = self
            self._data = new_data
            self._as_array = False
        return self

    def to_raw(self, value=None):
        if not self._as_raw:
            self._as_raw = True
            value = value or self._data or value
            self._data = value
            self.use()
        return self

    def add(self, d={}, **kw):
        self.to_array()
        self.use()

        if isinstance(d, Option) and not kw:
            val = d
        else:
            val = self.clone().to_object()
            val.opts(d, **kw)

        key = None
        if 'name' in val._data.key_list:
            key = val._data['name']

        self._data.add(val, key)
        return self

    # def append(self, *args, **kw):
    #     if self._as_raw:
    #         return self._data.append(*args,**kw)
    #     else:
    #         return self.add(*args, **kw)

    def remove(self, key=-1):
        self._data.pop(key)
        return self

    def clear(self, unuse=False):
        parsed = []

        for k, v in self._meta['params'].items():
            ins = self.__dict__[k]
            if ins._used:
                if v not in parsed:
                    parsed.append(v)
                    ins = v.clone()
                    ins._parent = self
                    self.__dict__[k] = ins
                    if unuse:
                        self.unuse()
                else:
                    self.__dict__[k] = self.__dict__[v._name]

    @classmethod
    def delegate(cls, target, new_names={}, prefix=''):
        if isinstance(target, str):
            target = cls._meta.params[target]

        for k, v in target._meta['params'].items():
            n = new_names.get(k)
            if not n:
                if prefix:
                    n = prefix+k[0].upper()+k[1:]
                else:
                    n = k
            d = Delegator(target._name, k)
            setattr(cls, n, d)
            cls._meta.delegators[n] = d

    def add_param(self, name, param):
        param._name = name
        self._meta.params[name] = param
        self.__dict__[name] = param.clone(self)


class RawOption(OptionBase):
    '''
    Option that operates on raw value
    '''

    def __init__(self, value=None, value_choices=[], __doc__=None, data_key=None):
        super().__init__(value_choices=value_choices, __doc__=__doc__, data_key=data_key)
        self.to_raw(value)

    def __repr__(self):
        if '_inited' in self.__dict__:
            return '{}({})'.format(self.__class__.__name__, self._data.__repr__())
        return super().__repr__()


class Option(OptionBase):
    '''
    Option that operates as object and array
    '''
    id = RawOption()
    show = RawOption()
    zlevel = RawOption()
    z = RawOption()

    def __init__(self, d={}, value_choices=[], __doc__=None, **kw):
        super().__init__(value_choices=value_choices, __doc__=__doc__)
        self._data = ODD()
        self.opts(d, **kw)

    def __repr__(self):
        if '_inited' in self.__dict__:
            if self._as_array:
                name = self.__class__.__name__+'Array'
                text = self._data.value_list.__repr__()
            else:
                name = self.__class__.__name__
                text = self._data.__repr__()
            return '{}({})'.format(name, text)
        return super().__repr__()


if __name__ == '__main__':
    o = Option()
