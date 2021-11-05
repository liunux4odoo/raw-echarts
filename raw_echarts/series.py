from raw_echarts.elements import *
from raw_echarts.mapdata import *
from raw_echarts.axis import *


class Series(Option):
    type = RawOption()
    name = RawOption()
    label = Label(position='top')
    data = RawOption([])
    datasetIndex = RawOption()
    dimensions = Dimension().to_array(False)
    encode = RawOption({})

    visualMap = RawOption()
    tooltip = Tooltip()
    seriesLayoutBy = RawOption(value_choices=['column', 'row'])
    clip = RawOption()

    legendHoverLink = RawOption()
    hoverAnimation = Animation()

    coordinateSystem = RawOption(value_choices=['cartesian2d', 'polar'])
    xAxisIndex = RawOption()
    yAxisIndex = RawOption()
    polarIndex = RawOption()
    geoIndex = RawOption()
    calendarIndex = RawOption()

    cursor = RawOption()

    large = RawOption()
    largeThreshold = RawOption()
    progressive = RawOption()
    progressiveThreshold = RawOption()
    progressiveChunkMode = RawOption(value_choices=['sequential', 'mod'])

    markPoint = MarkPoint()
    markLine = MarkLine()
    markArea = MarkArea()

    emphasis = Emphasis()

    def __init__(self, type=None, name=None, data=[], **kw):
        super().__init__(type=type, name=name, data=data, **kw)
        self._js_dependences = ['echarts.min.js']

    def add_js_link(self, js_link):
        if js_link not in self._js_dependences:
            self._js_dependences.append(js_link)
        return self


Series.delegate('hoverAnimation', prefix='hover2')


class SeriesData(Option):
    pass


class LiquidFill(Option):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_js_link('echarts-liquidfill.min.js')


class WordCloud(Option):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_js_link('echarts-wordcloud.min.js')


class BarBackgroundStyle(StyleMixin):
    barBorderRadius = RawOption()


class Bar(Series):
    stack = RawOption()
    roundCap = RawOption()
    barWidth = RawOption()
    barMaxWidth = RawOption()
    barMinWidth = RawOption()
    barMinHeight = RawOption()
    barGap = RawOption()
    barCategoryGap = RawOption()

    color = RawOption([])
    itemStyle = ItemStyle()

    showBackground = RawOption()
    backgroundStyle = BarBackgroundStyle()

    def __init__(self, name='', data=[], **kw):
        super().__init__('bar', name, data, **kw)


def _parse_data_pair(data, columns=[]):
    if not columns:
        columns = ['name', 'value']

    new_data = []
    for x in data:
        d = {}
        if isinstance(x, dict):
            d.update(x)
        elif isinstance(x, (list, tuple)):
            for i, y in enumerate(x):
                if isinstance(y, dict):
                    d.update(y)
                elif i < len(columns):
                    d.update({columns[i]: y})
        else:
            d = x
        new_data.append(d)
    return new_data


class LabelLine(Option):
    lineStyle = LineStyle()


class Pie(PositionMixin, AnimationMixin, Series):
    center = RawOption()
    radius = RawOption()
    roseType = RawOption(value_choices=['radius', 'angle', 'area'])
    selectedMode = RawOption(value_choices=['single', 'multiple'])
    selectedOffset = RawOption()
    clockwise = RawOption()
    startAngle = RawOption()
    minAngle = RawOption()
    minShowLabelAngle = RawOption()
    avoidLabelOverlap = RawOption()
    stillShowZeroSum = RawOption()

    labelLine = LabelLine()
    lineStyle = Delegator('labelLine', 'lineStyle')

    def __init__(self, name='', data=[], **kw):
        new_data = _parse_data_pair(
            data, ['name', 'value', 'selected', 'label', 'labelLine', 'emphasis'])
        super().__init__('pie', name, new_data, **kw)


class Map(Series):
    # todo: these options could be share between map and geo coordinate
    mapType = RawOption()
    roam = RawOption()
    center = RawOption()
    aspectScale = RawOption()
    bounddingCoords = RawOption()
    zoom = RawOption()
    scaleLimit = RawOption()
    nameMap = RawOption()
    nameProperty = RawOption()
    selectedMode = RawOption()

    def __init__(self, mapType='china', name='', data=[], **kw):
        new_data = _parse_data_pair(data, columns=['name', 'value', 'label'])
        super().__init__('map', name, new_data, mapType=mapType, **kw)
        MAPS.load_data()
        self.add_js_link(MAPS[mapType])


class Line(SymbolMixin, Series):
    stack = RawOption()
    connectNulls = RawOption()
    smooth = RawOption()
    smoothMonotone = RawOption()
    sampling = RawOption(value_choices=['average', 'max', 'min', 'sum'])

    itemStyle = ItemStyle()
    lineStyle = LineStyle()
    areaStyle = AreaStyle()

    def __init__(self, name='', data=[], **kw):
        super().__init__('line', name, data, **kw)


class ScatterData(SymbolMixin, Option):  # todo: a common series data class
    label = RawOption()


class Scatter(SymbolMixin, Series):
    def __init__(self, name='', data=[], **kw):
        super().__init__('scatter', name, data, **kw)


class RippleEffect(Option):
    color = RawOption()
    period = RawOption()
    scale = RawOption()
    brushType = RawOption(value_choices=['stroke', 'fill'])


class EffectScatter(SymbolMixin, Series):
    effectType = RawOption(value_choices=['ripple'])
    showEffectOn = RawOption(value_choices=['render', 'emphasis'])
    rippleEffect = RippleEffect()

    def __init__(self, name='', data=[], **kw):
        super().__init__('effectScatter', name, data, **kw)


class Radar(SymbolMixin, Series):
    radarIndex = RawOption()

    def __init__(self, name='', data=[], **kw):
        super().__init__('radar', name, data, **kw)


class TreeData(Option):
    name = RawOption()
    label = Label()
    value = RawOption()
    collapsed = RawOption()
    itemStyle = ItemStyle()

    children = RawOption([])


class Tree(SymbolMixin, PositionMixin, Series):
    layout = RawOption(value_choices=['orthogonal', 'radial'])
    orient = RawOption()

    edgeShape = RawOption(value_choices=['curve', 'polyline'])
    edgeForkPosition = RawOption()
    roam = RawOption(value_choices=['move', 'pan', 'scale', 'zoom'])
    expandAndCollapse = RawOption()
    initialTreeDepth = RawOption()

    leaves = Option(label=Label(), emphasis=Emphasis())

    def __init__(self, name='', data=[], **kw):
        super().__init__('tree', name, data, **kw)


class TreeMapLevel(ColorMixin, Option):
    visualDimension = RawOption()
    visualMin = RawOption()
    visualMax = RawOption()
    colorMappingBy = RawOption(value_choices=['value', 'index', 'id'])
    visibleMin = RawOption()
    childrenVisibleMin = RawOption()
    label = Label()
    upperLabel = Label()
    emphasis = Emphasis()


class BreadCrumb(PositionMixin, Option):
    emptyItemWidth = RawOption()
    itemStyle = ItemStyle()
    emphasis = Emphasis()


class TreeMap(SymbolMixin, PositionMixin, Series):
    squareRatio = RawOption()
    leafDepth = RawOption()
    drillDownIcon = RawOption()
    roam = RawOption(value_choices=['move', 'pan', 'scale', 'zoom'])
    nodeClick = RawOption(value_choices=['zoomToNode', 'link'])
    zoomToNodeRatio = RawOption()
    levels = TreeMapLevel().to_array(False)

    visualDimension = RawOption()
    colorMappingBy = RawOption(value_choices=['value', 'index', 'id'])
    visibleMin = RawOption()
    childrenVisibleMin = RawOption()

    label = Label()
    upperLabel = Label()

    def __init__(self, name='', data=[], **kw):
        super().__init__('treemap', name, data, **kw)


class SunburstHighlight(Option):
    label = Label()
    itemStyle = ItemStyle()


class SunburstDownplay(Option):
    label = Label()
    itemStyle = ItemStyle()


class Sunburst(AnimationMixin, Series):
    center = RawOption()
    radius = RawOption()
    highlight = SunburstHighlight()
    downplay = SunburstDownplay()
    levels = RawOption()

    def __init__(self, name='', data=[], **kw):
        super().__init__('sunburst', name, data, **kw)


class Boxplot(AnimationMixin, Series):
    layout = RawOption(value_choices=['vertical', 'horizontal'])
    boxWidth = RawOption()

    def __init__(self, name='', data=[], **kw):
        super().__init__('boxplot', name, data, **kw)


class CandleStick(AnimationMixin, Series):
    layout = RawOption(value_choices=['vertical', 'horizontal'])
    barWidth = RawOption()
    barMinWidth = RawOption()
    barMaxWidth = RawOption()

    def __init__(self, name='', data=[], **kw):
        super().__init__('candlestick', name, data, **kw)


KLine = CandleStick


class HeatMap(AnimationMixin, Series):
    # geo coord
    pointSize = RawOption()
    blurSize = RawOption()
    minOpacity = RawOption()
    maxOpacity = RawOption()

    def __init__(self, name='', data=[], **kw):
        super().__init__('heatmap', name, data, **kw)


class Parallel(AnimationMixin, Series):
    parallelIndex = RawOption()

    def __init__(self, name='', data=[], **kw):
        super().__init__('parallel', name, data, **kw)


class LinesEffect(SymbolMixin, Option):
    period = RawOption()
    delay = RawOption()
    constantSpeed = RawOption()
    color = RawOption()
    trailLength = RawOption()
    loop = RawOption()


class Lines(AnimationMixin, SymbolMixin, Series):
    polyline = RawOption()
    effect = LinesEffect()

    def __init__(self, name='', data=[], **kw):
        super().__init__('lines', name, data, **kw)


class GraphForce(Option):
    initLayout = RawOption()
    repulsion = RawOption()
    gravity = RawOption()
    edgeLength = RawOption()
    layoutAnimation = RawOption()
    friction = RawOption()


class GraphCategory(SymbolMixin, Option):
    name = RawOption()
    itemStyle = ItemStyle()
    label = Label()
    emphasis = Emphasis()


class Graph(AnimationMixin, SymbolMixin, Series):
    layout = RawOption(value_choices=['none', 'force', 'circluar'])
    center = RawOption()
    zoom = RawOption()
    roam = RawOption()
    nodeScaleRatio = RawOption()
    focusNodeAdjacency = RawOption()
    edgeSymbol = RawOption()
    edgeSymbolSize = RawOption()
    edgeLabel = Label()
    categories = GraphCategory().to_array(False)

    # circular
    circular = Option(rotateLabel=RawOption())
    rotateLabel = Delegator('circular', 'rotateLabel')

    # force
    force = GraphForce()
    draggable = RawOption()

    def __init__(self, name='', data=[], **kw):
        super().__init__('graph', name, data, **kw)


class Sankey(PositionMixin, SymbolMixin, Series):
    nodeWidth = RawOption()
    nodeGap = RawOption()
    nodeAlign = RawOption(value_choices=['left', 'justify', 'right'])
    layoutIterations = RawOption()
    orient = RawOption(value_choices=['horizontal', 'vertical'])
    draggable = RawOption()
    focusNodeAdjacency = RawOption()
    levels = RawOption()

    def __init__(self, name='', data=[], **kw):
        super().__init__('sankey', name, data, **kw)


class Funnel(PositionMixin, SymbolMixin, Series):
    min = RawOption()
    max = RawOption()
    minSize = RawOption()
    maxSize = RawOption()
    sort = RawOption(value_choices=['ascending', 'descending', 'none'])
    gap = RawOption()
    funnelAlign = RawOption(value_choices=['left', 'right', 'center'])

    def __init__(self, name='', data=[], **kw):
        super().__init__('funnel', name, data, **kw)


class Gauge(PositionMixin, SymbolMixin, Series):
    radius = RawOption()
    startAngle = RawOption()
    endAngle = RawOption()
    clockwise = RawOption()
    min = RawOption()
    max = RawOption()
    splitNumber = RawOption()

    axisLine = AxisLine()
    splitLine = SplitLine()
    axisTick = AxisTick()

    axisLineStyle = Delegator('axisLine', 'lineStyle')
    splitLineStyle = Delegator('splitLine', 'lineStyle')
    splitLineLength = Delegator('splitLine', 'lineLength')
    axisTickSplitNumber = Delegator('axisTick', 'splitNumber')
    axisTickStyle = Delegator('axisTick', 'lineStyle')
    axisTickLength = Delegator('axisTick', 'lineLength')

    axisLabel = Label()
    title = Label()
    detail = Label()

    def __init__(self, name='', data=[], **kw):
        super().__init__('gauge', name, data, **kw)


class PictorialBar(AnimationMixin, SymbolMixin, Bar):
    symbolPosition = RawOption(value_choices=['start', 'center', 'end'])
    symbolMargin = RawOption()
    symbolClip = RawOption()
    symbolBoundingData = RawOption()
    symbolPatternSize = RawOption()

    def __init__(self, name='', data=[], **kw):
        super().__init__('pictorialbar', name, data, **kw)


class ThemeRiver(PositionMixin, Series):
    singleAxisIndex = RawOption()

    def __init__(self, name='', data=[], **kw):
        super().__init__('themeRiver', name, data, **kw)


class Custom(Series):
    renderItem = RawOption()

    def __init__(self, name='', data=[], renderItem=None):
        if isins(renderItem, str):
            renderItem = JsCode(renderItem)
        super().__init__('custom', name, data, renderItem=renderItem)
