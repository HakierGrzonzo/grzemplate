from lxml.etree import fromstring, tostring

class Component:
    tag = "py-component"
    template_str = "<p>py-component works!<span>boo</span></p>"
    def __init__(self, parser):
        self.parser = parser
        self.parsed = self.parser.parseComponent(self)

    def __repr__(self) -> str:
        return f"<Component {self.tag} @{id(self)}>"

    def getRenderFunc(self, expression):
        def foo():
            return f"// {expression} //"
        return foo

    def render(self):
        res = ""
        for item in self.parsed:
            if isinstance(item, str):
                res += item
            else:
                res += item()
        return res

