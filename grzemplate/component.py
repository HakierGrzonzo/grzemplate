from lxml.etree import fromstring, tostring

class Component:
    tag = "py-component"
    template_str = "<p>py-component works!<span>{test2.upper()}</span></p>"
    def __init__(self, parser, **attrs):
        self._attrs = attrs
        self.__parser = parser
        self._env = {}
        for x in [globals(), self.__dict__, self._attrs]:
            for k, v in x.items():
                if not k.startswith("_"):
                    self._env[k] = v 
        self.__parsed = self.__parser.parseComponent(self)

    def __repr__(self) -> str:
        return f"<Component {self.tag} @{id(self)}>"

    def getRenderFunc(self, expression):
        compiled = compile(expression.strip(), self.tag, "eval")
        def foo():
            try:
                return eval(compiled, self._env)
            except Exception as e:
                print(
                        f"Exception in {self}, in line:",
                        f"\t{expression.strip()}", sep="\n"
                )
                raise e
        return foo

    def render(self):
        res = ""
        for item in self.__parsed:
            if isinstance(item, str):
                res += item
            else:
                res += item()
        return res

    def getParsed(self):
        return self.__parsed

