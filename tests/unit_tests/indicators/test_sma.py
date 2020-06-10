# -------------------------------------------------------------------------------------------------
#  Copyright (C) 2015-2020 Nautech Systems Pty Ltd. All rights reserved.
#  The use of this source code is governed by the license as found in the LICENSE file.
#  https://nautechsystems.io
# -------------------------------------------------------------------------------------------------

import time
import unittest

from nautilus_trader.indicators.average.sma import SimpleMovingAverage

from tests.test_kit.series import BatterySeries


class SimpleMovingAverageTests(unittest.TestCase):

    # Fixture Setup
    def setUp(self):
        # Arrange
        self.sma = SimpleMovingAverage(10)

    def test_name_returns_expected_name(self):
        # Act
        # Assert
        self.assertEqual('SimpleMovingAverage', self.sma.name)

    def test_str_returns_expected_string(self):
        # Act
        # Assert
        self.assertEqual('SimpleMovingAverage(10)', str(self.sma))

    def test_repr_returns_expected_string(self):
        # Act
        # Assert
        self.assertTrue(repr(self.sma).startswith('<SimpleMovingAverage(10) object at'))
        self.assertTrue(repr(self.sma).endswith('>'))

    def test_period_returns_expected_value(self):
        # Act
        # Assert
        self.assertEqual(10, self.sma.period)

    def test_initialized_without_inputs_returns_false(self):
        # Act
        # Assert
        self.assertEqual(False, self.sma.initialized)

    def test_initialized_with_required_inputs_returns_true(self):
        # Arrange
        self.sma.update(1.00000)
        self.sma.update(2.00000)
        self.sma.update(3.00000)
        self.sma.update(4.00000)
        self.sma.update(5.00000)
        self.sma.update(6.00000)
        self.sma.update(7.00000)
        self.sma.update(8.00000)
        self.sma.update(9.00000)
        self.sma.update(10.00000)

        # Act
        # Assert
        self.assertEqual(True, self.sma.initialized)
        self.assertEqual(10, self.sma.count)
        self.assertEqual(5.5, self.sma.value)

    def test_value_with_one_input_returns_expected_value(self):
        # Arrange
        self.sma.update(1.00000)

        # Act
        # Assert
        self.assertEqual(1.0, self.sma.value)

    def test_value_with_three_inputs_returns_expected_value(self):
        # Arrange
        self.sma.update(1.00000)
        self.sma.update(2.00000)
        self.sma.update(3.00000)

        # Act
        # Assert
        self.assertEqual(2.0, self.sma.value)

    def test_value_at_returns_expected_value(self):
        # Arrange
        self.sma.update(1.00000)
        self.sma.update(2.00000)
        self.sma.update(3.00000)

        # Act
        # Assert
        self.assertEqual(2.0, self.sma.value)

    def test_with_battery_signal(self):
        # Arrange
        tt = time.time()
        battery_signal = BatterySeries.create(length=1000000)
        output = []

        # Act
        for point in battery_signal:
            self.sma.update(point)
            output.append(self.sma.value)

        # Assert
        self.assertEqual(len(battery_signal), len(output))
        print(self.sma.value)
        print(time.time() - tt)