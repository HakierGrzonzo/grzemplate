from grzemplate.debug import DEBUG
from grzemplate.obfuscator import obfuscate
from .parser import parser
from .component import Component
from .directive import ScopeDirective, ForDirective, Directive
from bs4 import BeautifulSoup as soup
import pathlib

def pp(tree: str) -> str:
    return soup(tree, features='lxml').prettify()

def template(location: str) -> str:
    path = pathlib.Path(location).absolute()
    if not location.endswith(".py"):
        raise Exception("Invalid path, pass __file__")
    else:
        path = str(path)[:-3] + ".html"
    return open(path).read()


def render(component: Component) -> str:
    if DEBUG:
        return component.render()
    else:
        return obfuscate(component.render())

