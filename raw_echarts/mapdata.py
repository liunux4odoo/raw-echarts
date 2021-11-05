from pathlib import Path
import simplejson as json
import re
import difflib


__all__ = ['CustomMap', 'CITY_CORRDS', 'MAPS']


ROOT_PATH = Path(__file__).parent.absolute()


def _get_close_matches(*args, **kw):
    return difflib.get_close_matches(*args, **kw)[0]


def _is_english(text):
    return bool(re.match(r'^[a-zA-Z0-9\s\-_]+$', text))


def CustomMap(self, map_name, geo_json, special_areas=None):
    return {
        'mapName': map_name,
        'geoJSON': geo_json,
        'specialAreas': special_areas,
    }


class CityCoords:
    __ins = None
    __inited = False

    def __new__(cls):
        if cls.__ins is None:
            cls.__ins = super().__new__(cls)
        return cls.__ins

    def __init__(self):
        if not self.__inited:
            self.data = {}
            self.__class__.__inited = True

    def load_data(self, refresh=False):
        if not self.data or refresh:
            with ROOT_PATH.joinpath('data', 'city_coordinates.json').open(encoding='utf-8') as fp:
                self.data.update(json.load(fp))
        return self

    def __getitem__(self, key):
        key = _get_close_matches(key, self.data.keys())
        return key, self.data[key]

    def __setitem__(self, key, val):
        self.data[key] = val

    def update(self, d={}, **kw):
        self.data.update(d, **kw)


class Maps:
    __ins = None
    __inited = False

    def __new__(cls):
        if cls.__ins is None:
            cls.__ins = super().__new__(cls)
        return cls.__ins

    def __init__(self):
        if not self.__inited:
            self.cn = {}
            self.en = {}
            self.__class__.__inited = True

    def load_data(self, refresh=False):
        if not self.cn or refresh:
            with ROOT_PATH.joinpath('data', 'map_filename.json').open(encoding='utf-8') as fp:
                for k, v in json.load(fp).items():
                    if v[0].startswith('maps/'):
                        en = v[0].replace('maps/', '')
                        map = v[0]+'.'+v[1]
                        en = re.sub(r'[\d_]+', ' ', en).strip()
                        self.cn[k] = map
                        self.en[en] = map
        return self

    def __getitem__(self, key):
        if _is_english(key):
            key = _get_close_matches(key, self.en.keys())
            return self.en.__getitem__(key)
        else:
            key = _get_close_matches(key, self.cn.keys())
            return self.cn.__getitem__(key)


CITY_CORRDS = CityCoords()
MAPS = Maps()
