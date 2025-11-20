from datetime                                                                           import datetime, UTC
from mgraph_db.mgraph.domain.Domain__MGraph__Node                                       import Domain__MGraph__Node
from mgraph_db.providers.time_series.MGraph__Time_Series                                import MGraph__Time_Series
from mgraph_db.providers.time_series.actions.MGraph__Time_Point__Builder                import MGraph__Time_Point__Builder
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Time_Point__Create__Data   import Schema__MGraph__Time_Point__Create__Data
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Time_Series__Edges         import Schema__MGraph__Time_Series__Edge__Second
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                        import Obj_Id
from osbot_utils.helpers.flows.Flow                                                     import Flow
from osbot_utils.helpers.flows.decorators.task                                          import task


class Flow__Create__MGraph__Time_Point(Flow):
    date_time         : datetime                                 = None
    source_id         : Obj_Id                                   = None
    create_data       : Schema__MGraph__Time_Point__Create__Data = None
    mgraph_time_series: MGraph__Time_Series                      = None
    time_point        : Domain__MGraph__Node                     = None
    png_create        : bool                                     = False
    png_file_name     : str                                      = './flow-time-point.png'

    @task()
    def setup__point__create_data(self):
        if self.date_time is None:
            self.date_time = datetime.now(UTC)
        if self.source_id is None:
            self.source_id = Obj_Id()
        if self.mgraph_time_series is None:
            self.mgraph_time_series = MGraph__Time_Series()

        time_point_builder = MGraph__Time_Point__Builder(source_id=self.source_id)
        self.create_data   = time_point_builder.from_datetime(self.date_time)
        #print(f"creating Time_Point for {self.source_id} on {self.date_time}")

    @task()
    def create_points(self):
        with self.mgraph_time_series.edit() as _:
            #_.create_time_point__from_datetime(self.date_time)
            self.time_point  = _.create_from__datetime(self.date_time)

        # with self.mgraph_time_series.index() as _:
        #     _.print__stats()

    @task()
    def create_png(self):
        if self.png_create:
            with self.mgraph_time_series.screenshot() as _:
                (_.export().export_dot().show_node__value()
                                        .show_edge__type()
                                        .set_edge_to_node__type_fill_color(Schema__MGraph__Time_Series__Edge__Second, 'azure'))
                _.save_to(self.png_file_name)
                _.dot()


    def main(self, date_time: datetime=None, source_id: Obj_Id=None):
        self.date_time = date_time
        self.source_id = source_id

        self.setup__point__create_data()
        self.create_points()
        self.create_png()


