#!/usr/bin/env python3
# -------------------------------------------------------------------------------------------------
# <copyright file="objects.pyx" company="Invariance Pte">
#  Copyright (C) 2018-2019 Invariance Pte. All rights reserved.
#  The use of this source code is governed by the license as found in the LICENSE.md file.
#  http://www.invariance.com
# </copyright>
# -------------------------------------------------------------------------------------------------

# cython: language_level=3, boundscheck=False, wraparound=False

from cpython.datetime cimport datetime

from inv_trader.model.enums cimport Venue

cdef class Symbol:
    """
    Represents the symbol for a financial market tradeable instrument.
    """
    cdef readonly str code
    cdef readonly Venue venue


cdef class Tick:
    """
    Represents a single tick in a financial market.
    """
    cdef readonly Symbol symbol
    cdef readonly object bid
    cdef readonly object ask
    cdef readonly datetime timestamp


cdef class BarType:
    """
    Represents a financial market symbol and bar specification.
    """
    cdef readonly Symbol symbol
    cdef readonly int period
    cdef readonly object resolution
    cdef readonly object quote_type


cdef class Bar:
    """
    Represents a financial market trade bar.
    """
    cdef readonly object open
    cdef readonly object high
    cdef readonly object low
    cdef readonly object close
    cdef readonly int volume
    cdef readonly datetime timestamp


cdef class DataBar:
    """
    Represents a financial market trade bar.
    """
    cdef readonly double open
    cdef readonly double high
    cdef readonly double low
    cdef readonly double close
    cdef readonly double volume
    cdef readonly datetime timestamp


cdef class Instrument:
    """
    Represents a tradeable financial market instrument.
    """
    cdef readonly Symbol symbol
    cdef readonly str broker_symbol
    cdef readonly object quote_currency
    cdef readonly object security_type
    cdef readonly int tick_decimals
    cdef readonly object tick_size
    cdef readonly object tick_value
    cdef readonly object target_direct_spread
    cdef readonly int round_lot_size
    cdef readonly int contract_size
    cdef readonly int min_stop_distance_entry
    cdef readonly int min_limit_distance_entry
    cdef readonly int min_stop_distance
    cdef readonly int min_limit_distance
    cdef readonly int min_trade_size
    cdef readonly int max_trade_size
    cdef readonly object margin_requirement
    cdef readonly object rollover_interest_buy
    cdef readonly object rollover_interest_sell
    cdef readonly datetime timestamp