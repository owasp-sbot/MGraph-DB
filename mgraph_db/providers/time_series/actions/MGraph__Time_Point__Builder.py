from datetime                                                                               import datetime
from typing                                                                                 import Optional
from zoneinfo                                                                               import ZoneInfo
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Time_Point__Create__Data       import Schema__MGraph__Time_Point__Create__Data
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe


class MGraph__Time_Point__Builder(Type_Safe):
    source_id: Obj_Id = None

    def from_datetime(self, dt: datetime) -> Schema__MGraph__Time_Point__Create__Data:              # Creates time point data from datetime object
        if dt.tzinfo is None:                                                                       # Ensure datetime has timezone
            dt = dt.replace(tzinfo=ZoneInfo('UTC'))


        dt_str      = dt.strftime("%a, %d %b %Y %H:%M:%S %z")
        utc_offset  = int(dt.utcoffset().total_seconds() / 60)                                      # Convert to minutes
        offset_str  = f"{'+' if utc_offset >= 0 else ''}{utc_offset}"
        time_zone   = dt.tzinfo.tzname(None) or 'UTC'

        return Schema__MGraph__Time_Point__Create__Data(source_id       = self.source_id     ,
                                                        year            = dt.year            ,
                                                        month           = dt.month           ,
                                                        day             = dt.day             ,
                                                        hour            = dt.hour            ,
                                                        minute          = dt.minute          ,
                                                        second          = dt.second          ,
                                                        timezone        = time_zone          ,
                                                        datetime_obj    = dt                 ,
                                                        datetime_str    = dt_str             ,
                                                        utc_offset      = utc_offset         ,
                                                        utc_offset_str  = offset_str         ,
                                                        timestamp       = int(dt.timestamp()))

    def from_components(self, year   : Optional[int] = None,                                        # Creates time point data from individual components
                              month  : Optional[int] = None,
                              day    : Optional[int] = None,
                              hour   : Optional[int] = None,
                              minute : Optional[int] = None,
                              second : Optional[int] = None,
                              timezone: str = 'UTC') -> Schema__MGraph__Time_Point__Create__Data:

        if all(x is not None for x in [year, month, day, hour, minute]):                           # If we have complete date/time info
            dt = datetime(year, month, day, hour, minute, second or 0, tzinfo=ZoneInfo(timezone))
            return self.from_datetime(dt)

        return Schema__MGraph__Time_Point__Create__Data(year     = year   ,
                                                        month    = month  ,
                                                        day      = day    ,
                                                        hour     = hour   ,
                                                        minute   = minute ,
                                                        second   = second ,
                                                        timezone =timezone)# Return partial data if missing components