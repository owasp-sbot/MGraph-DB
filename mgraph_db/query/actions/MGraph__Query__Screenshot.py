import io
from mgraph_db.mgraph.MGraph                             import MGraph
from mgraph_db.query.MGraph__Query                       import MGraph__Query
from mgraph_db.query.actions.MGraph__Query__Export__View import MGraph__Query__Export__View
from osbot_utils.decorators.methods.cache_on_self        import cache_on_self
from osbot_utils.type_safe.Type_Safe                     import Type_Safe
from osbot_utils.utils.Files                             import file_create_from_bytes

DEFAULT__GRAPH__MARGIN                    = 0.05
DEFAULT__GRAPH__TITLE                     = 'MGraph Query'
DEFAULT__GRAPH__TITLE__SIZE               = 14
DEFAULT__GRAPH__TITLE__COLOR              = 'darkblue'
DEFAULT__GRAPH__TITLE__FONT               = 'Courier' #'Arial'
DEFAULT__GRAPH__BACKGROUND_COLOR         = 'azure'
DEFAULT__SOURCE_GRAPH__BACKGROUND_COLOR  = '#0000FF10'

class MGraph__Query__Screenshot(Type_Safe):
    show_node__type        : bool          = False
    show_node__value       : bool          = False
    show_edge__type        : bool          = False
    show_source_graph      : bool          = True
    graph__margin          : float         = DEFAULT__GRAPH__MARGIN
    graph__title           : str           = DEFAULT__GRAPH__TITLE
    graph__title__color    : str           = DEFAULT__GRAPH__TITLE__COLOR
    graph__title__font     : str           = DEFAULT__GRAPH__TITLE__FONT
    graph__title__size     : int           = DEFAULT__GRAPH__TITLE__SIZE
    graph__background_color: str           = DEFAULT__GRAPH__BACKGROUND_COLOR
    mgraph_query           : MGraph__Query

    def query_export_view(self):
        return MGraph__Query__Export__View(mgraph_query=self.mgraph_query)

    def graph(self):
        return self.query_export_view().export()

    def mgraph(self):
        return MGraph(graph=self.graph())

    @cache_on_self
    def screenshot(self):
        return self.mgraph().screenshot()

    def configure_dot(self, title=None):
        with self.screenshot().export().export_dot() as _:
            _.set_graph__title             (title or self.graph__title  )
            _.set_graph__margin(self.graph__margin)
            _.set_graph__title__font__size (self.graph__title__size     )
            _.set_graph__title__font__name (self.graph__title__font     )
            _.set_graph__title__font__color(self.graph__title__color    )
            _.set_graph__background__color (DEFAULT__SOURCE_GRAPH__BACKGROUND_COLOR)
            if self.show_node__value: _.show_node__value()
            if self.show_node__type : _.show_node__type()
            if self.show_edge__type : _.show_edge__type()
        return self

    # exported_mgraph_graph =
    # exported_mgraph       = MGraph(graph=exported_mgraph_graph)
    # exported_mgraph.screenshot().save_to('test_MGraph__Query.exported.png').dot()

    def create_source_graph_bytes(self):
        screenshot = MGraph(graph=self.mgraph_query.mgraph_data.graph).screenshot()
        with screenshot.export().export_dot() as _:
            if self.show_node__value: _.show_node__value()
            if self.show_node__type : _.show_node__type()
            if self.show_edge__type: _.show_edge__type()
            _.set_graph__margin(self.graph__margin)
            _.set_graph__title("Source Graph")
            _.set_graph__title__font__name (self.graph__title__font     )
            _.set_graph__title__font__color(self.graph__title__color    )
            _.set_graph__background__color (self.graph__background_color)
        bytes__source_graph = screenshot.dot()
        return bytes__source_graph

    def save_to(self, path):

        self.configure_dot()
        if self.show_source_graph:
            bytes__source_graph = self.create_source_graph_bytes()
            bytes__query_graph  = self.screenshot().dot()
            self.merge_images_side_by_side(bytes__source_graph, bytes__query_graph, path)
        else:
            with self.screenshot() as _:
                _.save_to(path)
                _.dot()
                #
        return self



    def merge_images_side_by_side(self, png_bytes1, png_bytes2, save_to_path):
        from PIL                                                 import Image
        # Open images from bytes
        img1 = Image.open(io.BytesIO(png_bytes1))
        img2 = Image.open(io.BytesIO(png_bytes2))

        # Ensure both images have the same height
        if img1.height != img2.height:
            new_height = max(img1.height, img2.height)
            img1 = img1.resize((img1.width, new_height))
            img2 = img2.resize((img2.width, new_height))

        # Create a new image with combined width
        new_width = img1.width + img2.width
        new_img = Image.new("RGBA", (new_width, img1.height))

        # Paste images side by side
        new_img.paste(img1, (0, 0))
        new_img.paste(img2, (img1.width, 0))

        # Save result to bytes
        output = io.BytesIO()
        new_img.save(output, format="PNG")
        new_bytes = output.getvalue()  # Return the new PNG as bytes
        file_create_from_bytes(path=save_to_path, bytes=new_bytes)

