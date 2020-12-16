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

from decimal import Decimal
import unittest

from parameterized import parameterized

from nautilus_trader.common.clock import TestClock
from nautilus_trader.common.logging import TestLogger
from nautilus_trader.data.cache import DataCache
from nautilus_trader.model.bar import Bar
from nautilus_trader.model.currencies import AUD
from nautilus_trader.model.currencies import JPY
from nautilus_trader.model.currencies import USD
from nautilus_trader.model.enums import Maker
from nautilus_trader.model.enums import PriceType
from nautilus_trader.model.identifiers import Symbol
from nautilus_trader.model.identifiers import TradeMatchId
from nautilus_trader.model.identifiers import Venue
from nautilus_trader.model.objects import Price
from nautilus_trader.model.objects import Quantity
from nautilus_trader.model.tick import QuoteTick
from nautilus_trader.model.tick import TradeTick
from tests.test_kit.providers import TestInstrumentProvider
from tests.test_kit.stubs import TestStubs
from tests.test_kit.stubs import UNIX_EPOCH


FXCM = Venue("FXCM")
USDJPY_FXCM = TestInstrumentProvider.default_fx_ccy(Symbol("USD/JPY", FXCM))
AUDUSD_FXCM = TestInstrumentProvider.default_fx_ccy(Symbol("AUD/USD", FXCM))


class DataCacheTests(unittest.TestCase):

    def setUp(self):
        # Fixture Setup
        self.cache = DataCache(logger=TestLogger(TestClock()))

    def test_reset_an_empty_cache(self):
        # Arrange
        # Act
        self.cache.reset()

        # Assert
        self.assertEqual([], self.cache.instruments())
        self.assertEqual([], self.cache.quote_ticks(AUDUSD_FXCM.symbol))
        self.assertEqual([], self.cache.trade_ticks(AUDUSD_FXCM.symbol))
        self.assertEqual([], self.cache.bars(TestStubs.bartype_gbpusd_1sec_mid()))

    def test_symbols_when_no_instruments_returns_empty_list(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual([], self.cache.symbols())

    def test_instruments_when_no_instruments_returns_empty_list(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual([], self.cache.instruments())

    def test_quote_ticks_for_unknown_symbol_returns_empty_list(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual([], self.cache.quote_ticks(AUDUSD_FXCM.symbol))

    def test_trade_ticks_for_unknown_symbol_returns_empty_list(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual([], self.cache.trade_ticks(AUDUSD_FXCM.symbol))

    def test_bars_for_unknown_symbol_returns_empty_list(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual([], self.cache.bars(TestStubs.bartype_gbpusd_1sec_mid()))

    def test_instrument_when_no_instruments_returns_none(self):
        # Arrange
        # Act
        # Assert
        self.assertIsNone(self.cache.instrument(AUDUSD_FXCM.symbol))

    def test_quote_tick_when_no_ticks_returns_none(self):
        # Arrange
        # Act
        # Assert
        self.assertIsNone(self.cache.quote_tick(AUDUSD_FXCM.symbol))

    def test_trade_tick_when_no_ticks_returns_none(self):
        # Arrange
        # Act
        # Assert
        self.assertIsNone(self.cache.trade_tick(AUDUSD_FXCM.symbol))

    def test_bar_when_no_bars_returns_none(self):
        # Arrange
        # Act
        # Assert
        self.assertIsNone(self.cache.bar(TestStubs.bartype_gbpusd_1sec_mid()))

    def test_quote_tick_count_for_unknown_symbol_returns_zero(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual(0, self.cache.quote_tick_count(AUDUSD_FXCM.symbol))

    def test_trade_tick_count_for_unknown_symbol_returns_zero(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual(0, self.cache.trade_tick_count(AUDUSD_FXCM.symbol))

    def test_has_quote_ticks_for_unknown_symbol_returns_false(self):
        # Arrange
        # Act
        # Assert
        self.assertFalse(self.cache.has_quote_ticks(AUDUSD_FXCM.symbol))

    def test_has_trade_ticks_for_unknown_symbol_returns_false(self):
        # Arrange
        # Act
        # Assert
        self.assertFalse(self.cache.has_trade_ticks(AUDUSD_FXCM.symbol))

    def test_has_bars_for_unknown_bar_type_returns_false(self):
        # Arrange
        # Act
        # Assert
        self.assertFalse(self.cache.has_bars(TestStubs.bartype_gbpusd_1sec_mid()))

    def test_symbols_when_one_instrument_returns_expected_list(self):
        # Arrange
        instrument = TestInstrumentProvider.ethusdt_binance()

        self.cache.add_instrument(instrument)

        # Act
        result = self.cache.symbols()

        # Assert
        self.assertEqual([instrument.symbol], result)

    def test_instruments_when_one_instrument_returns_expected_list(self):
        # Arrange
        instrument = TestInstrumentProvider.ethusdt_binance()

        self.cache.add_instrument(instrument)

        # Act
        result = self.cache.instruments()

        # Assert
        self.assertEqual([instrument], result)

    def test_quote_ticks_when_one_tick_returns_expected_list(self):
        # Arrange
        tick = QuoteTick(
            AUDUSD_FXCM.symbol,
            Price("1.00000"),
            Price("1.00001"),
            Quantity(1),
            Quantity(1),
            UNIX_EPOCH,
        )

        self.cache.add_quote_ticks([tick])

        # Act
        result = self.cache.quote_ticks(tick.symbol)

        # Assert
        self.assertEqual([tick], result)

    def test_add_quote_ticks_when_already_ticks_does_not_add(self):
        # Arrange
        tick = QuoteTick(
            AUDUSD_FXCM.symbol,
            Price("1.00000"),
            Price("1.00001"),
            Quantity(1),
            Quantity(1),
            UNIX_EPOCH,
        )

        self.cache.add_quote_tick(tick)

        # Act
        self.cache.add_quote_ticks([tick])
        result = self.cache.quote_ticks(tick.symbol)

        # Assert
        self.assertEqual([tick], result)

    def test_trade_ticks_when_one_tick_returns_expected_list(self):
        # Arrange
        tick = TradeTick(
            AUDUSD_FXCM.symbol,
            Price("1.00000"),
            Quantity(10000),
            Maker.BUYER,
            TradeMatchId("123456789"),
            UNIX_EPOCH,
        )

        self.cache.add_trade_ticks([tick])

        # Act
        result = self.cache.trade_ticks(tick.symbol)

        # Assert
        self.assertEqual([tick], result)

    def test_add_trade_ticks_when_already_ticks_does_not_add(self):
        # Arrange
        tick = TradeTick(
            AUDUSD_FXCM.symbol,
            Price("1.00000"),
            Quantity(10000),
            Maker.BUYER,
            TradeMatchId("123456789"),
            UNIX_EPOCH,
        )

        self.cache.add_trade_tick(tick)

        # Act
        self.cache.add_trade_ticks([tick])
        result = self.cache.trade_ticks(tick.symbol)

        # Assert
        self.assertEqual([tick], result)

    def test_bars_when_one_bar_returns_expected_list(self):
        # Arrange
        bar_type = TestStubs.bartype_gbpusd_1sec_mid()
        bar = Bar(
            Price("1.00001"),
            Price("1.00004"),
            Price("1.00002"),
            Price("1.00003"),
            Quantity(100000),
            UNIX_EPOCH,
        )

        self.cache.add_bars(bar_type, [bar])

        # Act
        result = self.cache.bars(bar_type)

        # Assert
        self.assertTrue([bar], result)

    def test_add_bars_when_already_bars_does_not_add(self):
        # Arrange
        bar_type = TestStubs.bartype_gbpusd_1sec_mid()
        bar = Bar(
            Price("1.00001"),
            Price("1.00004"),
            Price("1.00002"),
            Price("1.00003"),
            Quantity(100000),
            UNIX_EPOCH,
        )

        self.cache.add_bar(bar_type, bar)

        # Act
        self.cache.add_bars(bar_type, [bar])
        result = self.cache.bars(bar_type)

        # Assert
        self.assertTrue([bar], result)

    def test_instrument_when_no_instrument_returns_none(self):
        # Arrange
        # Act
        result = self.cache.instrument(AUDUSD_FXCM.symbol)

        # Assert
        self.assertIsNone(result)

    def test_instrument_when_instrument_exists_returns_expected(self):
        self.cache.add_instrument(AUDUSD_FXCM)

        # Act
        result = self.cache.instrument(AUDUSD_FXCM.symbol)

        # Assert
        self.assertEqual(AUDUSD_FXCM, result)

    def test_price_when_no_ticks_returns_none(self):
        # Act
        result = self.cache.price(AUDUSD_FXCM.symbol, PriceType.LAST)

        # Assert
        self.assertIsNone(result)

    def test_price_given_last_when_no_trade_ticks_returns_none(self):
        # Act
        tick = QuoteTick(
            AUDUSD_FXCM.symbol,
            Price("1.00000"),
            Price("1.00001"),
            Quantity(1),
            Quantity(1),
            UNIX_EPOCH,
        )

        self.cache.add_quote_tick(tick)

        result = self.cache.price(AUDUSD_FXCM.symbol, PriceType.LAST)

        # Assert
        self.assertIsNone(result)

    def test_price_given_quote_price_type_when_no_quote_ticks_returns_none(self):
        # Arrange
        tick = TradeTick(
            AUDUSD_FXCM.symbol,
            Price("1.00000"),
            Quantity(10000),
            Maker.BUYER,
            TradeMatchId("123456789"),
            UNIX_EPOCH,
        )

        self.cache.add_trade_tick(tick)

        # Act
        result = self.cache.price(AUDUSD_FXCM.symbol, PriceType.MID)

        # Assert
        self.assertIsNone(result)

    def test_price_given_last_when_trade_tick_returns_expected_price(self):
        # Arrange
        tick = TradeTick(
            AUDUSD_FXCM.symbol,
            Price("1.00000"),
            Quantity(10000),
            Maker.BUYER,
            TradeMatchId("123456789"),
            UNIX_EPOCH,
        )

        self.cache.add_trade_tick(tick)

        # Act
        result = self.cache.price(AUDUSD_FXCM.symbol, PriceType.LAST)

        # Assert
        self.assertEqual(Price("1.00000"), result)

    @parameterized.expand([
        [PriceType.BID, Price("1.00000")],
        [PriceType.ASK, Price("1.00001")],
        [PriceType.MID, Price("1.000005")],
    ])
    def test_price_given_various_quote_price_types_when_quote_tick_returns_expected_price(self, price_type, expected):
        # Arrange
        tick = QuoteTick(
            AUDUSD_FXCM.symbol,
            Price("1.00000"),
            Price("1.00001"),
            Quantity(1),
            Quantity(1),
            UNIX_EPOCH,
        )

        self.cache.add_quote_tick(tick)

        # Act
        result = self.cache.price(AUDUSD_FXCM.symbol, price_type)

        # Assert
        self.assertEqual(expected, result)

    def test_quote_tick_when_index_out_of_range_returns_none(self):
        # Arrange
        tick = QuoteTick(
            AUDUSD_FXCM.symbol,
            Price("1.00000"),
            Price("1.00001"),
            Quantity(1),
            Quantity(1),
            UNIX_EPOCH,
        )

        self.cache.add_quote_tick(tick)

        # Act
        result = self.cache.quote_tick(AUDUSD_FXCM.symbol, index=1)

        # Assert
        self.assertEqual(1, self.cache.quote_tick_count(AUDUSD_FXCM.symbol))
        self.assertIsNone(result)

    def test_quote_tick_with_two_ticks_returns_expected_tick(self):
        # Arrange
        tick1 = QuoteTick(
            AUDUSD_FXCM.symbol,
            Price("1.00000"),
            Price("1.00001"),
            Quantity(1),
            Quantity(1),
            UNIX_EPOCH,
        )

        tick2 = QuoteTick(
            AUDUSD_FXCM.symbol,
            Price("1.00001"),
            Price("1.00003"),
            Quantity(1),
            Quantity(1),
            UNIX_EPOCH,
        )

        self.cache.add_quote_tick(tick1)
        self.cache.add_quote_tick(tick2)

        # Act
        result = self.cache.quote_tick(AUDUSD_FXCM.symbol, index=0)

        # Assert
        self.assertEqual(2, self.cache.quote_tick_count(AUDUSD_FXCM.symbol))
        self.assertEqual(tick2, result)

    def test_trade_tick_when_index_out_of_range_returns_none(self):
        # Arrange
        tick = TradeTick(
            AUDUSD_FXCM.symbol,
            Price("1.00000"),
            Quantity(10000),
            Maker.BUYER,
            TradeMatchId("123456789"),
            UNIX_EPOCH,
        )

        self.cache.add_trade_tick(tick)

        # Act
        result = self.cache.trade_tick(AUDUSD_FXCM.symbol, index=1)

        # Assert
        self.assertEqual(1, self.cache.trade_tick_count(AUDUSD_FXCM.symbol))
        self.assertIsNone(result)

    def test_trade_tick_with_one_tick_returns_expected_tick(self):
        # Arrange
        tick1 = TradeTick(
            AUDUSD_FXCM.symbol,
            Price("1.00000"),
            Quantity(10000),
            Maker.BUYER,
            TradeMatchId("123456789"),
            UNIX_EPOCH,
        )

        tick2 = TradeTick(
            AUDUSD_FXCM.symbol,
            Price("1.00001"),
            Quantity(20000),
            Maker.SELLER,
            TradeMatchId("123456789"),
            UNIX_EPOCH,
        )

        self.cache.add_trade_tick(tick1)
        self.cache.add_trade_tick(tick2)

        # Act
        result = self.cache.trade_tick(AUDUSD_FXCM.symbol, index=0)

        # Assert
        self.assertEqual(2, self.cache.trade_tick_count(AUDUSD_FXCM.symbol))
        self.assertEqual(tick2, result)

    def test_bar_index_out_of_range_returns_expected_bar(self):
        # Arrange
        bar_type = TestStubs.bartype_gbpusd_1sec_mid()
        bar = Bar(
            Price("1.00001"),
            Price("1.00004"),
            Price("1.00002"),
            Price("1.00003"),
            Quantity(100000),
            UNIX_EPOCH,
        )

        self.cache.add_bar(bar_type, bar)

        # Act
        result = self.cache.bar(bar_type, index=1)

        # Assert
        self.assertEqual(1, self.cache.bar_count(bar_type))
        self.assertIsNone(result)

    def test_bar_with_two_bars_returns_expected_bar(self):
        # Arrange
        bar_type = TestStubs.bartype_gbpusd_1sec_mid()
        bar1 = Bar(
            Price("1.00001"),
            Price("1.00004"),
            Price("1.00002"),
            Price("1.00003"),
            Quantity(100000),
            UNIX_EPOCH,
        )

        bar2 = Bar(
            Price("1.00002"),
            Price("1.00003"),
            Price("1.00004"),
            Price("1.00005"),
            Quantity(200000),
            UNIX_EPOCH,
        )

        self.cache.add_bar(bar_type, bar1)
        self.cache.add_bar(bar_type, bar2)

        # Act
        result = self.cache.bar(bar_type, index=0)

        # Assert
        self.assertEqual(2, self.cache.bar_count(bar_type))
        self.assertEqual(bar2, result)

    def test_get_xrate_returns_correct_rate(self):
        # Arrange
        self.cache.add_instrument(USDJPY_FXCM)

        tick = QuoteTick(
            USDJPY_FXCM.symbol,
            Price("110.80000"),
            Price("110.80010"),
            Quantity(1),
            Quantity(1),
            UNIX_EPOCH,
        )

        self.cache.add_quote_tick(tick)

        # Act
        result = self.cache.get_xrate(FXCM, JPY, USD)

        # Assert
        self.assertEqual(Decimal("0.009025266685348968705339031887"), result)

    def test_get_xrate_with_no_conversion_returns_one(self):
        # Arrange
        # Act
        result = self.cache.get_xrate(FXCM, AUD, AUD)

        # Assert
        self.assertEqual(Decimal("1"), result)

    def test_get_xrate_with_conversion(self):
        # Arrange
        self.cache.add_instrument(AUDUSD_FXCM)

        tick = QuoteTick(
            AUDUSD_FXCM.symbol,
            Price("0.80000"),
            Price("0.80010"),
            Quantity(1),
            Quantity(1),
            UNIX_EPOCH,
        )

        self.cache.add_quote_tick(tick)

        # Act
        result = self.cache.get_xrate(FXCM, AUD, USD)

        # Assert
        self.assertEqual(Decimal("0.80005"), result)
