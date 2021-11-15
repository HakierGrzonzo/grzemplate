from .component import Component
from lxml.html import tostring
from . import parser

class Directive(Component):
    tag = "pd-directive"
    def __init__(self, parser, content, scope, **attrs):
        self._scope = scope
        self.content = content
        self._attrs = attrs
        self._parser = parser

    def _get_env(self):
        return self._scope

    def __repr__(self) -> str:
        return f"<Directive {self.tag} @{id(self)}>"

@parser.register()
class ScopeDirective(Directive):
    tag = "pd-scope"
    def __init__(self, parser, content, scope, **attrs):
        super().__init__(parser, content, scope, **attrs)
        self._parsed = [f"<!-- <{self._attrs.get('tag', self.tag)}> -->"]
        for k, v in self._attrs['pass_scope'].items():
            self._scope[k] = v
        for inner in self._attrs['inner_content']:
            self._parsed += self._parser.parseComponent(self, inner)
        self._parsed.append(f"<!-- </{self._attrs.get('tag', self.tag)}> -->")

@parser.register()
class ForDirective(Directive):
    tag = "pd-for"
    template_str = '<pd-scope pass_scope="{iterator}" inner_content="{content}"></pd-scope>'
    def __init__(self, parser, content, scope, **attrs):
        super().__init__(parser, content, scope, **attrs)
        self._scope["content"] = self.content
        self._iterator = self._attrs['iter']
        self._iterator_key = self._attrs.get("key", "i")
        self._parsed = [f"<!-- <{self._attrs.get('tag', self.tag)}> -->"]
        for x in self._iterator:
            self._parsed += [f"<!-- {self._iterator_key} : {str(x)} -->"]
            self._scope["iterator"] = {self._iterator_key: x}
            self._parsed += self._parser.parseComponent(self)
        self._parsed.append(f"<!-- </{self._attrs.get('tag', self.tag)}> -->")
