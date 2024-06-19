from django import template

register = template.Library()

@register.filter
def first_sentence(value):
    sentences = value.split('.')
    if sentences:
        return sentences[0] + '.'  # Ensure the period is included
    return value
