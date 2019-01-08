#!/usr/bin/env python3
# -------------------------------------------------------------------------------------------------
# <copyright file="clock.pxd" company="Invariance Pte">
#  Copyright (C) 2018-2019 Invariance Pte. All rights reserved.
#  The use of this source code is governed by the license as found in the LICENSE.md file.
#  http://www.invariance.com
# </copyright>
# -------------------------------------------------------------------------------------------------

# cython: language_level=3, boundscheck=False

from cpython.datetime cimport datetime, timedelta
from inv_trader.model.identifiers cimport Label

cdef class Clock:
    """
    The abstract base class for all clocks.
    """
    cdef readonly object timezone
    cdef datetime _unix_epoch
    cdef dict _timers

    cpdef datetime time_now(self)
    cpdef datetime unix_epoch(self)
    cdef long milliseconds_since_unix_epoch(self)
    cpdef set_time_alert(
            self,
            Label label,
            datetime alert_time,
            handler)
    cpdef cancel_time_alert(self, Label label)
    cpdef set_timer(
            self,
            Label label,
            timedelta interval,
            datetime start_time,
            datetime stop_time,
            bint repeat,
            handler)
    cpdef cancel_timer(self, Label label)
    cpdef list get_labels(self)
    cpdef stop_all_timers(self)
    cpdef void _raise_time_event(
            self,
            Label label,
            datetime alert_time)
    cpdef void _repeating_timer(
            self,
            Label label,
            datetime alert_time,
            timedelta interval,
            datetime stop_time)

cdef class LiveClock(Clock):
    """
    Implements a clock for live trading.
    """
    pass


cdef class TestClock(Clock):
    """
    Implements a clock for backtesting and unit testing.
    """
    cdef datetime _time
    cdef readonly timedelta time_step

    cpdef void increment_time(self)
    cpdef void set_time(self, datetime time)