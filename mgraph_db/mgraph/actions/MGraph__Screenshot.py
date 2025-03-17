from typing                                         import Type
from mgraph_db.mgraph.actions.MGraph__Export        import MGraph__Export
from mgraph_db.mgraph.domain.Domain__MGraph__Graph  import Domain__MGraph__Graph
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self
from osbot_utils.type_safe.Type_Safe                import Type_Safe
from osbot_utils.utils.Env                          import get_env, not_in_github_action, load_dotenv
from osbot_utils.utils.Files                        import file_create_from_bytes
from osbot_utils.utils.Http                         import url_join_safe, POST_json_get_bytes

ENV_NAME__URL__MGRAPH_DB_SERVERLESS     = 'URL__MGRAPH_DB_SERVERLESS'
PATH__RENDER_MATPLOTLIB                 = '/matplotlib/render-graph'
PATH__RENDER_MERMAID                    = '/web_root/render-mermaid'
PATH__RENDER_DOT                        = '/graphviz/render-dot'
DEFAULT__FILE_NAME__SCREENSHOT__SAVE_TO = './mgraph-screenshot.png'
DEFAULT__URL__LOCAL__MGRAPH_DB_API      = 'http://localhost:8080'


class MGraph__Screenshot(Type_Safe):
    export_class : Type[MGraph__Export]
    graph        : Domain__MGraph__Graph
    target_file  : str = None

    def dot_to_png(self, dot_code):
        return self.create_screenshot__from__dot_code(dot_code=dot_code)

    def dot(self, print_dot_code=False):
        dot_code = self.export().to__dot()
        if print_dot_code:
            print()
            print(dot_code)
        png_bytes = self.dot_to_png(dot_code)
        return png_bytes

    def dot__just_ids(self):
        dot_code  = self.export().to__dot()
        png_bytes = self.dot_to_png(dot_code)
        return png_bytes

    def dot__just_values(self):
        dot_code         = self.export().to__dot(show_value=True, show_edge_ids=False)
        png_bytes = self.dot_to_png(dot_code)
        return png_bytes

    def dot__just_types(self):
        dot_code = self.export().to__dot_types()
        png_bytes = self.dot_to_png(dot_code)
        return png_bytes

    def dot__schema(self):
        dot_code = self.export().to__dot_schema()
        png_bytes = self.dot_to_png(dot_code)
        return png_bytes


    def create_screenshot__from__dot_code(self, dot_code):
        method_path   = PATH__RENDER_DOT
        method_params = {'dot_source': dot_code}
        return self.execute_request(method_path, method_params)

    @cache_on_self
    def export(self):
        return self.export_class(graph=self.graph)

    def handle_response(self, response):
        if type(response) is bytes:
            screenshot_bytes = response
            if self.target_file and screenshot_bytes:
                file_create_from_bytes(self.target_file, screenshot_bytes)
            return screenshot_bytes

    def execute_request(self, method_path, method_params):
        target_url       = self.url__render_method(method_path)
        response         = POST_json_get_bytes(url=target_url, data=method_params)
        screenshot_bytes = self.handle_response(response)
        return screenshot_bytes

    def save(self):
        return self.save_to(DEFAULT__FILE_NAME__SCREENSHOT__SAVE_TO)

    def save_to(self, target_file):
        self.target_file = target_file
        return self

    def url__render_method(self, path):
        return url_join_safe(self.url__render_server(), path)

    def url__render_server(self):
        url = get_env(ENV_NAME__URL__MGRAPH_DB_SERVERLESS)
        if url is None and not_in_github_action():
            url = DEFAULT__URL__LOCAL__MGRAPH_DB_API
        return url

    def load_dotenv(self):
        load_dotenv()
        return self

    def show_edge_id(self):
        self.export().export_dot().show_edge__id()
        return self

    def show_edge_type(self):
        self.export().export_dot().show_edge__type__str()
        return self

    def show_edge_predicate(self):
        self.export().export_dot().show_edge__predicate__str()
        return self

    def show_node_id(self):
        self.export().export_dot().show_node__id()
        return self

    def show_node_value(self):
        self.export().export_dot().show_node__value()
        return self

    def show_node_type(self):
        self.export().export_dot().show_node__type()
        return self