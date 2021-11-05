from raw_echarts.elements import *
from raw_echarts.mapdata import *
from raw_echarts.axis3D import *


class Series3D(Option):
    type = RawOption()
    name = RawOption()
    coordinateSystem = RawOption(
        value_choices=['cartesian3D', 'globe', 'geo3D'])
    grid3DIndex = RawOption()
    globeIndex = RawOption()
    geo3DIndex = RawOption()

    symbol = RawOption()
    symbolSize = RawOption()

    label = Label()
    itemStyle = ItemStyle()
    emphasis = Emphasis()

    data = RawOption([])

    blendMode = RawOption(value_choices=['source-over', 'lighter'])
    silent = RawOption()

    animation = RawOption()
    animationDurationUpdate = RawOption()
    animationEasingUpdate = RawOption()

    progressive = RawOption()
    progressiveThreshold = RawOption()

    def __init__(self, type, name='', data=[], **kw):
        super().__init__(type=type, name=name, data=data, **kw)
        self._js_dependences = ['echarts.min.js', 'echarts-gl.min.js']

    def add_js_link(self, js_link):
        if js_link not in self._js_dependences:
            self._js_dependences.append(js_link)
        return self


class Scatter3D(Series3D):
    def __init__(self, name='', data=[], **kw):
        super().__init__('scatter3D', name, data, **kw)


class Line3D(Series3D):
    def __init__(self, name='', data=[], **kw):
        super().__init__('line3D', name, data, **kw)


class Bar3D(Series3D):
    bevelLevel = RawOption()
    bevelSmoothness = RawOption()
    stack = RawOption()
    minHeight = RawOption()

    shading = RawOption(value_choices=['color', 'lambert', 'realistic'])
    realisticMaterial = RealisticMaterial()
    lambertMaterial = Material()
    colorMaterial = Material()

    def __init__(self, name='', data=[], **kw):
        super().__init__('bar3D', name, data, **kw)


class Map3D(PositionMixin, ShadingMixin, Option):
    map = RawOption()
    boxWidth = RawOption()
    boxHeight = RawOption()
    boxDepth = RawOption()
    regionHeight = RawOption()

    groundPlane = GroundPlane()

    instancing = RawOption()
    label = Label()
    itemStyle = ItemStyle()
    emphasis = Emphasis()

    data = RawOption([])

    def __init__(self, map='china', name='', data=[], **kw):
        new_data = _parse_data_pair(data, columns=['name', 'value', 'label'])
        super().__init__('map3D', name, new_data, map=map, **kw)
        MAPS.load_data()
        self.add_js_link(MAPS[map])


class Lines3DEffect(SymbolMixin, Option):
    period = RawOption()
    constantSpeed = RawOption()
    trailLength = RawOption()
    trailWidth = RawOption()
    trailColor = RawOption()
    trailOpacity = RawOption()


class Lines3D(Series3D):
    polyline = RawOption()
    effect = Lines3DEffect()

    def __init__(self, name='', data=[], **kw):
        super().__init__('lines3D', name, data, **kw)


class WireFrame(Option):
    lineStyle = Option()

    color = Delegator('lineStyle', 'color')
    width = Delegator('lineStyle', 'width')
    opacity = Delegator('lineStyle', 'opacity')


class Surface(ShadingMixin, Series3D):
    parametric = RawOption()
    equation = RawOption()
    parametricEquation = RawOption()
    wireframe = WireFrame()

    def __init__(self, name='', data=[], **kw):
        super().__init__('surface', name, data, **kw)


class Polygons3D(ShadingMixin, Series3D):
    multiPolygon = RawOption()

    def __init__(self, name='', data=[], **kw):
        super().__init__('polygons3D', name, data, **kw)


class ScatterGL(ShadingMixin, Series3D):
    def __init__(self, name='', data=[], **kw):
        super().__init__('scatterGL', name, data, **kw)


class ForceAtlas(Option):
    GPU = RawOption()
    steps = RawOption()
    stopThreshold = RawOption()
    barnesHutOptimize = RawOption()
    repulsionByDegree = RawOption()
    linLogMode = RawOption()
    gravity = RawOption()
    gravityCenter = RawOption()
    scaling = RawOption()
    edgeWeightInfluence = RawOption()
    edgeWeight = RawOption()
    nodeWeight = RawOption()
    preventOverlap = RawOption()


class GraphLink(Option):
    source = RawOption()
    target = RawOption()
    value = RawOption()
    lineStyle = LineStyle()


class GraphGL(ShadingMixin, Series3D):
    layout = RawOption(value_choices=['forceAtlas2'])
    forceAtlas2 = ForceAtlas()
    data = RawOption([])
    nodes = data
    links = GraphLink().to_array(False)
    edges = links

    def __init__(self, name='', data=[], **kw):
        super().__init__('graphGL', name, data, **kw)


class FlowGL(ShadingMixin, Series3D):
    particleDensity = RawOption()
    particleType = RawOption(value_choices=['point', 'line'])
    particleSize = RawOption()
    particleSpeed = RawOption()
    particleTrail = RawOption()
    supersampling = RawOption()
    gridWidth = RawOption()
    gridHeight = RawOption()

    def __init__(self, name='', data=[], **kw):
        super().__init__('flowGL', name, data, **kw)
