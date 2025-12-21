from typing                                                                           import Type
from osbot_utils.type_safe.Type_Safe                                                  import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id       import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Label    import Safe_Str__Label
from mgraph_db.mgraph.domain.Domain__MGraph__Graph                                    import Domain__MGraph__Graph
from mgraph_db.mgraph.index.MGraph__Index                                             import MGraph__Index


class PlantUML__Base(Type_Safe):                                                      # base class for PlantUML renderers
    graph                : Domain__MGraph__Graph              = None                  # the graph being rendered
    index                : MGraph__Index                      = None                  # graph index for lookups

    def safe_id(self, raw_id) -> Safe_Str__Id:                                        # sanitize ID for PlantUML
        if raw_id is None:
            return Safe_Str__Id('node')
        safe_str = str(raw_id).replace('-', '_').replace(' ', '_')                    # replace invalid chars
        safe_str = ''.join(c if c.isalnum() or c == '_' else '_' for c in safe_str)   # keep only valid chars
        if safe_str and safe_str[0].isdigit():                                        # ensure starts with letter
            safe_str = f'n_{safe_str}'
        return Safe_Str__Id(safe_str or 'node')

    def wrap_text(self, text: str, width: int = 40) -> str:                           # wrap text for labels
        if not text or len(text) <= width:
            return text or ''
        words  = text.split()                                                         # split into words
        lines  = []                                                                   # accumulate lines
        line   = ''                                                                   # current line
        for word in words:
            if len(line) + len(word) + 1 <= width:
                line = f'{line} {word}' if line else word
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
        return '\\n'.join(lines)                                                      # PlantUML newline

    def type_name__from__type(self, type_obj: Type) -> Safe_Str__Label:               # extract short type name
        if not type_obj:
            return Safe_Str__Label('Node')
        name = getattr(type_obj, '__name__', str(type_obj))
        # todo: check the performance implications of this for loop
        for prefix in ['Schema__MGraph__', 'Schema__', 'Domain__MGraph__', 'Domain__']:
            if name.startswith(prefix):
                name = name[len(prefix):]
                break
        return Safe_Str__Label(name)

    def escape_label(self, text: str) -> str:                                         # escape special chars in labels
        if not text:
            return ''
        return (text
                .replace('"', '\\"')
                .replace('\n', '\\n')
                .replace('\r', ''))
