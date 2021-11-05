from raw_echarts.elements import *
from raw_echarts.charts import *


__all__ = ['TimelineChart']


class CheckpointStyle(StyleMixin, Option):
    symbol = RawOption(value_choices=[
        'circle', 'rect', 'roundRect', 'triangle', 'diamond', 'pin', 'arrow', 'none'])
    symbolSize = RawOption()
    symbolRotate = RawOption()
    symbolKeepAspect = RawOption()
    symbolOffset = RawOption()

    animation = RawOption()
    animationDuration = RawOption()
    animationEasing = RawOption()


class ControlStyle(StyleMixin, Option):
    showPlayBtn = RawOption()
    showPrevBtn = RawOption()
    showNextBtn = RawOption()
    itemSize = RawOption()
    itemGap = RawOption()
    position = RawOption(value_choices=['left', 'right', 'top', 'bottom'])
    playIcon = RawOption()
    prevIcon = RawOption()
    nextIcon = RawOption()


class Timeline(PositionMixin, SymbolMixin, Option):
    type = RawOption(value_choices=['slider'])
    orient = RawOption(value_choices=['horizontal', 'vertical'])
    inverse = RawOption()

    lineStyle = LineStyle()
    label = Label()
    itemStyle = ItemStyle()
    checkpointStyle = CheckpointStyle()
    axisType = RawOption(value_choices=['category', 'value', 'time'])
    currentIndex = RawOption()
    autoPlay = RawOption()
    rewind = RawOption()
    loop = RawOption()
    playInterval = RawOption()
    realtime = RawOption()
    controlPosition = RawOption(value_choices=['right', 'left'])
    controlStyle = ControlStyle()

    emphasis = Option(label=Label(), itemStyle=ItemStyle())

    data = RawOption([])


class TimelineSeriesData(RawOption):
    def __init__(self, data=[]):
        super().__init__([])
        for d in data:
            self.append(d)

    def __getitem__(self, idx):
        return self._data[idx]['data']

    def __setitem__(self, idx, val):
        if isinstance(val, list):
            val = {'data': val}
        self._data[idx] = val

    def append(self, val):
        if isinstance(val, list):
            val = {'data': val}
        self._data.append(val)
        return self


class BaseOption(Root):
    timeline = Timeline()


class SeriesOption(Option):
    title = Title()
    series = TimelineSeriesData()


class TimelineChart(Chart):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._option.add_param('baseOption', BaseOption())
        self._option.add_param('options', SeriesOption().to_array(False))
        self._option.options.use()
        self.timeline.data = []

    def __getattr__(self, attr):
        if hasattr(self._option.baseOption, attr):
            return getattr(self._option.baseOption, attr)
        raise AttributeError(f'"{self}" object has no attribute: "{attr}"')

    def opts(self, d={}, **kw):
        self._option.baseOption.opts(d, **kw)
        return self

    def add_page(self, data='', title=None, series_data=[]):
        if isinstance(title, str):
            title = {'text': title}
        self._option.options.add(
            dict(title=title, series=TimelineSeriesData(series_data)))
        self._option.baseOption.timeline.data.append(data)
        return self

    @property
    def pages(self):
        return self._option.options


if __name__ == '__main__':
    c = TimelineChart()
    c.title(text='a', sub='x', style=TextStyle(size=8))
    c.radar(indicator=[
        {'name': 'axis 1', 'max': 10},
        {'name': 'axis 2', 'max': 10},
        {'name': 'axis 3', 'max': 10},
        {'name': 'axis 4', 'max': 10},
        {'name': 'axis 5', 'max': 10},
    ])
    p = Radar('radar', [
        {
            'name': 'person 1',
            'value': [1, 2, 3, 4, 5],
        },
        {
            'name': 'person 2',
            'value': [5, 4, 3, 2, 1]
        }
    ])
    c.add_chart(p)
    c.add_page('page 1', 'page1', [[
        {'name': 'p1', 'value': [2, 2, 2, 2, 2]},
        {'name': 'p2', 'value': [3, 3, 3, 3, 3]}]])
    c.add_page('page 2', 'page2', [[
        {'name': 'p1', 'value': [3, 3, 3, 3, 3]},
        {'name': 'p2', 'value': [2, 2, 2, 2, 2]}]])

    print(c.get_option())
