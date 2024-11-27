from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Custom filter to retrieve item from a dictionary."""
    return dictionary.get(key)


@register.filter
def get_model_field(model_instance, field_name):
    """
    Retrieve the value of a field from a model instance dynamically.
    Uses getattr to safely access the field's value.
    """
    return getattr(model_instance, field_name, None)
