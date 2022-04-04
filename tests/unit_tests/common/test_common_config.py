# -------------------------------------------------------------------------------------------------
#  Copyright (C) 2015-2022 Nautech Systems Pty Ltd. All rights reserved.
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

import pkgutil

import pytest

from nautilus_trader.common.config import ActorConfig
from nautilus_trader.common.config import ActorFactory
from nautilus_trader.common.config import ImportableActorConfig
from tests.test_kit.mocks.actors import MockActor


class TestActorFactory:
    @pytest.mark.skip(reason="WIP")
    def test_create_from_source(self):
        # Arrange
        config = ActorConfig(
            component_id="MyActor",
        )

        source = pkgutil.get_data("tests.test_kit", "mocks.py")
        importable = ImportableActorConfig(
            module="MockActor",
            source=source,
            config=config,
        )

        # Act
        strategy = ActorFactory.create(importable)

        # Assert
        assert isinstance(strategy, MockActor)
        assert repr(config) == "ActorConfig()"

    def test_create_from_path(self):
        # Arrange
        config = ActorConfig(
            component_id="MyActor",
        )
        importable = ImportableActorConfig(
            path="tests.test_kit.mocks.actors:MockActor",
            config=config,
        )

        # Act
        strategy = ActorFactory.create(importable)

        # Assert
        assert isinstance(strategy, MockActor)
        assert repr(config) == "ActorConfig(component_id='MyActor')"