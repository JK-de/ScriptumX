"""Session-backed undo stack for scene / scene-item moves."""

SESSION_KEY = 'move_undo_stack'
MAX_STACK = 20


def snapshot_orders(queryset):
    """Return [(id, order), ...] for the current ordered queryset."""
    return [(item.id, item.order) for item in queryset]


def push_undo(request, kind, focus_id, orders):
    """Push a move undo record. kind is 'scene' or 'sceneitem'."""
    stack = list(request.session.get(SESSION_KEY, []))
    stack.append({
        'kind': kind,
        'focus_id': int(focus_id),
        'orders': orders,
    })
    request.session[SESSION_KEY] = stack[-MAX_STACK:]
    request.session.modified = True


def peek_undo(request, kind=None):
    stack = request.session.get(SESSION_KEY, [])
    if not stack:
        return None
    top = stack[-1]
    if kind and top.get('kind') != kind:
        return None
    return top


def pop_undo(request, kind=None):
    stack = list(request.session.get(SESSION_KEY, []))
    if not stack:
        return None
    if kind and stack[-1].get('kind') != kind:
        return None
    entry = stack.pop()
    request.session[SESSION_KEY] = stack
    request.session.modified = True
    return entry


def apply_order_snapshot(model, orders):
    """Restore id→order pairs on model instances."""
    if not orders:
        return 0
    id_to_order = {int(pk): int(order) for pk, order in orders}
    updated = 0
    for obj in model.objects.filter(pk__in=id_to_order.keys()):
        new_order = id_to_order[obj.pk]
        if obj.order != new_order:
            obj.order = new_order
            obj.save(update_fields=['order'])
            updated += 1
    return updated
