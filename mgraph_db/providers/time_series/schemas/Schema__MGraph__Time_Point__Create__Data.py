from datetime                                                                             import datetime
from typing                                                                               import Type
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Node__Time_Point             import Schema__MGraph__Node__Time_Point
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Node__Value__Timestamp       import Schema__MGraph__Node__Value__Timestamp
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Node__Value__Timezone__Name  import Schema__MGraph__Node__Value__Timezone__Name
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Node__Value__UTC_Offset      import Schema__MGraph__Node__Value__UTC_Offset
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                          import Obj_Id
from osbot_utils.type_safe.Type_Safe                                                      import Type_Safe
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Time_Series__Edges           import \
    Schema__MGraph__Time_Series__Edge__Year, Schema__MGraph__Time_Series__Edge__Month, \
    Schema__MGraph__Time_Series__Edge__Day, Schema__MGraph__Time_Series__Edge__Hour, \
    Schema__MGraph__Time_Series__Edge__Minute, Schema__MGraph__Time_Series__Edge__Second, \
    Schema__MGraph__Time_Series__Edge__Timezone, Schema__MGraph__Time_Series__Edge__UTC_Offset, \
    Schema__MGraph__Time_Series__Edge__Timestamp, Schema__MGraph__Time_Series__Edge__Source_Id



class Schema__MGraph__Time_Point__Create__Data(Type_Safe):          # The data needed for creation
    source_id             : Obj_Id      = None
    year                  : int         = None
    month                 : int         = None
    day                   : int         = None
    hour                  : int         = None
    minute                : int         = None
    second                : int         = None
    timezone              : str         = None

    datetime_obj          : datetime    = None
    datetime_str          : str         = None
    utc_offset            : int         = None
    utc_offset_str        : str         = None
    timestamp             : int         = None

    node_type__time_point : Type[Schema__MGraph__Node__Time_Point             ]                 # Node types
    node_type__timezone   : Type[Schema__MGraph__Node__Value__Timezone__Name  ]
    node_type__utc_offset : Type[Schema__MGraph__Node__Value__UTC_Offset      ]
    node_type__timestamp  : Type[Schema__MGraph__Node__Value__Timestamp       ]

    edge_type__year       : Type[Schema__MGraph__Time_Series__Edge__Year      ]              # Edge types
    edge_type__month      : Type[Schema__MGraph__Time_Series__Edge__Month     ]
    edge_type__day        : Type[Schema__MGraph__Time_Series__Edge__Day       ]
    edge_type__hour       : Type[Schema__MGraph__Time_Series__Edge__Hour      ]
    edge_type__minute     : Type[Schema__MGraph__Time_Series__Edge__Minute    ]
    edge_type__second     : Type[Schema__MGraph__Time_Series__Edge__Second    ]
    edge_type__tz         : Type[Schema__MGraph__Time_Series__Edge__Timezone  ]
    edge_type__utc_offset : Type[Schema__MGraph__Time_Series__Edge__UTC_Offset]
    edge_type__timestamp  : Type[Schema__MGraph__Time_Series__Edge__Timestamp ]
    edge_type__source_id  : Type[Schema__MGraph__Time_Series__Edge__Source_Id ]

