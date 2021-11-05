from raw_echarts.elements import *


class AxisLine(Option):
    onZero = RawOption()
    onZeroAxisIndex = RawOption()
    symbol = RawOption(value_choices=['none', 'arrow'])
    symbolSize = RawOption()
    symbolOffset = RawOption()
    lineStyle = LineStyle()

    style = lineStyle


class AxisTick(Option):
    alignWithLabel = RawOption()
    interval = RawOption()
    inside = RawOption()
    length = RawOption()
    lineStyle = LineStyle()


class MinorTick(Option):
    splitNumber = RawOption()
    length = RawOption()


class AxisLabel(Label):
    interval = RawOption()
    inside = RawOption()
    rotate = RawOption()
    margin = RawOption()
    showMinLabel = RawOption()
    showMaxLabel = RawOption()


class SplitLine(Option):
    interval = RawOption()
    lineStyle = LineStyle()


SplitLine.delegate('lineStyle')


class SplitArea(Option):
    interval = RawOption()
    areaStyle = AreaStyle()


SplitArea.delegate('areaStyle')


class Axis(Option):
    gridIndex = RawOption()
    position = RawOption(value_choices=['top', 'bottom'])
    type = RawOption(value_choices=['category', 'value', 'time', 'log'])
    offset = RawOption()

    name = RawOption()
    nameLocation = RawOption(
        value_choices=['start', 'center', 'middle', 'end'])
    nameGap = RawOption()
    nameRotate = RawOption()
    nameTextStyle = TextStyle()
    style = nameTextStyle

    min = RawOption(value_choices=['dataMin'])
    max = RawOption(value_choices=['dataMax'])
    scale = RawOption()
    inverse = RawOption()
    splitNumber = RawOption()
    interval = RawOption()
    minInterval = RawOption()
    maxInterval = RawOption()
    boundaryGap = RawOption()
    data = RawOption([])

    logBase = RawOption()
    silent = RawOption()
    triggerEvent = RawOption()

    axisLabel = RawOption()
    axisLine = AxisLine()
    axisPointer = AxisPointer()
    axisTick = AxisTick()

    splitLine = SplitLine()
    minorSplitLine = LineStyle()
    splitArea = SplitArea()


class RadiusAxis(Axis):
    polarIndex = RawOption()


class AngleAxis(RadiusAxis):
    startAngle = RawOption()
    clockwise = RawOption()


class SingleAxis(Axis):
    orient = RawOption(value_choices=['horizontal', 'vertical'])
    tooltip = Tooltip()
