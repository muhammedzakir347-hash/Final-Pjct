from django import template

register = template.Library()

@register.simple_tag
def t(request, obj, field_base):
    rtl = request.session.get("rtl", False)
    suffix = "_ar" if rtl else "_en"
    return getattr(obj, f"{field_base}{suffix}", "")
