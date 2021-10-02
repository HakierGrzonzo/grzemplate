from lxml.etree import fromstring, tostring
from .component import Component

compnents = {
    Component.tag: Component
}

class Parser():
    def __init__(self, component_dict):
        self.component_dict = component_dict
    
    def register(self):
        def func(component):
            self.component_dict[component.tag] = component
            return component
        return func

    def parseComponent(self, component: Component):
        node = fromstring(component.template_str)
        parsed = self.parseNode(node, component)
        res = []
        str = ""
        for item in parsed:
            if isinstance(item, type(str)):
                str += item
            else:
                res.append(str)
                str = ""
                res.append(item)
        res.append(str)
        return res
    
    def parseExpression(self, text, component):
        first_split = text.split("{")
        res = [first_split[0]]
        if len(first_split) > 1:
            for split in first_split[1:]:
                expr, tail = split.split("}")
                expr_func = component.getRenderFunc(expr)
                res += [expr_func, tail]
        return res


    def parseNode(self, node, component):
        res = []
        if node.tag.startswith("py-"):
            # handle components
            component_class = self.component_dict.get(node.tag, None)
            if component_class is None:
                raise AttributeError(f"Component {node.tag} does not exist")
            attrs = {}
            for k, v in node.items():
                if v.startswith("{") and v.endswith("}"):
                    attrs[k] = component.getRenderFunc(v.strip("{}"))()
                else:
                    attrs[k] = v
            res += component_class(self, **attrs).getParsed()
        else:
            # handle normal tags
            res.append(f"<{node.tag}")
            attrs =  [self.parseExpression(f'{k}="{v}"', component) for k, v in node.items()]
            if len(attrs) > 0:
                for i, attr in enumerate(attrs):
                    if i - 1 != len(attrs):
                        res.append(" ")
                    res += attr
            res.append(">")
            if node.text:
                res += self.parseExpression(node.text, component)
            for child in node:
                res += self.parseNode(child, component)
            res.append(f"</{node.tag}>")
            if node.tail:
                res += self.parseExpression(node.tail, component)
        return res
