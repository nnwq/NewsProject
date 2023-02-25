from django import template

register = template.Library()

bad_words = [
    'fuck',
    'ass'
]


@register.filter(name='censor')
def censor(value):
    for bw in bad_words:
        value = value.replace(bw, bw[0] + '*' + len(bw))
    return value
