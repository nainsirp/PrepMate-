from django import template

register = template.Library()

@register.filter
def filter_by_category(questions, category):
    """Filter questions by category"""
    return questions.filter(category=category)
