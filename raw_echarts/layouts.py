from raw_echarts.elements import *
from raw_echarts.axis import Axis, SplitLine


__all__ = ['Grid', 'Polar', 'LRadar', 'Calendar',
           'Single', 'Geo', 'Parallel', 'ParallelAxis']


class Grid(PositionMixin, StyleMixin, Option):
    containLabel = RawOption()

    tooltip = Tooltip()


class Polar(Option):
    center = RawOption()
    radius = RawOption()
    tooltip = Tooltip()


class RadarIndicator(Option):
    name = RawOption()
    max = RawOption()
    min = RawOption()
    color = RawOption()

    def __init__(self, name='', max=100, min=0, color=None, **kw):
        super().__init__(name=name, max=max, min=min, color=color, **kw)


class LRadar(Polar):
    name = TextStyle()
    indicator = RadarIndicator().to_array(False)

    def add_indicator(self, name='', max=100, min=0, color=None, **kw):
        self.indicator.append(RadarIndicator(name, max, min, color, **kw))


class CalendarLabel(TextStyle):
    firstDay = RawOption()
    position = RawOption(value_choices=['start', 'end'])
    nameMap = RawOption(value_choices=['cn', 'en'])
    formatter = RawOption()


class Calendar(PositionMixin, Option):
    range = RawOption()
    cellSize = RawOption()
    orient = RawOption(value_choices=['horizontal', 'vertical'])

    splitLine = SplitLine()
    itemStyle = ItemStyle()
    dayLabel = CalendarLabel()
    monthLabel = CalendarLabel()
    yearLabel = CalendarLabel()


class Single(Option):
    tooltip = Tooltip()


class GeoRegion(Option):
    name = RawOption()
    selected = RawOption()
    itemStyle = ItemStyle()
    label = Label()
    emphasis = Option(label=Label())


class Geo(PositionMixin, Option):
    map = RawOption()
    roam = RawOption(value_choices=['move', 'scale'])
    center = RawOption()
    aspectScale = RawOption()
    bounddingCoords = RawOption()
    zoom = RawOption()
    scaleLimit = RawOption()
    nameMap = RawOption()
    nameProperty = RawOption()
    selectMode = RawOption()
    layoutCenter = RawOption()
    layoutSize = RawOption()
    silent = RawOption()

    regions = GeoRegion().to_array(False)

    label = Label()
    itemStyle = ItemStyle()
    emphasis = Option(label=Label(), itemStyle=ItemStyle())

    def __init__(self, map=None, **kw):
        super().__init__(map=map, **kw)
        if map:
            MAPS.load_data()
            self.add_js_link(MAPS[map])


class ParallelAxis(Axis):
    paralleIndex = RawOption()
    dim = RawOption()
    areaSelectStyle = AreaStyle()


class Parallel(PositionMixin, Option):
    parallelAxisDefault = ParallelAxis()
    parallelAxisExpandable = RawOption()
    axisExpandCenter = RawOption()
    axisExpandCount = RawOption()
    axisExpandWidth = RawOption()
    axisExpandTriggerOn = RawOption()
