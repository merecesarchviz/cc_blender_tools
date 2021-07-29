# Copyright (C) 2021 Victor Soupday
# This file is part of CC3_Blender_Tools <https://github.com/soupday/cc3_blender_tools>
#
# CC3_Blender_Tools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CC3_Blender_Tools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CC3_Blender_Tools.  If not, see <https://www.gnu.org/licenses/>.

import bpy
import os
import time

from bpy.types import XrSessionSettings
from . import vars

timer = 0

def log_info(msg):
    prefs = bpy.context.preferences.addons[__name__.partition(".")[0]].preferences
    """Log an info message to console."""
    if prefs.log_level == "ALL":
        print(msg)


def log_warn(msg):
    prefs = bpy.context.preferences.addons[__name__.partition(".")[0]].preferences
    """Log a warning message to console."""
    if prefs.log_level == "ALL" or prefs.log_level == "WARN":
        print("Warning: " + msg)


def log_error(msg, e = None):
    """Log an error message to console and raise an exception."""
    print("Error: " + msg)
    if e is not None:
        print("    -> " + getattr(e, 'message', repr(e)))


def start_timer():
    global timer
    timer = time.perf_counter()


def log_timer(msg, unit = "s"):
    prefs = bpy.context.preferences.addons[__name__.partition(".")[0]].preferences
    global timer
    if prefs.log_level == "ALL":
        duration = time.perf_counter() - timer
        if unit == "ms":
            duration *= 1000
        elif unit == "us":
            duration *= 1000000
        elif unit == "ns":
            duration *= 1000000000
        print(msg + ": " + str(duration) + " " + unit)


def message_box(message = "", title = "Info", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text = message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)


def unique_name(name, no_version = False):
    """Generate a unique name for the node or property to quickly
       identify texture nodes or nodes with parameters."""

    props = bpy.context.scene.CC3ImportProps
    if no_version:
        name = name + "_" + vars.NODE_PREFIX + str(props.node_id)
    else:
        name = vars.NODE_PREFIX + name + "_" + vars.VERSION_STRING + "_" + str(props.node_id)
    props.node_id = props.node_id + 1
    return name


def is_same_path(pa, pb):
    return os.path.normcase(os.path.realpath(pa)) == os.path.normcase(os.path.realpath(pb))


def is_in_path(pa, pb):
    return os.path.normcase(os.path.realpath(pa)) in os.path.normcase(os.path.realpath(pb))


def object_has_material(obj, name):
    name = name.lower()
    if obj.type == "MESH":
        for mat in obj.data.materials:
            if name in mat.name.lower():
                return True
    return False


def obj_exists(obj):
    try:
        name = obj.name
        return True
    except:
        return False


def clamp(x, min = 0.0, max = 1.0):
    if x < min:
        x = min
    if x > max:
        x = max
    return x


def smoothstep(edge0, edge1, x):
    x = clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return x * x * (3 - 2 * x)


def saturate(x):
    if x < 0.0:
        x = 0.0
    if x > 1.0:
        x = 1.0
    return x


def remap(edge0, edge1, min, max, x):
    return min + ((x - edge0) * (max - min) / (edge1 - edge0))


def lerp(min, max, t):
    return min + (max - min) * t


def inverse_lerp(min, max, value):
    return (value - min) / (max - min)


def lerp_color(c0, c1, t):
    return (lerp(c0[0], c1[0], t),
            lerp(c0[1], c1[1], t),
            lerp(c0[2], c1[2], t),
            lerp(c0[3], c1[3], t))


def linear_to_srgbx(x):
    if x < 0.0:
        return 0.0
    elif x < 0.0031308:
        return x * 12.92
    elif x < 1.0:
        return 1.055 * pow(x, 1.0 / 2.4) - 0.055
    else:
        return pow(x, 5.0 / 11.0)


def linear_to_srgb(color):
    return (linear_to_srgbx(color[0]),
            linear_to_srgbx(color[1]),
            linear_to_srgbx(color[2]),
            color[3])


def srgb_to_linearx(x):
    if x <= 0.04045:
        return x / 12.95
    elif x < 1.0:
        return pow((x + 0.055) / 1.055, 2.4)
    else:
        return pow(x, 2.2)


def srgb_to_linear(color):
    return (srgb_to_linearx(color[0]),
            srgb_to_linearx(color[1]),
            srgb_to_linearx(color[2]),
            color[3])


def count_maps(*maps):
    count = 0
    for map in maps:
        if map is not None:
            count += 1
    return count


def dimensions(x):
    try:
        l = len(x)
        return l
    except:
        return 1


def match_dimensions(socket, value):
    socket_dimensions = dimensions(socket)
    value_dimensions = dimensions(value)
    if socket_dimensions == 3 and value_dimensions == 1:
        return (value, value, value)
    elif socket_dimensions == 2 and value_dimensions == 1:
        return (value, value)
    return value


