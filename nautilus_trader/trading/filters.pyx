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

import os
import pytz
import pandas as pd
from cpython.datetime cimport datetime, timedelta
from enum import Enum

from nautilus_trader.core.correctness cimport Condition
from nautilus_trader.core.datetime cimport ensure_utc_timestamp, ensure_utc_index
from nautilus_trader import PACKAGE_ROOT


class ForexSession(Enum):
    UNDEFINED = 0,
    SYDNEY = 1,
    TOKYO = 2,
    LONDON = 3,
    NEW_YORK = 4


cdef class ForexSessionFilter:
    """
    Provides methods to help filter trading strategy rules dependant on Forex session times.
    """

    def __init__(self):
        self.tz_sydney = pytz.timezone('Australia/Sydney')
        self.tz_tokyo = pytz.timezone('Japan')
        self.tz_london = pytz.timezone('Europe/London')
        self.tz_new_york = pytz.timezone('EST')

    cpdef datetime local_from_utc(self, session: ForexSession, datetime utc):
        """
        Return the local datetime from the given session and time_now (UTC).
        
        Parameters
        ----------
        session : ForexSession
        utc : datetime

        Returns
        -------
        datetime
            The converted local datetime.
        
        """
        Condition.type(session, ForexSession, 'session')

        if session == ForexSession.SYDNEY:
            return utc.astimezone(self.tz_sydney)

        if session == ForexSession.TOKYO:
            return utc.astimezone(self.tz_tokyo)

        if session == ForexSession.LONDON:
            return utc.astimezone(self.tz_london)

        if session == ForexSession.NEW_YORK:
            return utc.astimezone(self.tz_new_york)

    cpdef datetime next_start(self, session: ForexSession, datetime utc_now):
        """
        Returns the next session start.
        
        Sydney Session    0700-1600 AEST   Monday to Friday
        Tokyo Session     0900-1800 Japan  Monday to Friday
        London Session    0800-1600 UTC    Monday to Friday
        New York Session  0800-1700 EST    Monday to Friday

        Parameters
        ----------
        session : ForexSession
            The session for the start datetime.
        utc_now : datetime
            The datetime now.

        Returns
        -------
        datetime
            
        """
        Condition.type(session, ForexSession, 'session')

        cdef datetime local_now = self.local_from_utc(session, utc_now)
        cdef datetime start

        # Local days session start
        if session == ForexSession.SYDNEY:
            start = self.tz_sydney.localize(datetime(local_now.year, local_now.month, local_now.day, 7))
        elif session == ForexSession.TOKYO:
            start = self.tz_tokyo.localize(datetime(local_now.year, local_now.month, local_now.day, 9))
        elif session == ForexSession.LONDON:
            start = self.tz_london.localize(datetime(local_now.year, local_now.month, local_now.day, 8))
        elif session == ForexSession.NEW_YORK:
            start = self.tz_new_york.localize(datetime(local_now.year, local_now.month, local_now.day, 8))

        # Already past this days session start
        if local_now > start:
            start += timedelta(days=1)

        # Weekend - next session start becomes next Mondays session start
        if start.weekday() > 4:
            diff = 7 - start.weekday()
            start += timedelta(days=diff)

        return start.astimezone(pytz.utc)

    cpdef datetime prev_start(self, session: ForexSession, datetime utc_now):
        """
        Returns the previous session start.
        
        Sydney Session    0700-1600 AEST   Monday to Friday
        Tokyo Session     0900-1800 Japan  Monday to Friday
        London Session    0800-1600 UTC    Monday to Friday
        New York Session  0800-1700 EST    Monday to Friday
        
        Parameters
        ----------
        session : ForexSession
            The session for the start datetime.
        utc_now : datetime
            The datetime now.

        Returns
        -------
        datetime
            
        """
        Condition.type(session, ForexSession, 'session')

        cdef datetime local_now = self.local_from_utc(session, utc_now)
        cdef datetime start

        # Local days session start
        if session == ForexSession.SYDNEY:
            start = self.tz_sydney.localize(datetime(local_now.year, local_now.month, local_now.day, 7))
        elif session == ForexSession.TOKYO:
            start = self.tz_tokyo.localize(datetime(local_now.year, local_now.month, local_now.day, 9))
        elif session == ForexSession.LONDON:
            start = self.tz_london.localize(datetime(local_now.year, local_now.month, local_now.day, 8))
        elif session == ForexSession.NEW_YORK:
            start = self.tz_new_york.localize(datetime(local_now.year, local_now.month, local_now.day, 8))

        # Prior to this days session start
        if local_now < start:
            start -= timedelta(days=1)

        # Weekend - previous session start becomes last Fridays session start
        if start.weekday() > 4:
            diff = start.weekday() - 4
            start -= timedelta(days=diff)

        return start.astimezone(pytz.utc)

    cpdef datetime next_end(self, session: ForexSession, datetime utc_now):
        """
        Returns the next session end.
        
        Sydney Session    0700-1600 AEST   Monday to Friday
        Tokyo Session     0900-1800 Japan  Monday to Friday
        London Session    0800-1600 UTC    Monday to Friday
        New York Session  0800-1700 EST    Monday to Friday
        
        Parameters
        ----------
        session : ForexSession
            The session for the end datetime.
        utc_now : datetime
            The datetime now.

        Returns
        -------
        datetime
            
        """
        Condition.type(session, ForexSession, 'session')

        cdef datetime local_now = self.local_from_utc(session, utc_now)
        cdef datetime end

        # Local days session end
        if session == ForexSession.SYDNEY:
            end = self.tz_sydney.localize(datetime(local_now.year, local_now.month, local_now.day, 16))
        elif session == ForexSession.TOKYO:
            end = self.tz_tokyo.localize(datetime(local_now.year, local_now.month, local_now.day, 18))
        elif session == ForexSession.LONDON:
            end = self.tz_london.localize(datetime(local_now.year, local_now.month, local_now.day, 16))
        elif session == ForexSession.NEW_YORK:
            end = self.tz_new_york.localize(datetime(local_now.year, local_now.month, local_now.day, 17))

        # Already past this days session end
        if local_now > end:
            end += timedelta(days=1)

        # Weekend - next session end becomes last Mondays session end
        if end.weekday() > 4:
            diff = 7 - end.weekday()
            end += timedelta(days=diff)

        return end.astimezone(pytz.utc)

    cpdef datetime prev_end(self, session: ForexSession, datetime utc_now):
        """
        Returns the previous sessions end.
        
        Sydney Session    0700-1600 AEST   Monday to Friday
        Tokyo Session     0900-1800 Japan  Monday to Friday
        London Session    0800-1600 UTC    Monday to Friday
        New York Session  0800-1700 EST    Monday to Friday
        
        Parameters
        ----------
        session : ForexSession
            The session for end datetime.
        utc_now : datetime
            The datetime now.

        Returns
        -------
        datetime
            
        """
        Condition.type(session, ForexSession, 'session')

        cdef datetime local_now = self.local_from_utc(session, utc_now)
        cdef datetime end

        # Local days session end
        if session == ForexSession.SYDNEY:
            end = self.tz_sydney.localize(datetime(local_now.year, local_now.month, local_now.day, 16))
        elif session == ForexSession.TOKYO:
            end = self.tz_tokyo.localize(datetime(local_now.year, local_now.month, local_now.day, 18))
        elif session == ForexSession.LONDON:
            end = self.tz_london.localize(datetime(local_now.year, local_now.month, local_now.day, 16))
        elif session == ForexSession.NEW_YORK:
            end = self.tz_new_york.localize(datetime(local_now.year, local_now.month, local_now.day, 17))

        # Prior to this days session end
        if local_now < end:
            end -= timedelta(days=1)

        # Weekend - previous session end becomes Fridays session end
        if end.weekday() > 4:
            diff = end.weekday() - 4
            end -= timedelta(days=diff)

        return end.astimezone(pytz.utc)


class NewsImpact(Enum):
    UNDEFINED = 0,
    NONE = 1,
    LOW = 2,
    MEDIUM = 3,
    HIGH = 4


cdef class NewsEvent:
    """
    Represents an economic news event.
    """

    def __init__(
            self,
            datetime timestamp,
            impact,
            name,
            currency):
        """

        Parameters
        ----------
        timestamp : datetime
            The timestamp for the start of the economic news event.
        impact : NewsImpact
            The expected impact for the economic news event.
        name : str
            The name of the economic news event.
        currency : str
            The currency the economic news event is expected to affect.
        """
        self.timestamp = timestamp
        self.impact = impact
        self.name = name
        self.currency = currency


cdef class EconomicNewsEventFilter:
    """
    Provides methods to help filter trading strategy rules based on economic news events.
    """

    def __init__(
            self,
            list currencies not None,
            list impacts not None,
            str news_csv_path not None='default'):
        """
        Initializes a new instance of the EconomicNewsEventFilter class.

        :param news_csv_path: The path to the short term interest rate data csv.
        """
        if news_csv_path == 'default':
            news_csv_path = os.path.join(PACKAGE_ROOT + '/_data/news/', 'news_events.zip')

        self.currencies = currencies
        self.impacts = impacts

        news_data = ensure_utc_index(pd.read_csv(news_csv_path, parse_dates=True, index_col=0))

        self._news_data = news_data[(news_data['Currency'].isin(currencies))
                                   & news_data['Impact'].isin(impacts)]

    cpdef NewsEvent next_event(self, datetime time_now):
        """
        Returns the next news event matching the initial filter conditions. 
        If there is no next event then returns None.
        
        Parameters
        ----------
        time_now : datetime

        Returns
        -------
        datetime or None
            The datetime of the next news event in the filtered data or None.

        """
        events = self._news_data[self._news_data.index >= ensure_utc_timestamp(time_now)]

        if events.empty:
            return None

        cdef int index = 0
        row = events.iloc[index]
        return NewsEvent(events.index[index], row['Impact'], row['Name'], row['Currency'])

    cpdef NewsEvent prev_event(self, datetime time_now):
        """
        Returns the previous news event matching the initial filter conditions. 
        If there is no next event then returns None.
        
        Parameters
        ----------
        time_now : datetime

        Returns
        -------
        datetime or None
            The datetime of the previous news event in the filtered data or None.

        """
        events = self._news_data[self._news_data.index <= ensure_utc_timestamp(time_now)]
        if events.empty:
            return None

        cdef int index = -1
        row = events.iloc[index]
        return NewsEvent(events.index[index], row['Impact'], row['Name'], row['Currency'])