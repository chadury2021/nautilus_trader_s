#!/usr/bin/env python3
# -------------------------------------------------------------------------------------------------
# <copyright file="tools.pyx" company="Invariance Pte">
#  Copyright (C) 2018 Invariance Pte. All rights reserved.
#  The use of this source code is governed by the license as found in the LICENSE.md file.
#  http://www.invariance.com
# </copyright>
# -------------------------------------------------------------------------------------------------

import cython
import inspect

from numpy import ndarray
from typing import Callable, List
from pandas.core.frame import DataFrame

from inv_trader.core.precondition import Precondition
from inv_trader.model.objects import DataBar


POINT = 'point'
PRICE = 'price'
MID = 'mid'
OPEN = 'open'
HIGH = 'high'
LOW = 'low'
CLOSE = 'close'
VOLUME = 'volume'
TIMESTAMP = 'timestamp'

cdef class BarBuilder:
    """
    Provides a means of building lists of bars from a given Pandas DataFrame of
    the correct specification.
    """
    cdef object _data
    cdef int _volume_multiple

    def __init__(self, data: DataFrame, volume_multiple: int=1):
        """
        Initializes a new instance of the BarBuilder class.

        :param volume_multiple: The volume multiple for the builder (> 0).
        """
        Precondition.positive(volume_multiple, 'volume_multiple')

        self._data = data
        self._volume_multiple = volume_multiple

    def build_bars(self):
        """
        Build a list of bars from the held Pandas DataFrame.
        
        :return: The bars.
        """
        return list(map(self._build_bar, self._data.index, self._data.values))

    def _build_bar(self, timestamp, values: ndarray):
        """
        Build a bar from the given index and values. The function expects the
        values to be an ndarray with 5 elements [open, high, low, close, volume].
        
        :param timestamp: The timestamp for the bar.
        :param values: The values for the bar. 
        :return: 
        """
        return DataBar(values[0],
                       values[1],
                       values[2],
                       values[3],
                       values[4] * self._volume_multiple,
                       timestamp)


cdef class IndicatorUpdater:
    """
    Provides an adapter for updating an indicator with a bar. When instantiated
    with a live indicator update method, the updater will inspect the method and
    construct the required parameter list for updates.
    """
    cdef object _indicator
    cdef object _input_method
    cdef list _input_params
    cdef list _outputs

    cdef readonly list output

    def __init__(self,
                 indicator: object,
                 input_method: Callable or None=None,
                 outputs: List[str] or None=None):
        """
        Initializes a new instance of the IndicatorUpdater class.

        :param indicator: The indicator for updating.
        :param input_method: The indicators input method.
        :param outputs: The list of the indicators output properties.
        """
        self._indicator = indicator
        if input_method is None:
            self._input_method = indicator.update
        else:
            self._input_method = input_method

        self._input_params = []

        param_map = {
            POINT: CLOSE,
            PRICE: CLOSE,
            MID: CLOSE,
            OPEN: OPEN,
            HIGH: HIGH,
            LOW: LOW,
            CLOSE: CLOSE,
            TIMESTAMP: TIMESTAMP
        }

        for param in inspect.signature(self._input_method).parameters:
            self._input_params.append(param_map[param])

        if outputs is None or len(outputs) == 0:
            self._outputs = ['value']
        else:
            self._outputs = outputs

        self.output = []

    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.binding(True)
    cpdef update_bar(self, object bar):
        """
        Update the indicator with the given Bar object.

        :param bar: The update bar.
        """
        self._input_method(*[bar.__getattribute__(param) for param in self._input_params])

    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.binding(True)
    cpdef list get_outputs(self):
        """
        Create a list of the current indicator outputs.
        
        :return: The list of indicator outputs.
        """
        return [self._indicator.__getattribute__(output) for output in self._outputs]