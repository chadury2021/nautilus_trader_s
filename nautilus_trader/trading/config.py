# -------------------------------------------------------------------------------------------------
#  Copyright (C) 2015-2021 Nautech Systems Pty Ltd. All rights reserved.
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

import importlib
import importlib.util
import sys
from importlib.machinery import ModuleSpec
from types import ModuleType
from typing import Optional, Union

import pydantic

from nautilus_trader.core.correctness import PyCondition
from nautilus_trader.trading.strategy import TradingStrategy


class TradingStrategyConfig(pydantic.BaseModel):
    """
    The base model for all trading strategy configurations.

    order_id_tag : str
        The unique order ID tag for the strategy. Must be unique
        amongst all running strategies for a particular trader ID.
    oms_type : OMSType
        The order management system type for the strategy. This will determine
        how the `ExecutionEngine` handles position IDs (see docs).
    """

    order_id_tag: str = "000"
    oms_type: str = "HEDGING"


class StrategyFactory:
    """
    Provides strategy creation from importable configurations.
    """

    @staticmethod
    def create(config: "ImportableStrategyConfig") -> TradingStrategy:
        """
        Create a trading strategy from the given configuration.

        Parameters
        ----------
        config : ImportableStrategyConfig
            The configuration for the building step.

        Returns
        -------
        TradingStrategy

        Raises
        ------
        TypeError
            If config is not of type `ImportableStrategyConfig`.

        """
        PyCondition.type(config, ImportableStrategyConfig, "config")
        if (config.path is None or config.path.isspace()) and (
            config.source is None or config.source.isspace()
        ):
            raise ValueError("both `source` and `path` were None")

        if config.path is not None:
            mod = importlib.import_module(config.module)
            cls = getattr(mod, config.cls)
            assert isinstance(config.config, TradingStrategyConfig)
            return cls(config=config.config)
        else:
            spec: ModuleSpec = importlib.util.spec_from_loader(config.module, loader=None)
            module: ModuleType = importlib.util.module_from_spec(spec)

            exec(config.source, module.__dict__)  # noqa
            sys.modules[config.module] = module


class ImportableStrategyConfig(pydantic.BaseModel):
    """
    Represents the trading strategy configuration for one specific backtest run.

    path : str, optional
        The fully-qualified name of the module.
    source : bytes, optional
        The strategy source code.
    config : Union[TradingStrategyConfig, str]

    """

    path: Optional[str]
    source: Optional[bytes]
    config: Union[TradingStrategyConfig, str]

    def _check_path(self):
        assert self.path, "`path` not set, can't parse module"
        assert ":" in self.path, "Path variable should be of the form: path.to.module:class"

    @property
    def module(self):
        self._check_path()
        return self.path.rsplit(":")[0]

    @property
    def cls(self):
        self._check_path()
        return self.path.rsplit(":")[1]
