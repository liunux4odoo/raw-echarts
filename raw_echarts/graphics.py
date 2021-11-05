from raw_echarts.elements import *


class Graphic(PositionMixin, Option):
    type = RawOption(value_choices=['image', 'text', 'group', 'rect', 'sector',
                                    'ring', 'polygon', 'line', 'polyline', 'bezierCurve', 'arch'])
    action = RawOption(data_key='$action', value_choices=[
                       'remove', 'replace', 'merge'])
    shape = RawOption()

    style = ItemStyle()

    silent = RawOption()
    invisible = RawOption()
    bounding = RawOption(value_choices=['raw', 'all'])
    draggable = RawOption()

    origin = RawOption()
    scale = RawOption()
    rotation = RawOption()
    position = RawOption()
    cursor = RawOption()
    info = RawOption()
    ignore = RawOption()

    onclick = RawOption()
    onmousemove = RawOption()
    onmouseover = RawOption()
    onmouseout = RawOption()
    onmouseup = RawOption()
    onmousedown = RawOption()
    onmousewheel = RawOption()
    ondrag = RawOption()
    ondragstart = RawOption()
    ondragend = RawOption()
    ondragenter = RawOption()
    ondragleave = RawOption()
    ondragover = RawOption()
    ondrop = RawOption()


class GRect(Graphic):
    def __init__(self, x, y, width, height, r=None, **kw):
        kw.update({
            'type': 'rect',
            'shape': {
                    'x': x,
                'y': y,
                'width': width,
                'height': height,
                'r': r,
            }
        })
        super().__init__(**kw)


class GCircle(Graphic):
    def __init__(self, cx, cy, r, **kw):
        kw.update({
            'type': 'circle',
            'shape': {
                    'cx': cx,
                'cy': cy,
                'r': r,
            }
        })
        super().__init__(**kw)


class GRing(Graphic):
    def __init__(self, cx, cy, r, r0, **kw):
        kw.update({
            'type': 'ring',
            'shape': {
                    'cx': cx,
                'cy': cy,
                'r': r,
                'r0': r0,
            }
        })
        super().__init__(**kw)


class GArc(Graphic):
    def __init__(self, cx, cy, r, r0, startAngle, endAngle, clockwise=True, **kw):
        if isinstance(startAngle, (int, float)):
            startAngle = JsCode('Math.PI * {}'.format(startAngle/180))
        if isinstance(endAngle, (int, float)):
            endAngle = JsCode('Math.PI * {}'.format(endAngle/180))

        kw.update({
            'type': 'arc',
            'shape': {
                    'cx': cx,
                'cy': cy,
                'r': r,
                'r0': r0,
                'clockwise': clockwise,
                'startAngle': startAngle,
                'endAngle': endAngle,
            }
        })
        super().__init__(**kw)


class GSector(Graphic):
    pass


class GPolygon(Graphic):
    def __init__(self, *points, **kw):
        kw.update({
            'type': 'polygon',
            'shape': {
                    'points': points,
            }
        })
        super().__init__(**kw)


class GPolyline(Graphic):
    def __init__(self, *points, **kw):
        kw.update({
            'type': 'polyline',
            'shape': {
                    'points': points,
            }
        })
        super().__init__(**kw)


class GLine(Graphic):
    def __init__(self, x1, y1, x2, y2, percent=1, **kw):
        kw.update({
            'type': 'line',
            'shape': {
                    'x1': x1,
                'y1': y1,
                'x2': x2,
                'y2': y2,
                'percent': percent,
            }
        })
        super().__init__(**kw)


class GBezierCurve(Graphic):
    def __init__(self, x1, y1, x2, y2, cpx1, cpy1, cpx2=None, cpy2=None, percent=1, **kw):
        kw.update({
            'type': 'line',
            'shape': {
                    'x1': x1,
                'y1': y1,
                'x2': x2,
                'y2': y2,
                'cpx1': cpx1,
                'cpy1': cpy1,
                'cpx2': cpx2,
                'cpy2': cpy2,
                'percent': percent,
            }
        })
        super().__init__(**kw)


class GImage(Graphic):
    def __init__(self, image, x, y, width, height, **kw):
        kw.update({
            'type': 'image',
            'shape': {
                    'image': image,
                'x': x,
                'y': y,
                'width': width,
                'height': height,
            }
        })
        super().__init__(**kw)


class GTextStyle(ItemStyle):
    text = RawOption()
    x = RawOption()
    y = RawOption()
    font = RawOption()
    textAlign = RawOption(value_choices=['left', 'center', 'right'])
    textVerticalAlign = RawOption(value_choices=['top', 'middle', 'bottom'])


class GText(Graphic):
    style = GTextStyle()

    def __init__(self, text, x, y, **kw):
        kw.update({
            'type': 'text',
            'shape': {
                    'text': text,
                'x': x,
                'y': y,
            }
        })
        super().__init__(**kw)


class GGroup(Graphic):
    children = RawOption([])
    progressive = RawOption()
    diffChildrenByName = RawOption()

    def __init__(self, *children, **kw):
        if children:
            self.children = list(children)

        kw.update({
            'type': 'group',
            'children': self.children
        })
        super().__init__(**kw)
