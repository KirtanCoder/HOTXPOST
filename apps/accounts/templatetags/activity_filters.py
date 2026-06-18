from django import template

register = template.Library()

ACTION_ICONS = {
    'signup': 'user-plus',
    'login': 'sign-in-alt',
    'logout': 'sign-out-alt',
    'verify': 'check-circle',
    'reject': 'times-circle',
    'block': 'ban',
    'post_create': 'plus-circle',
    'post_edit': 'edit',
    'post_delete': 'trash',
    'post_claim': 'hand-paper',
    'post_complete': 'check',
    'post_approve': 'thumbs-up'
}

@register.filter
def action_icon(action):
    """Return the Font Awesome icon name for a given activity action."""
    return ACTION_ICONS.get(action, 'circle')
