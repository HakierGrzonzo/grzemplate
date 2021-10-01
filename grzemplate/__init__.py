from .parser import Parser, compnents
from .component import Component
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

parser = Parser(compnents)

@parser.register()
class App(Component):
    tag = "py-app"
    template_str = '<div attr="val" test="{doo}">some {here} text here<py-component></py-component>and here<span>doo</span>boo</div>'

app = App(parser)
print(app.parsed)
print(app.render())

