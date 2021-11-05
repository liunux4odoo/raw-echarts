import re
from lxml import etree
from io import StringIO
from raw_echarts.elements import *
from raw_echarts.layouts import *
from raw_echarts.axis import *
from raw_echarts.axis3D import *
from raw_echarts.toolbox import *
from raw_echarts.graphics import *
from raw_echarts.series import *
from raw_echarts.series3D import *


class NotebookRender:
    __ins = None
    __inited = False

    def __new__(cls):
        if cls.__ins is None:
            cls.__ins = super().__new__(cls)
        return cls.__ins

    def __init__(self):
        if not self.__inited:
            self.loaded_js = set()
            self.__class__.__inited = True

    def render(self, chart):
        from IPython.display import HTML, display

        self.load_js(*chart._js_dependences)
        return display(HTML(chart.render_embed()))

    def load_js(self, *jss):
        from IPython.display import HTML, Javascript, display

        for js in jss:
            if js not in self.loaded_js:
                self.loaded_js.add(js)
                if js[:4] not in ['http', 'file']:
                    js = CONFIG.ECHARTS_ASSETS+js
                # if js.startswith('http'):
                #     display(Javascript(url=js))
                # elif js.startswith('file'):
                #     with open(js.replace('file://',''),encoding='utf-8') as fp:
                #         display(Javascript(fp.read()))
                display(HTML('<script src="{}"></script>'.format(js)))

    def run_js(self, js):
        from IPython.display import Javascript, display

        return display(Javascript(js))


class Title(Option):
    text = RawOption(__doc__='title of chart')
    subtext = RawOption(__doc__='sub title of chart')
    link = RawOption(__doc__='title hyperlink',
                     value_choices=['self', 'blank'])
    sublink = RawOption(__doc__='sub title hyperlink')
    target = RawOption(__doc__='where to open the title link',
                       value_choices=['self', 'blank'])
    subtarget = RawOption(__doc__='where to open the sub title link',)

    padding = RawOption(__doc__=['padding of title box.',
                                 '- single value for 4 directions.',
                                 '- [x,y]: x for top and bottom, y for left and right.',
                                 '- [a,b,c,d]: padding for top, right, bottom, left.',
                                 ])
    itemGap = RawOption(__doc__='gap between title and subtitle.')

    textStyle = TextStyle(
        __doc__='style of title, see `styles.TextStyle` for more information.')
    subtextStyle = TextStyle(
        __doc__='style of subtitle, `see styles.TextStyle` for more information.')

    style = textStyle
    substyle = subtextStyle


class Legend(PositionMixin, StyleMixin, Option):
    show = RawOption()
    type = RawOption(value_choices=['plain', 'scroll'])
    orient = RawOption(value_choices=['horizontal', 'vertical'])
    selectMode = RawOption(value_choices=['single', 'multiple'])
    formatter = RawOption()
    data = RawOption([])
    icon = RawOption(value_choices=[
                     'circle', 'rect', 'roundRect', 'triangle', 'diamond', 'pin', 'arrow', 'none'])
    selected = Option()
    align = RawOption(value_choices=['auto', 'left', 'right'])
    padding = RawOption()
    itemGap = RawOption()
    itemWidth = RawOption()
    itemHeight = RawOption()
    inactiveColor = RawOption()
    symbolKeepAspect = RawOption()

    tooltip = Tooltip()
    textStyle = TextStyle()
    style = textStyle

    # scroll legend
    scrollDataIndex = RawOption()
    pageButtonItemGap = RawOption()
    pageButtonGap = RawOption()
    pageButtonPosition = RawOption(value_choices=['start', 'end'])
    pageFormatter = RawOption()
    pageIcons = RawOption()
    pageIconColor = RawOption()
    pageIconInactiveColor = RawOption()
    pageIconSize = RawOption()
    pageTextStyle = TextStyle()
    animation = RawOption()
    animationDurationUpdate = RawOption()


class DataZoom(PositionMixin, Option):
    type = RawOption(value_choices=['slider', 'inside'])
    filterMode = RawOption(
        value_choices=['filter', 'weakFilter', 'empty', 'none'])
    start = RawOption()
    end = RawOption()
    startValue = RawOption()
    endValue = RawOption()

    minSpan = RawOption()
    minValueSpan = RawOption()
    maxSpan = RawOption()
    maxValueSpan = RawOption()

    disabled = RawOption()

    xAxisIndex = RawOption([])
    yAxisIndex = RawOption([])
    radiusAxisIndex = RawOption([])
    angleAxisIndex = RawOption([])

    # inside
    orient = RawOption(value_choices=['horizontal', 'vertical'])
    zoomLock = RawOption()
    throttle = RawOption()
    rangeMode = RawOption()
    zoomOnMouseWheel = RawOption()
    moveOnMouseMove = RawOption()
    moveOnMouseWheel = RawOption()
    preventDefaultMouseMove = RawOption()

    # slider
    backgroundColor = RawOption()
    dataBackground = Option(lineStyle=LineStyle(), areaStyle=AreaStyle())
    lineStyle = Delegator('dataBackground', 'lineStyle')
    lineStyle = Delegator('dataBackground', 'areaStyle')
    fillColor = RawOption()
    borderColor = RawOption()
    handleIcon = RawOption()
    handleSize = RawOption()
    handleStyle = ItemStyle()

    textStyle = TextStyle()

    labelPrecision = RawOption()
    labelFormatter = RawOption()
    showDetail = RawOption()
    showDataShadow = RawOption()
    realtime = RawOption()


class VisualMap(PositionMixin, StyleMixin, Option):
    class Piece(Option):
        min = RawOption()
        max = RawOption()
        value = RawOption()
        label = RawOption()
        color = RawOption()
        gt = RawOption()
        gte = RawOption()
        lt = RawOption()
        lte = RawOption()

    class Range(Option):
        symbol = RawOption(value_choices=[
                           'circle', 'rect', 'roundRect', 'triangle', 'diamond', 'pin', 'arrow', 'none'])
        symbolSize = RawOption()
        color = RawOption()
        colorAlpha = RawOption()
        opacity = RawOption()
        colorLightness = RawOption()
        colorSaturation = RawOption()
        colorHue = RawOption()

    orient = RawOption()
    type = RawOption(value_choices=['continuous', 'piecewise'])
    min = RawOption()
    max = RawOption()
    range = RawOption([])
    inRange = Range()
    outOfRange = Range()
    textStyle = TextStyle()

    inverse = RawOption()
    precision = RawOption()
    itemWidth = RawOption()
    itemHeight = RawOption()
    align = RawOption(
        value_choices=['align', 'left', 'right', 'top', 'bottom'])
    text = RawOption([])
    textGap = RawOption()
    dimension = RawOption()
    seriesIndex = RawOption()
    hoverLink = RawOption()
    formatter = RawOption()

    # continuous
    calculable = RawOption(True)
    realtime = RawOption(True)

    # peicewise
    splitNumber = RawOption()
    categories = RawOption()
    minOpen = RawOption()
    maxOpen = RawOption()
    selectedMode = RawOption(value_choices=['single', 'multiple'])
    showLabel = RawOption()
    itemGap = RawOption()
    itemSymbol = RawOption(
        ['circle', 'rect', 'roundRect', 'triangle', 'diamond', 'pin', 'arrow', 'none'])
    pieces = Piece().to_array(False)


class Root(AnimationMixin, Option):
    color = RawOption()
    title = Title()

    grid = Grid().to_array()
    radar = LRadar().to_array()
    polar = Polar().to_array()
    calendar = Calendar().to_array()
    single = Single().to_array()
    parallel = Parallel().to_array()
    geo = Geo().to_array()

    globe = Globe()
    grid3D = Grid3D()

    xAxis = Axis().to_array()
    yAxis = Axis().to_array()
    radiusAxis = RadiusAxis()
    angleAxis = AngleAxis()

    xAxis3D = Axis3D()
    yAxis3D = Axis3D()
    zAxis3D = Axis3D()

    series = Series().to_array(False)

    legend = Legend()
    tooltip = Tooltip()
    toolbox = Toolbox()

    visualMap = VisualMap()
    dataZoom = DataZoom()

    def __init__(self, **kw):
        super().__init__(**kw)
        # self.xAxis.use()
        # self.yAxis.use()


class DataSet:
    pass


class Chart:
    def __init__(self, chart_id=None, width=600, height=400):
        self.chart_id = chart_id or str(id(self))
        self._option = Root()
        self.width = self.parse_size(width)
        self.height = self.parse_size(height)
        # self.set_colors([
        #     "#c23531",
        #     "#2f4554",
        #     "#61a0a8",
        #     "#d48265",
        #     "#749f83",
        #     "#ca8622",
        #     "#bda29a",
        #     "#6e7074",
        #     "#546570",
        #     "#c4ccd3",
        #     "#f05b72",
        #     "#ef5b9c",
        #     "#f47920",
        #     "#905a3d",
        #     "#fab27b",
        #     "#2a5caa",
        #     "#444693",
        #     "#726930",
        #     "#b2d235",
        #     "#6d8346",
        #     "#ac6767",
        #     "#1d953f",
        #     "#6950a1",
        #     "#918597"
        # ])
        self._js_dependences = []
        self.notebook = NotebookRender()

    def __getitem__(self, key):
        return self._option[key]

    def __getattr__(self, attr):
        if hasattr(self._option, attr):
            return getattr(self._option, attr)
        raise AttributeError(f'"{self}" object has no attribute: "{attr}"')

    def get_option(self):
        def _p(v):
            if isinstance(v, RawOption):
                return _p(v._data)
            if isinstance(v, Option):
                if v._as_array and isinstance(v._data, ODD):
                    return [_p(x) for x in v._data.value_list]
                else:
                    return _p(v._data)
            if isinstance(v, list):
                return [_p(x) for x in v]
            if isinstance(v, (dict, ODD)):
                return dict([(v._get_data_key() if isinstance(v, OptionBase) else _p(k), _p(v)) for k, v in v.items()])
            return v
        return _p(self._option._data)

    def parse_size(self, v):
        if isinstance(v, int):
            v = f'{v}px'
        elif isinstance(v, float):
            v = f'{v*100:.0f}%'
        elif isinstance(v, str):
            v = v.strip()
            if not v.endswith('px') and not v.endswith('%'):
                v += 'px'
        return v

    def opts(self, d={}, **kw):
        self._option.opts(d, **kw)
        return self

    def set_colors(self, colors=[]):
        self.opts(color=colors)

    def to_json(self):
        return dumps(self.get_option())

    def clone(self):
        obj = type(self)(width=self.width, height=self.height)
        obj._option = self._option.clone()
        obj._js_dependences = self._js_dependences.copy()
        return obj

    def render_embed(self):
        root = etree.Element('div', {'id': f'{self.chart_id}_container'})
        div = etree.Element('div', {'id': self.chart_id, 'class': 'chart-container', 'style': f'width:{self.width};height:{self.height};'})
        script = etree.Element('script')
        script.text = f'''
        var chart_{self.chart_id}=echarts.init(document.getElementById("{self.chart_id}"),"white",{{"renderer":"canvas"}});
        var option_{self.chart_id}={self.to_json()};
        chart_{self.chart_id}.setOption(option_{self.chart_id});
        '''
        div.append(script)
        root.append(div)
        content = etree.tostring(
            root, method='HTML', pretty_print=True).decode()
        return content

    def render_file(self, file=None, title='Awesome Echarts'):
        root = etree.HTML('<html/>')

        head = etree.Element('head')
        metas = [
            etree.Element('meta', charset='UTF-8'),
            etree.Element('meta', name='viewport',
                          content='width=device-width, initial-scale=1'),
            etree.Element('meta', name='theme-color', content='#000000'),
            etree.Element('meta', name='description',
                          content='Awesome ECharts')
        ]
        t = etree.Element('title')
        t.text = title
        script = etree.Element('script', {
                               'type': 'text/javascript', 'src': CONFIG.ECHARTS_ASSETS+'/echarts.min.js'})
        for m in metas:
            head.append(m)
        head.append(t)
        head.append(script)

        for js in self._js_dependences:
            head.append(etree.Element(
                'script', {'type': 'text/javascript', 'src': js}))

        body = etree.Element('body')
        noscript = etree.Element('noscript')
        noscript.text = 'you should enable javascript to run this app.'
        body.append(noscript)
        body.append(etree.fromstring(self.render_embed()))

        root.append(head)
        root.append(body)
        content = etree.tostring(
            root, method='HTML', pretty_print=True).decode()
        content = '<!DOCTYPE html>\n'+content

        if isinstance(file, str):
            if not file.endswith('.html'):
                file += '.html'
            with open(file, 'w', encoding='utf-8') as fp:
                fp.write(content)
        elif hasattr(file, 'write'):
            file.write(content)
            file.seek(0)
        return content

    def render_notebook(self):
        obj = self.clone()
        obj.notebook.render(obj)
        return obj

    def setOption(self, option, notMerge=False, lazyUpdate=False):
        self.call_js('setOption', option, notMerge, lazyUpdate)

    def register_map(self, name, geo_json, special_areas):
        self.notebook.run_js('echarts.registerMap({},{},{})'.format(
            name, dumps(geo_json), dumps(special_areas)))

    def load_javascript(self):
        self.notebook.load_js(*self._js_dependences)

    def call_js(self, func, *args, **kw):
        args = dumps(list(args))[1:-1]
        kw = ', '.join(['{}={}'.format(k, json.dumps(v))
                        for k, v in kw.items()])
        if kw:
            kw = ', '+kw
        js = 'chart_{}.{}({}{})'.format(self.chart_id, func, args, kw)
        self.notebook.run_js(js)

    def anim(self, animation=True, **kw):
        self.opts({'animation': animation})
        self.opts(**kw)
        return self

    def add_chart(self, s, legend=True, icon=None, selected=True):
        self.series.add(s)

        if legend:
            self.legend.use()

        if isinstance(s, (Scatter, EffectScatter)):
            self.uses('xAxis', 'yAxis')
        elif isinstance(s, (Scatter3D)):
            self.uses('grid3D', 'xAxis3D', 'yAxis3D', 'zAxis3D')

        if legend:
            i = legend-1
            if i > 0:
                self.legend.add()
                while i > len(self.legend):
                    self.legend.add()
            if icon:
                self.legend.data.append({'name': s['name'], 'icon': icon})
            else:
                self.legend.data.append(s['name'])
            self.legend.selected[s['name']] = selected
        for x in s._js_dependences:
            if x not in self._js_dependences:
                self._js_dependences.append(x)
        return self


def _echarts_assets_callback(name, value, old):
    if name == 'ECHARTS_ASSETS':
        NotebookRender().load_js('echarts.min.js')


CONFIG.add_callback(_echarts_assets_callback)

if __name__ == '__main__':
    CONFIG.ECHARTS_ASSETS = r'file://f:/myrepo/pyecharts-assets/assets'

    c = Chart()
    c.anim(duration=1000)
    c.xAxis.opts(data=[1, 2, 3])
    c.yAxis.use()
    c.title(text='this is a title', sub=r'sub title')
    c.title.style(color='red', style='italic')
    c.tooltip.use()

    bar = Bar('y', [1, 2, 3])
    bar.opts(color=LinearGradient(0, 0, 0, 1, colors=[
             'red', 'blue'], globalCoord=False))
    bar.label(show=True, formatter=JsCode('function(p){return p.value*3;}'))
    c.add_chart(bar, icon=Image(
        file=r'D:\Program files\360\360Chrome\Chrome\User Data\Default\Extensions\kpbnombpnpcffllnianjibmpadjolanh\1.2.30_0\statics\imgs\arrow_down.svg').url)

    c.render_file(r'e:\temp\render.html')

    for k, v in c.get_option().items():
        print(k, v)
