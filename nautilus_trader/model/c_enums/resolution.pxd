# -------------------------------------------------------------------------------------------------
# <copyright file="resolution.pxd" company="Nautech Systems Pty Ltd">
#  Copyright (C) 2015-2019 Nautech Systems Pty Ltd. All rights reserved.
#  The use of this source code is governed by the license as found in the LICENSE.md file.
#  https://nautechsystems.io
# </copyright>
# -------------------------------------------------------------------------------------------------


cpdef enum Resolution:
    UNKNOWN = -1,
    TICK = 0,
    SECOND = 1,
    MINUTE = 2,
    HOUR = 3,
    DAY = 4

cdef inline str resolution_string(int value):
    if value == 0:
        return "TICK"
    elif value == 1:
        return "SECOND"
    elif value == 2:
        return "MINUTE"
    elif value == 3:
        return "HOUR"
    elif value == 4:
        return "DAY"
    elif value == -1:
        return "UNKNOWN"
    else:
        return "UNKNOWN"
