from grzemplate import pp, Component, parser, render

@parser.register()
class App(Component):
    tag = "py-app"
    template_str = """
<pd-for iter="{range(10)}">
    <p>
        <pd-for key="j" iter="{range(10)}">
            <span>j: {str(j)} woo</span>
            <pd-if cond="{i == 6 and j == 9}">
                <span>Ha ha {str(i)}{str(j)}</span>
            </pd-if>
        </pd-for>
    </p>
    <span>boo {str(i - 1) + "meh"} woo</span>
</pd-for>
    """
app = App(parser)
print(pp(render(app)))
