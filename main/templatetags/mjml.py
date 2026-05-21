import mrml
from django import template

register = template.Library()


class MjmlNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        content = self.nodelist.render(context)
        return mrml.to_html(content).content


@register.tag("mjml")
def do_mjml(parser, token):
    """
    Compile MJML to HTML after Django template rendering.

    Usage:
        {% load mjml %}
        {% mjml %}
        <mjml>
          <mj-body>
            <mj-section>
              <mj-column>
                <mj-text>Hello {{ user.name }}!</mj-text>
              </mj-column>
            </mj-section>
          </mj-body>
        </mjml>
        {% endmjml %}
    """
    nodelist = parser.parse(("endmjml",))
    parser.delete_first_token()
    return MjmlNode(nodelist)
