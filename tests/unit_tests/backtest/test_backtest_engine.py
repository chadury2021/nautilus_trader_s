# -------------------------------------------------------------------------------------------------
#  Copyright (C) 2015-2020 Nautech Systems Pty Ltd. All rights reserved.
#  https://nautechsystems.io
#
#  Licensed under the GNU Lesser General Public License Version 3.0 (the "License");
#  You may not use this file except in compliance with the License.
#  You may obtain a copy of the License at https://www.gnu.org/licenses/lgpl-3.0.en.html
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# -------------------------------------------------------------------------------------------------

import unittest

from nautilus_trader.backtest.data_container import BacktestDataContainer
from nautilus_trader.backtest.engine import BacktestEngine
from nautilus_trader.backtest.models import FillModel
from nautilus_trader.model.currencies import USD
from nautilus_trader.model.enums import BarAggregation
from nautilus_trader.model.enums import OMSType
from nautilus_trader.model.enums import PriceType
from nautilus_trader.model.identifiers import Venue
from nautilus_trader.model.objects import Money
from nautilus_trader.trading.strategy import TradingStrategy
from tests.test_kit.providers import TestDataProvider
from tests.test_kit.providers import TestInstrumentProvider
from tests.test_kit.stubs import TestStubs


USDJPY_FXCM = TestStubs.symbol_usdjpy_fxcm()


class BacktestEngineTests(unittest.TestCase):

    def setUp(self):
        # Fixture Setup
        usdjpy = TestInstrumentProvider.default_fx_ccy(TestStubs.symbol_usdjpy_fxcm())
        data = BacktestDataContainer()
        data.add_instrument(usdjpy)
        data.add_bars(usdjpy.symbol, BarAggregation.MINUTE, PriceType.BID, TestDataProvider.usdjpy_1min_bid()[:2000])
        data.add_bars(usdjpy.symbol, BarAggregation.MINUTE, PriceType.ASK, TestDataProvider.usdjpy_1min_ask()[:2000])

        self.engine = BacktestEngine(
            data=data,
            strategies=[TradingStrategy("000")],
        )

        self.engine.add_exchange(
            venue=Venue("FXCM"),
            oms_type=OMSType.HEDGING,
            generate_position_ids=True,
            starting_balances=[Money(1_000_000, USD)],
            fill_model=FillModel(),
        )

    def tearDown(self):
        self.engine.reset()
        self.engine.dispose()

    def test_initialization(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual(1, len(self.engine.trader.strategy_states()))

    def test_reset_engine(self):
        # Arrange
        self.engine.run()

        # Act
        self.engine.reset()

        # Assert
        self.assertEqual(0, self.engine.iteration)  # No exceptions raised

    def test_run_empty_strategy(self):
        # Arrange
        # Act
        self.engine.run()

        # Assert
        self.assertEqual(7999, self.engine.iteration)

    def test_change_fill_model(self):
        # Arrange
        # Act
        self.engine.change_fill_model(Venue("FXCM"), FillModel())

        # Assert
        self.assertTrue(True)  # No exception raised
