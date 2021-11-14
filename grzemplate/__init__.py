from .parser import Parser
from .component import Component
from bs4 import BeautifulSoup as soup
import pathlib
"""
tree = etree.XML('''
    <html>
        <head>
            <title>title</title>
        </head>
    </html>
    ''')

tree[0][0].set("src", "test")
print(etree.tostring(tree, pretty_print=True).decode("utf-8"))
"""

parser = Parser()

"""
@parser.register()
class App(Component):
    tag = "py-app"
    template_str = '<div attr="val">some text here<py-component test="ok" test2="{ \'ok\' }"><strong>{tag.upper()}</strong></py-component>and here<span>doo<em>test</em></span>boo</div>'
"""

def _pp(tree: str) -> str:
    return soup(tree, features='lxml').prettify()
"""
app = App(parser)
print(_pp(app.render()))
"""

def template(location: str) -> str:
    path = pathlib.Path(location).absolute()
    if not location.endswith(".py"):
        raise Exception("Invalid path, pass __file__")
    else:
        path = str(path)[:-3] + ".html"
    return open(path).read()


def render(component: Component) -> str:
    return component.render()

