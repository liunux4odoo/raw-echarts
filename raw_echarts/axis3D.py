from raw_echarts.elements import *
from raw_echarts.axis import AxisLine, AxisLabel, AxisTick, SplitLine, SplitArea


class Material(Option):
    detailTexture = RawOption()
    textureTiling = RawOption()
    textureOffset = RawOption()


class RealisticMaterial(Material):
    normalTexture = RawOption()

    roughness = RawOption()
    metalness = RawOption()
    roughnessAdjust = RawOption()
    metalnessAdjust = RawOption()


class MainLight(Option):
    color = RawOption()
    intensity = RawOption()
    shadow = RawOption()
    shadowQuality = RawOption()
    alpha = RawOption()
    beta = RawOption()
    time = RawOption()


class AmbientLight(Option):
    color = RawOption()
    intensity = RawOption()


class AmbientCubemap(Option):
    texture = RawOption()
    diffuseIntensity = RawOption()
    specularIntensity = RawOption()


class Light(Option):
    main = MainLight()
    ambient = AmbientLight()
    ambientCubemap = AmbientCubemap()


class PostEffectBloom(Option):
    enable = RawOption()
    bloomIntensity = RawOption()

    def opts(self, intensity=None, enable=True):
        return super().opts(bloomIntensity=intensity, enable=enable)


class PostEffectDepthOfField(Option):
    enable = RawOption()
    focalDistance = RawOption()
    focalRange = RawOption()
    fstop = RawOption()
    blurRadius = RawOption()


class PostEffectSSAO(Option):
    enable = RawOption()
    quality = RawOption()
    radius = RawOption()
    intensity = RawOption()


class PostEffectColorCorrction(Option):
    enable = RawOption()
    lookupTexture = RawOption()
    exposure = RawOption()
    brightness = RawOption()
    contrast = RawOption()
    saturation = RawOption()


class PostEffect(Option):
    enable = RawOption()
    bloom = PostEffectBloom()
    depthOfField = PostEffectDepthOfField()
    screenSpaceAmbientOcclusion = PostEffectSSAO()
    SSAO = screenSpaceAmbientOcclusion
    colorCorrectoin = PostEffectColorCorrction()

    # todo:
    FXAA = RawOption()
    temporalSuperSampling = RawOption()


class ViewControl(Option):
    projection = RawOption(value_choices=['perspective', 'orthographic'])
    autoRotate = RawOption()
    autoRotateDirection = RawOption(value_choices=['cw', 'ccw'])
    autoRotateSpeed = RawOption()
    autoRotateAfterStill = RawOption()
    damping = RawOption()
    rotateSensitivity = RawOption()
    zoomSensitivity = RawOption()
    panSensitivity = RawOption()
    panMouseButton = RawOption(value_choices=['left', 'middle', 'right'])
    rotateMouseButton = RawOption(value_choices=['left', 'middle', 'right'])
    distance = RawOption()
    minDistance = RawOption()
    maxDistance = RawOption()
    orthographicSize = RawOption()
    minOrthographicSize = RawOption()
    maxOrthographicSize = RawOption()
    alpha = RawOption()
    beta = RawOption()
    minAlpha = RawOption()
    maxAlpha = RawOption()
    minBeta = RawOption()
    maxBeta = RawOption()
    center = RawOption()

    animation = RawOption()
    animationDurationUpdate = RawOption()
    animationEasingUpdate = RawOption()

    targetCoord = RawOption()


class ShadingMixin:
    environment = RawOption()
    shading = RawOption(value_choices=['color', 'lambert', 'realistic'])
    realisticMaterial = RealisticMaterial()
    lambertMaterial = Material()
    colorMaterial = Material()

    light = Light()
    postEffect = PostEffect()
    viewControl = ViewControl()


class GlobeLayer(Option):
    type = RawOption(value_choices=['overlay', 'blend'])
    name = RawOption()
    blendTo = RawOption(value_choices=['albedo', 'emission'])
    intensity = RawOption()
    shading = RawOption(value_choices=['color', 'lambert', 'realistic'])
    distance = RawOption()
    texture = RawOption()


class Globe(PositionMixin, ShadingMixin, Option):
    globeRadius = RawOption()
    globeOuterRadius = RawOption()

    baseTexture = RawOption()
    heightTexture = RawOption()
    displacementTexture = RawOption()
    displacementScale = RawOption()
    displacementQuality = RawOption(
        value_choices=['low', 'medium', 'high', 'ultra'])

    layers = GlobeLayer().to_array(False)


class GroundPlane(Option):
    show = RawOption()
    color = RawOption()


class Geo3DRedgion(Option):
    name = RawOption()
    regionHeight = RawOption()
    label = Label()
    itemStyle = ItemStyle()
    emphasis = Emphasis()


class Geo3D(PositionMixin, ShadingMixin, Option):
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

    regions = Geo3DRedgion().to_array(False)


class Mapbox3D(Option):
    pass


class Grid3D(ShadingMixin, PositionMixin, Option):
    boxWidth = RawOption()
    boxHeight = RawOption()
    boxDepth = RawOption()

    axisLine = AxisLine()
    axisLabel = AxisLabel()
    axisTick = AxisTick()
    splitLine = SplitLine()
    splitArea = SplitArea()
    axisPointer = AxisPointer()


class Axis3D(Option):
    name = RawOption()
    grid3DIndex = RawOption()
    nameTextStyle = TextStyle()
    nameGap = RawOption()
    type = RawOption(value_choices=['value', 'category', 'time', 'log'])

    min = RawOption(value_choices=['dataMin'])
    max = RawOption(value_choices=['dataMax'])
    scale = RawOption()
    interval = RawOption()
    minInterval = RawOption()
    data = RawOption([])

    splitNumber = RawOption()

    logBase = RawOption()

    axisLabel = RawOption()
    axisLine = AxisLine()
    axisPointer = AxisPointer()

    splitLine = SplitLine()
    splitArea = SplitArea()
