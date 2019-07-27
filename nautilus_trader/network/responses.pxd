# -------------------------------------------------------------------------------------------------
# <copyright file="responses.pxd" company="Nautech Systems Pty Ltd">
#  Copyright (C) 2015-2019 Nautech Systems Pty Ltd. All rights reserved.
#  The use of this source code is governed by the license as found in the LICENSE.md file.
#  https://nautechsystems.io
# </copyright>
# -------------------------------------------------------------------------------------------------

from nautilus_trader.core.message cimport Response


cdef class DataResponse(Response):
    """
    Represents a response of data.
    """
    cdef readonly bytes data
    cdef readonly str encoding
