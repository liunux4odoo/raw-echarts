from raw_echarts.bases import *


class AnimationMixin:
    animation = RawOption(
        __doc__='True or False, whether enable chart animation.')
    animationThreshold = RawOption(
        __doc__='number, disable animation when elements count of series are more than threshold.')
    animationDuration = RawOption(
        __doc__='number, duration of animation, could be function(idx) where idx is data index.')
    animationEasing = RawOption()
    animationDelay = RawOption()
    animationDelayUpdate = RawOption()
    animationEasingUpdate = RawOption()
    animationDurationUpdate = RawOption()

    blendMode = RawOption(value_choices=['source-over', 'lighter'])
    hoverLayerThreshold = RawOption()
    useUTC = RawOption()

    # pie
    animationType = RawOption(value_choices=['expansion', 'scale'])
    animationTypeUpdate = RawOption()


class Animation(AnimationMixin, Option):
    pass


class PositionMixin:
    x = RawOption()
    y = RawOption()
    left = RawOption()
    right = RawOption()
    top = RawOption()
    bottom = RawOption()
    width = RawOption()
    height = RawOption()


class ColorMixin:
    color = RawOption()
    colorAlpha = RawOption()
    colorSaturation = RawOption()


class ShadowMixin:
    color = RawOption()
    shadowColor = RawOption()
    shadowOffsetX = RawOption()
    shadowOffsetY = RawOption()
    shadowBlur = RawOption()
    opacity = RawOption()


class StyleMixin(ShadowMixin):
    backgroundColor = RawOption()
    borderWidth = RawOption()
    borderColor = RawOption()
    borderRadius = RawOption()

    bgcolor = backgroundColor


class SymbolMixin:
    symbol = RawOption(value_choices=['circle', 'rect', 'roundRect', 'triangle',
                                      'diamond', 'pin', 'arrow', 'emptyCircle',
                                      'none'])
    symbolSize = RawOption()
    symbolRotate = RawOption()
    symbolKeepAspect = RawOption()
    symbolOffset = RawOption()
    showSymbol = RawOption()
    showAllSymbol = RawOption()


class ShadowStyle(ShadowMixin, Option):
    pass


class TextStyle(StyleMixin, Option):
    color = RawOption()
    fontFamily = RawOption(
        value_choices=['sans-serif', 'serif', 'monospace', 'Aria', 'Microsoft YaHei'])
    fontSize = RawOption()
    fontStyle = RawOption(value_choices=['normal', 'italic', 'oblique'])
    fontWeight = RawOption(
        value_choices=['normal', 'bold', 'bolder', 'lighter'])

    textBorderColor = RawOption()
    textBorderWidth = RawOption()
    textShadowColor = RawOption()
    textShadowBlur = RawOption()
    textShadowOffsetX = RawOption()
    textShadowOffsetY = RawOption()

    lineHeight = RawOption()
    width = RawOption()
    height = RawOption()

    align = RawOption(value_choices=['left', 'center', 'right'])
    verticalAlign = RawOption(value_choices=['top', 'middle', 'bottom'])

    padding = RawOption()
    margin = RawOption()


class LineStyle(StyleMixin, Option):
    type = RawOption(value_choices=['solid', 'dashed', 'dotted'])
    width = RawOption()
    curveness = RawOption()


class AreaStyle(StyleMixin, Option):
    pass


class ItemStyle(StyleMixin, Option):
    borderType = RawOption(value_choices=['solid', 'dashed', 'dotted'])
    stroke = RawOption()
    fill = RawOption()
    lineWidth = RawOption()

    # geo
    areaColor = RawOption()

    # candlestick
    color0 = RawOption()
    borderColor0 = RawOption()


class Label(Option):
    show = RawOption()
    position = RawOption(value_choices=['start', 'middle', 'end',
                                        'insideStartTop', 'insideStartBottom',
                                        'insideMiddleTop', 'insideMiddleBottom',
                                        'insideEndTop', 'insideEndBottom'])
    offset = RawOption()
    margin = RawOption()
    formatter = RawOption()
    ellipsis = RawOption()

    textStyle = TextStyle()
    style = textStyle

    rich = TextStyle()

    # use in axis label
    precision = RawOption()


class Emphasis(Option):
    label = Label()
    itemStyle = ItemStyle()
    lineStyle = LineStyle()


class SymbolMixin:
    symbol = RawOption()
    symbolSize = RawOption()
    symbolRotate = RawOption()
    symbolKeepAspect = RawOption()
    symbolOffset = RawOption()

    label = Label()
    itemStyle = ItemStyle()
    lineStyle = LineStyle()

    silent = RawOption()
    emphasis = Emphasis()


class MarkPointData(SymbolMixin, Option):
    name = RawOption()
    type = RawOption(value_choices=['max', 'min', 'average'])
    valueIndex = RawOption()
    valueDim = RawOption()
    value = RawOption()

    x = RawOption()
    y = RawOption()
    coord = RawOption()

    itemStyle = ItemStyle()


class MarkPoint(SymbolMixin, AnimationMixin, Option):
    data = MarkPointData().to_array(False)


class MarkLine(SymbolMixin, AnimationMixin, Option):
    precision = RawOption()
    data = RawOption()


class MarkArea(SymbolMixin, AnimationMixin, Option):
    data = RawOption()


class Handle(ShadowMixin, Option):
    icon = RawOption()
    size = RawOption()
    margin = RawOption()
    throttle = RawOption()


class AxisPointer(AnimationMixin, Option):
    type = RawOption(value_choices=['line', 'shadow', 'cross', 'none'])
    triggerOn = RawOption()
    axis = RawOption(value_choices=['auto', 'x', 'y', 'radius', 'angle'])
    snap = RawOption()
    triggerTooltip = RawOption()
    value = RawOption()
    status = RawOption()
    link = RawOption()  # todo: link mapper in different axis types
    label = Label()

    lineStyle = LineStyle()
    shadowStyle = ShadowStyle()
    crossStyle = LineStyle()


class Tooltip(StyleMixin, Option):
    trigger = RawOption(value_choices=['axis', 'item', 'none'])
    axisPointer = AxisPointer()
    showContent = RawOption()
    alwaysShowContent = RawOption()
    triggerOn = RawOption(
        value_choices=['mousemove', 'click', 'mousemove|click', 'none'])
    showDelay = RawOption()
    hideDelay = RawOption()
    enterable = RawOption()
    renderMode = RawOption(value_choices=['html', 'richText'])
    confine = RawOption()
    appendToBody = RawOption()
    transitionDuration = RawOption()
    padding = RawOption()
    position = RawOption(
        value_choices=['inside', 'top', 'bottom', 'left', 'right'])
    formatter = RawOption()

    textStyle = TextStyle()
    style = textStyle

    extraCssText = RawOption()


class Dimension(Option):
    name = RawOption()
    type = RawOption(
        value_choices=['number', 'ordinal', 'float', 'int', 'time'])
    displayName = RawOption()

    def __init__(self, name=None, **kw):
        super().__init__(name=name, **kw)


class Encode(Option):
    x = RawOption()
    y = RawOption()
    single = RawOption()
    radius = RawOption()
    angle = RawOption()
    lng = RawOption()
    lat = RawOption()

    tooltip = RawOption()
    seriesName = RawOption()

    itemId = RawOption()
    itemName = RawOption()


class DataSet(Option):
    source = RawOption()
    dimensions = RawOption([])
    sourceHeader = RawOption()


class AriaSeperator(Option):
    middle = RawOption()
    end = RawOption()


class AriaItem(Option):
    prefix = RawOption()
    withName = RawOption()
    withoutName = RawOption()

    # multiple series and data
    seperator = AriaSeperator()

    # data
    allData = RawOption()
    partialData = RawOption()


class Aria(Option):
    description = RawOption()

    withTitle = RawOption()
    withoutTitle = RawOption()

    series = Option(maxCount=RawOption(),
                    single=AriaItem(), multiple=AriaItem())
    data = AriaItem(maxCount=RawOption())
