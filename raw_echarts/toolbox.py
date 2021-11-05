from raw_echarts.elements import *


__all__ = ['Toolbox']


class FeatureItemMixin:
    title = RawOption()
    icon = RawOption()
    iconStyle = ItemStyle()
    emphasis = Option(iconStyle=ItemStyle())


class Mark(FeatureItemMixin, Option):
    pass


class DataView(FeatureItemMixin, Option):
    readOnly = RawOption()
    optionToContent = RawOption()
    contentToOption = RawOption()
    lang = RawOption([])

    backgroundColor = RawOption()
    textareaColor = RawOption()
    textareaBorderColor = RawOption()
    textColor = RawOption()
    buttonColor = RawOption()
    buttonTextColor = RawOption()


class MagicType(FeatureItemMixin, Option):
    pass


class Restore(FeatureItemMixin, Option):
    pass


class SaveImage(FeatureItemMixin, Option):
    type = RawOption(value_choices=['png', 'jpeg', 'svg'])
    name = RawOption()
    backgroundColor = RawOption()
    connectedBackgroundColor = RawOption()
    excludeComponents = RawOption([])


class MagicType(Option):
    type = RawOption()
    title = Option()
    icon = Option()


class DataZoom(FeatureItemMixin, Option):
    filterMode = RawOption(
        value_choices=['filter', 'weakFilter', 'empty', 'none'])
    xAxisIndex = RawOption([])
    yAxisIndex = RawOption([])
    magicType = MagicType()
    option = Option()
    seriesIndex = Option()


class Brush(FeatureItemMixin, Option):
    type = RawOption()
    geoIndex = RawOption()
    xAxisIndex = RawOption()
    yAxisIndex = RawOption()
    brushLink = RawOption([])
    throttleType = RawOption(value_choices=['debounce', 'fixRate'])
    throttleDelay = RawOption()


class Feature(Option):
    mark = Mark()
    dataView = DataView()
    magicType = MagicType()
    restore = Restore()
    saveAsImage = SaveImage()
    dataZoom = DataZoom()


class Toolbox(PositionMixin, Option):
    orient = RawOption(value_choices=['horizontal', 'vertical'])
    itemSize = RawOption()
    itemGap = RawOption()
    showTitle = RawOption()

    feature = Feature()
    mark = Delegator('feature', 'mark')

    iconStyle = ItemStyle()
    emphasis = Option(iconStyle=ItemStyle())

    tooltip = Tooltip()

    def add_custom(self, name, title, icon, js, show=True):
        self.feature.add({
            'name': name,
            'title': title or name,
            'icon': icon,
            'onclick': JsCode(js),
            'show': show,
        })
        return self


if __name__ == '__main__':
    t = Toolbox()
