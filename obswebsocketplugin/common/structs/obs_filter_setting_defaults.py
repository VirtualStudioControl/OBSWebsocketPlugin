from typing import Dict

VALUE_DESCRIPTORS: Dict[str, dict] = {}

VALUE_TYPE_NONE = 0
VALUE_TYPE_FLOAT = 1
VALUE_TYPE_INT = 2
VALUE_TYPE_COLOR = 3
VALUE_TYPE_BOOLEAN = 4
VALUE_TYPE_STRING = 5
VALUE_TYPE_ENUM = 6


# Colors are in ABGR

FILTER_TYPE_AV_COMPRESSOR = 'compressor_filter'
FILTER_TYPE_AV_EXPANDER = 'expander_filter'
FILTER_TYPE_AV_GAIN = 'gain_filter'
FILTER_TYPE_AV_INVERT_POLARITY = 'invert_polarity_filter'
FILTER_TYPE_AV_LIMITER = 'limiter_filter'
FILTER_TYPE_AV_NOISE_GATE = 'noise_gate_filter'
FILTER_TYPE_AV_NOISE_SUPPRESS = 'noise_suppress_filter_v2'
FILTER_TYPE_AV_ASYNC_DELAY = 'async_delay_filter'

FILTER_TYPE_EFFECT_LUT = 'clut_filter'
FILTER_TYPE_EFFECT_CHROMAKEY = 'chroma_key_filter'
FILTER_TYPE_EFFECT_COLOR_CORRECT = 'color_filter'
FILTER_TYPE_EFFECT_COLORKEY = 'color_key_filter'
FILTER_TYPE_EFFECT_CROP = 'crop_filter'
FILTER_TYPE_EFFECT_MASK = 'mask_filter'
FILTER_TYPE_EFFECT_LUMA_KEY = 'luma_key_filter'
FILTER_TYPE_EFFECT_GPU_DELAY = 'gpu_delay'
FILTER_TYPE_EFFECT_SCALE = 'scale_filter'
FILTER_TYPE_EFFECT_SCROLL = 'scroll_filter'
FILTER_TYPE_EFFECT_SHARPNESS = 'sharpness_filter'
FILTER_TYPE_EFFECT_VIRTUALCAM = 'virtualcam-filter'

VALUE_DESC_MIN = "min"
VALUE_DESC_MAX = "max"
VALUE_DESC_DEFAULT = "default"
VALUE_DESC_TYPE = "type"
VALUE_DESC_UNIT = "unit"
VALUE_DESC_ALLOWED = "allowed"
VALUE_DESC_SPECIAL = "specialFlags"

VALUE_UNIT_NONE = ""
VALUE_UNIT_MS = " ms"
VALUE_UNIT_DB = " dB"
VALUE_UNIT_RATBYONE = ":1"

FLAG_SPECIALS_NONE = 0
FLAG_SPECIALS_SRCLIST = 1<<0
FLAG_SPECIALS_EDITABLE = 1<<1

def registerValueDescriptor(filterType, valueName, min=None, max=None, default=None, unit=None, type=None, allowed=None, specials=0):
    settings = {}

    if min is None:
        min = -2**32-1

    if max is None:
        max = 2**32-1

    settings[VALUE_DESC_MIN] = min
    settings[VALUE_DESC_MAX] = max
    settings[VALUE_DESC_DEFAULT] = default
    settings[VALUE_DESC_UNIT] = unit
    settings[VALUE_DESC_TYPE] = type
    settings[VALUE_DESC_ALLOWED] = allowed
    settings[VALUE_DESC_SPECIAL] = specials

    if filterType not in VALUE_DESCRIPTORS:
        VALUE_DESCRIPTORS[filterType] = {}

    VALUE_DESCRIPTORS[filterType][valueName] = settings


# region A/V Filters
#region Compressor
registerValueDescriptor('compressor_filter', 'attack_time', type=VALUE_TYPE_INT, unit=VALUE_UNIT_MS, default=6, min=1, max=500)
registerValueDescriptor('compressor_filter', 'output_gain', type=VALUE_TYPE_FLOAT, unit=VALUE_UNIT_DB, default=0.0, min=-32.0, max=32.0)
registerValueDescriptor('compressor_filter', 'ratio', type=VALUE_TYPE_FLOAT, unit=VALUE_UNIT_RATBYONE, default=10.0, min=1.0, max=32.0)
registerValueDescriptor('compressor_filter', 'release_time', type=VALUE_TYPE_INT, unit=VALUE_UNIT_MS, default=60, min=1, max=1000, allowed=None, specials=FLAG_SPECIALS_NONE)
registerValueDescriptor('compressor_filter', 'sidechain_source', type=VALUE_TYPE_ENUM, default='none', allowed=['none'], specials=FLAG_SPECIALS_SRCLIST)
registerValueDescriptor('compressor_filter', 'threshold', type=VALUE_TYPE_FLOAT, unit=VALUE_UNIT_DB, default=-18.0, min=-60.0, max=0.0)
#endregion

#region Expander
registerValueDescriptor('expander_filter', 'attack_time', type=VALUE_TYPE_FLOAT, unit=VALUE_UNIT_MS, default=10, min=1, max=100)
registerValueDescriptor('expander_filter', 'detector', type=VALUE_TYPE_ENUM, default='RMS', allowed=['RMS', 'peak'])
registerValueDescriptor('expander_filter', 'output_gain', type=VALUE_TYPE_FLOAT, unit=VALUE_UNIT_DB, default=0.0, min=-32.0, max=32.0)
registerValueDescriptor('expander_filter', 'presets', type=VALUE_TYPE_ENUM, default='expander', allowed=['expander', 'gate'])
registerValueDescriptor('expander_filter', 'ratio', type=VALUE_TYPE_FLOAT, unit=VALUE_UNIT_RATBYONE, default=2.0, min=1.0, max=20.0)
registerValueDescriptor('expander_filter', 'release_time', type=VALUE_TYPE_INT, unit=VALUE_UNIT_MS, default=50, min=1, max=1000)
registerValueDescriptor('expander_filter', 'threshold', type=VALUE_TYPE_FLOAT, unit=VALUE_UNIT_DB, default=-40.0, min=-60.0, max=0.0)
#endregion

#region Gain
registerValueDescriptor('gain_filter', 'db', type=VALUE_TYPE_FLOAT, unit=VALUE_UNIT_DB, default=0.0, min=-30.0, max=30.0)
#endregion

#region Invert Polarity
registerValueDescriptor('invert_polarity_filter', 'none', type=VALUE_TYPE_NONE)
#endregion

#region Limiter Filter
registerValueDescriptor('limiter_filter', 'release_time', type=VALUE_TYPE_INT, unit=VALUE_UNIT_MS, default=60, min=1, max=1000)
registerValueDescriptor('limiter_filter', 'threshold', type=VALUE_TYPE_FLOAT, unit=VALUE_UNIT_DB, default=-6.0, min=-60.0, max=0.0)
#endregion

#region Noise Gate
registerValueDescriptor('noise_gate_filter', 'close_threshold', type=VALUE_TYPE_FLOAT, unit=VALUE_UNIT_DB, default=-32.0, min=-96.0, max=0.0)
registerValueDescriptor('noise_gate_filter', 'open_threshold', type=VALUE_TYPE_FLOAT, unit=VALUE_UNIT_DB, default=-26.0, min=-96.0, max=0.0)

registerValueDescriptor('noise_gate_filter', 'attack_time', type=VALUE_TYPE_INT, unit=VALUE_UNIT_MS, default=25, min=0, max=10000)
registerValueDescriptor('noise_gate_filter', 'hold_time', type=VALUE_TYPE_INT, unit=VALUE_UNIT_MS, default=200, min=0, max=10000)
registerValueDescriptor('noise_gate_filter', 'release_time', type=VALUE_TYPE_INT, unit=VALUE_UNIT_MS, default=150, min=0, max=10000)
#endregion

#region Noise Supress
registerValueDescriptor('noise_suppress_filter_v2', 'method', type=VALUE_TYPE_ENUM, default='rnnoise', allowed=['rnnoise', 'speex', 'nvafx'], specials=FLAG_SPECIALS_EDITABLE)
registerValueDescriptor('noise_suppress_filter_v2', 'suppress_level', type=VALUE_TYPE_FLOAT, unit=VALUE_UNIT_DB, default=-30.0, min=-60.0, max=0.0)
registerValueDescriptor('noise_suppress_filter_v2', 'intensity', type=VALUE_TYPE_FLOAT, unit=VALUE_UNIT_NONE, default=1.0, min=0.0, max=1.0)
#endregion

#region Async Delay
registerValueDescriptor('async_delay_filter', 'async_delay_filter', type=VALUE_TYPE_INT, unit=VALUE_UNIT_MS, default=0, min=0, max=20000)
#endregion

#endregion


#region Effect Filters

#region LUT

registerValueDescriptor('clut_filter', 'clut_amount', type=VALUE_TYPE_FLOAT, unit=VALUE_UNIT_NONE, default=1.0, min=0.0, max=1.0)
registerValueDescriptor('clut_filter', 'image_path', type=VALUE_TYPE_STRING, default='')

#endregion

#region Chroma Key
registerValueDescriptor('chroma_key_filter', 'brightness', type=VALUE_TYPE_FLOAT, default=0.0, min=-1.0, max=1.0)
registerValueDescriptor('chroma_key_filter', 'key_color', type=VALUE_TYPE_COLOR, default=int('ffffffff', 16))
registerValueDescriptor('chroma_key_filter', 'contrast', type=VALUE_TYPE_FLOAT, default=0.0, min=-1.0, max=1.0)
registerValueDescriptor('chroma_key_filter', 'gamma', type=VALUE_TYPE_FLOAT, default=0.0, min=-1.0, max=1.0)
registerValueDescriptor('chroma_key_filter', 'key_color_type', type=VALUE_TYPE_ENUM, default='green', allowed=['green', 'blue', 'magenta', 'custom'],)
registerValueDescriptor('chroma_key_filter', 'opacity', type=VALUE_TYPE_INT, default=100, min=0, max=100)
registerValueDescriptor('chroma_key_filter', 'similarity', type=VALUE_TYPE_INT, default=400, min=1, max=1000)
registerValueDescriptor('chroma_key_filter', 'smoothness', type=VALUE_TYPE_INT, default=80, min=1, max=1000)
registerValueDescriptor('chroma_key_filter', 'spill', type=VALUE_TYPE_INT, default=100, min=1, max=1000)
#endregion

#region Chroma Key V2
registerValueDescriptor('chroma_key_filter_v2', 'brightness', type=VALUE_TYPE_FLOAT, default=0.0, min=-1.0, max=1.0)
registerValueDescriptor('chroma_key_filter_v2', 'key_color', type=VALUE_TYPE_COLOR, default=int('ffffffff', 16))
registerValueDescriptor('chroma_key_filter_v2', 'contrast', type=VALUE_TYPE_FLOAT, default=0.0, min=-1.0, max=1.0)
registerValueDescriptor('chroma_key_filter_v2', 'gamma', type=VALUE_TYPE_FLOAT, default=0.0, min=-1.0, max=1.0)
registerValueDescriptor('chroma_key_filter_v2', 'key_color_type', type=VALUE_TYPE_ENUM, default='green', allowed=['green', 'blue', 'magenta', 'custom'],)
registerValueDescriptor('chroma_key_filter_v2', 'opacity', type=VALUE_TYPE_FLOAT, default=1.0, min=0.0, max=1.0)
registerValueDescriptor('chroma_key_filter_v2', 'similarity', type=VALUE_TYPE_INT, default=400, min=1, max=1000)
registerValueDescriptor('chroma_key_filter_v2', 'smoothness', type=VALUE_TYPE_INT, default=80, min=1, max=1000)
registerValueDescriptor('chroma_key_filter_v2', 'spill', type=VALUE_TYPE_INT, default=100, min=1, max=1000)
#endregion

#region Color Correction
registerValueDescriptor('color_filter', 'brightness', type=VALUE_TYPE_FLOAT, default=0.0, min=-1.0, max=1.0)
registerValueDescriptor('color_filter', 'color', type=VALUE_TYPE_COLOR, default=int('ffffffff', 16))
registerValueDescriptor('color_filter', 'contrast', type=VALUE_TYPE_FLOAT, default=0.0, min=-2.0, max=2.0)
registerValueDescriptor('color_filter', 'gamma', type=VALUE_TYPE_FLOAT, default=0.0, min=-3.0, max=3.0)
registerValueDescriptor('color_filter', 'hue_shift', type=VALUE_TYPE_FLOAT, default=0.0, min=-180.0, max=180.0)
registerValueDescriptor('color_filter', 'opacity', type=VALUE_TYPE_INT, default=100, min=0, max=100)
registerValueDescriptor('color_filter', 'saturation', type=VALUE_TYPE_FLOAT, default=0.0, min=-1.0, max=5.0)
#endregion

#region Color Correction V2
registerValueDescriptor('color_filter_v2', 'brightness', type=VALUE_TYPE_FLOAT, default=0.0, min=-1.0, max=1.0)
registerValueDescriptor('color_filter_v2', 'color', type=VALUE_TYPE_COLOR, default=int('ffffffff', 16))
registerValueDescriptor('color_filter_v2', 'contrast', type=VALUE_TYPE_FLOAT, default=0.0, min=-2.0, max=2.0)
registerValueDescriptor('color_filter_v2', 'gamma', type=VALUE_TYPE_FLOAT, default=0.0, min=-3.0, max=3.0)
registerValueDescriptor('color_filter_v2', 'hue_shift', type=VALUE_TYPE_FLOAT, default=0.0, min=-180.0, max=180.0)
registerValueDescriptor('color_filter_v2', 'opacity', type=VALUE_TYPE_FLOAT, default=1.0, min=0.0, max=1.0)
registerValueDescriptor('color_filter_v2', 'saturation', type=VALUE_TYPE_FLOAT, default=0.0, min=-1.0, max=5.0)
#endregion

#region Color Key
registerValueDescriptor('color_key_filter', 'key_color_type', type=VALUE_TYPE_ENUM, default='green', allowed=['green', 'blue', 'magenta', 'custom'],)
registerValueDescriptor('color_key_filter', 'key_color', type=VALUE_TYPE_COLOR, default=int('ffffffff', 16))
registerValueDescriptor('color_key_filter', 'similarity', type=VALUE_TYPE_INT, default=80, min=1, max=1000)
registerValueDescriptor('color_key_filter', 'smoothness', type=VALUE_TYPE_INT, default=50, min=1, max=1000)
registerValueDescriptor('color_key_filter', 'opacity', type=VALUE_TYPE_INT, default=100, min=0, max=100)
registerValueDescriptor('color_key_filter', 'brightness', type=VALUE_TYPE_FLOAT, default=0.0, min=-1.0, max=1.0)
registerValueDescriptor('color_key_filter', 'contrast', type=VALUE_TYPE_FLOAT, default=0.0, min=-1.0, max=1.0)
registerValueDescriptor('color_key_filter', 'gamma', type=VALUE_TYPE_FLOAT, default=0.0, min=-1.0, max=1.0)
#endregion

#region Color Key V2
registerValueDescriptor('color_key_filter_v2', 'key_color_type', type=VALUE_TYPE_ENUM, default='green', allowed=['green', 'blue', 'magenta', 'custom'],)
registerValueDescriptor('color_key_filter_v2', 'key_color', type=VALUE_TYPE_COLOR, default=int('ffffffff', 16))
registerValueDescriptor('color_key_filter_v2', 'similarity', type=VALUE_TYPE_INT, default=80, min=1, max=1000)
registerValueDescriptor('color_key_filter_v2', 'smoothness', type=VALUE_TYPE_INT, default=50, min=1, max=1000)
registerValueDescriptor('color_key_filter_v2', 'opacity', type=VALUE_TYPE_FLOAT, default=1.0, min=0.0, max=1.0)
registerValueDescriptor('color_key_filter_v2', 'brightness', type=VALUE_TYPE_FLOAT, default=0.0, min=-1.0, max=1.0)
registerValueDescriptor('color_key_filter_v2', 'contrast', type=VALUE_TYPE_FLOAT, default=0.0, min=-1.0, max=1.0)
registerValueDescriptor('color_key_filter_v2', 'gamma', type=VALUE_TYPE_FLOAT, default=0.0, min=-1.0, max=1.0)
#endregion

#region Crop Filter
registerValueDescriptor('crop_filter', 'relative', type=VALUE_TYPE_BOOLEAN, default=True)

registerValueDescriptor('crop_filter', 'bottom', type=VALUE_TYPE_INT, default=0, min=-8192, max=8192)
registerValueDescriptor('crop_filter', 'left', type=VALUE_TYPE_INT, default=0, min=-8192, max=8192)
registerValueDescriptor('crop_filter', 'right', type=VALUE_TYPE_INT, default=0, min=-8192, max=8192)
registerValueDescriptor('crop_filter', 'top', type=VALUE_TYPE_INT, default=0, min=-8192, max=8192)
registerValueDescriptor('crop_filter', 'cx', type=VALUE_TYPE_INT, default=0, min=0, max=8192)
registerValueDescriptor('crop_filter', 'cy', type=VALUE_TYPE_INT, default=0, min=0, max=8192)
#endregion

#region Mask Filter
registerValueDescriptor('mask_filter', 'color', type=VALUE_TYPE_COLOR, default=int('ffffffff', 16))
registerValueDescriptor('mask_filter', 'image_path', type=VALUE_TYPE_STRING, default='')
registerValueDescriptor('mask_filter', 'opacity', type=VALUE_TYPE_INT, default=100, min=0, max=100)
registerValueDescriptor('mask_filter', 'stretch', type=VALUE_TYPE_BOOLEAN, default=False)
registerValueDescriptor('mask_filter', 'type', type=VALUE_TYPE_ENUM, default='mask_color_filter.effect',
                        allowed=['mask_color_filter.effect', 'mask_alpha_filter.effect', 'blend_mul_filter.effect', 'blend_add_filter.effect', 'blend_sub_filter.effect'])
#endregion

#region Mask Filter V2
registerValueDescriptor('mask_filter_v2', 'color', type=VALUE_TYPE_COLOR, default=int('ffffffff', 16))
registerValueDescriptor('mask_filter_v2', 'image_path', type=VALUE_TYPE_STRING, default='')
registerValueDescriptor('mask_filter_v2', 'opacity', type=VALUE_TYPE_FLOAT, default=1.0, min=0.0, max=1.0)
registerValueDescriptor('mask_filter_v2', 'stretch', type=VALUE_TYPE_BOOLEAN, default=False)
registerValueDescriptor('mask_filter_v2', 'type', type=VALUE_TYPE_ENUM, default='mask_color_filter.effect',
                        allowed=['mask_color_filter.effect', 'mask_alpha_filter.effect', 'blend_mul_filter.effect', 'blend_add_filter.effect', 'blend_sub_filter.effect'])
#endregion

#region Luma Key Filter
registerValueDescriptor('luma_key_filter', 'luma_max', type=VALUE_TYPE_FLOAT, default=1.0, min=0.0, max=1.0)
registerValueDescriptor('luma_key_filter', 'luma_max_smooth', type=VALUE_TYPE_FLOAT, default=0.0, min=0.0, max=1.0)
registerValueDescriptor('luma_key_filter', 'luma_min', type=VALUE_TYPE_FLOAT, default=0.0, min=0.0, max=1.0)
registerValueDescriptor('luma_key_filter', 'luma_min_smooth', type=VALUE_TYPE_FLOAT, default=0.0, min=0.0, max=1.0)
#endregion

#region Render Delay
registerValueDescriptor('gpu_delay', 'delay_ms', type=VALUE_TYPE_INT, unit=VALUE_UNIT_MS, default=0, min=0, max=500)
#endregion

#region Scale Filter
registerValueDescriptor('gain_filter', 'resolution', type=VALUE_TYPE_STRING, default='None')
registerValueDescriptor('sampling', 'sampling', type=VALUE_TYPE_ENUM, default='bicubic', allowed=['point', 'bilinear', 'bicubic', 'lanczos', 'area'])
registerValueDescriptor('gain_filter', 'undistort', type=VALUE_TYPE_BOOLEAN, default=False)
#endregion

#region Scroll Filter
registerValueDescriptor('scroll_filter', 'cx', type=VALUE_TYPE_INT, default=100, min=1, max=8192)
registerValueDescriptor('scroll_filter', 'cy', type=VALUE_TYPE_INT, default=100, min=1, max=8192)
registerValueDescriptor('scroll_filter', 'limit_cx', type=VALUE_TYPE_BOOLEAN, default=False)
registerValueDescriptor('scroll_filter', 'limit_cy', type=VALUE_TYPE_BOOLEAN, default=False)
registerValueDescriptor('scroll_filter', 'loop', type=VALUE_TYPE_BOOLEAN, default=True)
registerValueDescriptor('scroll_filter', 'speed_x', type=VALUE_TYPE_FLOAT, default=0, min=-500.0, max=500.0)
registerValueDescriptor('scroll_filter', 'speed_y', type=VALUE_TYPE_FLOAT, default=0, min=-500.0, max=500.0)
#endregion

#region Sharpness
registerValueDescriptor('sharpness_filter', 'sharpness', type=VALUE_TYPE_FLOAT, default=0.08, min=0.0, max=1.0)
#endregion
#endregion


def getSettingsForType(type: str):
    if type in VALUE_DESCRIPTORS:
        return VALUE_DESCRIPTORS[type]
    return {}
