from lxml.etree import fromstring
from . import parser

@parser.register()
class Component:
    tag = "py-component"
    template_str = "<p>py-component works!<span>{test2.upper()}</span></p>"
    def __init__(self, parser, content = None, **attrs):
        self.content = content
        self._attrs = attrs
        self._parser = parser
        self._parsed = [f"<!-- <{self.tag}> -->"]
        self._parsed += self._parser.parseComponent(self)
        self._parsed.append(f"<!-- </{self.tag}> -->")

    def _get_env(self):
        env = {}
        for x in [globals(), locals(), self._attrs, {'tag': self.tag}]:
            for k, v in x.items():
                if not k.startswith("_"):
                    env[k] = v 
        return env

    def __repr__(self) -> str:
        return f"<Component {self.tag} @{id(self)}>"

    def getRenderFunc(self, expression):
        compiled = compile(expression.strip(), self.tag, "eval")
        def foo():
            try:
                return eval(compiled, self._get_env())
            except Exception as e:
                print(
                        f"Exception in {self}, in line:",
                        f"\t{expression.strip()}", sep="\n"
                )
                raise e
        return foo

    def render(self):
        def sub_render(what) -> str:
            if isinstance(what, list):
                result = ""
                for item in what:
                    if isinstance(item, str):
                        result += item
                    else:
                        subitem = item()
                        if isinstance(subitem, str):
                            result += subitem
                        elif subitem is None:
                            continue
                        else:
                            for x in subitem:
                                result += sub_render(x)
                return result
            elif callable(what):
                return sub_render(what())
            elif isinstance(what, str):
                return what
            else:
                raise Exception("Invalid type returned!")

        return sub_render(self._parsed)

    def getParsed(self):
        return self._parsed

