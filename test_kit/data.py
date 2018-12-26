#!/usr/bin/env python3
# -------------------------------------------------------------------------------------------------
# <copyright file="data.py" company="Invariance Pte">
#  Copyright (C) 2018-2019 Invariance Pte. All rights reserved.
#  The use of this source code is governed by the license as found in the LICENSE.md file.
#  http://www.invariance.com
# </copyright>
# -------------------------------------------------------------------------------------------------

import pandas as pd

from pandas import DataFrame


class TestDataProvider(object):

    @staticmethod
    def get_gbpusd_1min_bid() -> DataFrame:
        return pd.read_csv('GBPUSD_1 Min_Bid_2008.01.01_2008.12.31.csv',
                           index_col='Time (UTC)')