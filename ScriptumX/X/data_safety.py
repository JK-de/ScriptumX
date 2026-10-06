"""
Data-safety helpers for script/scene editors: move undo, autosave, conflict.
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_POST

from X.common import Env, getOrderNumber
from X.conflict import is_stale, token_for
from X.move_undo import apply_order_snapshot, peek_undo, pop_undo, push_undo, snapshot_orders
from X.models import Scene, SceneItem


def perform_scene_move(request, scene_id, offset):
    """Move a Scene within the active script. Returns redirect URL path."""
    env = Env(request)
    scenes = list(Scene.objects.filter(project=env.project_id, script=env.script_id).order_by('order'))
    selected = Scene.objects.get(project=env.project_id, script=env.script_id, id=scene_id)

    offset = int(offset)
    if offset < 0:
        offset -= 1
    if offset > 0:
        offset += 1

    orders = snapshot_orders(scenes)
    new_order = getOrderNumber(scenes, scene_id, offset)
    if new_order:
        push_undo(request, 'scene', scene_id, orders)
        selected.order = new_order
        selected.save()
        messages.success(request, 'Scene moved. Use Undo Move to restore previous order.')
    return '/script/' + str(scene_id)


def perform_sceneitem_move(request, sceneitem_id, offset):
    """Move a SceneItem within the active scene. Returns redirect URL path."""
    env = Env(request)
    items = list(SceneItem.objects.filter(scene=env.scene).order_by('order'))
    selected = SceneItem.objects.get(scene=env.scene, id=sceneitem_id)

    offset = int(offset)
    if offset < 0:
        offset -= 1
    if offset > 0:
        offset += 1

    orders = snapshot_orders(items)
    new_order = getOrderNumber(items, sceneitem_id, offset)
    if new_order:
        push_undo(request, 'sceneitem', sceneitem_id, orders)
        selected.order = new_order
        selected.save()
        messages.success(request, 'Scene item moved. Use Undo Move to restore previous order.')
    return '/scene/' + str(sceneitem_id)


def undo_scene_move(request):
    entry = pop_undo(request, 'scene')
    if not entry:
        messages.warning(request, 'Nothing to undo.')
        return HttpResponseRedirect('/script/')
    apply_order_snapshot(Scene, entry.get('orders') or [])
    messages.success(request, 'Scene order restored.')
    focus = entry.get('focus_id')
    if focus:
        return HttpResponseRedirect('/script/' + str(focus))
    return HttpResponseRedirect('/script/')


def undo_sceneitem_move(request):
    entry = pop_undo(request, 'sceneitem')
    if not entry:
        messages.warning(request, 'Nothing to undo.')
        return HttpResponseRedirect('/scene/')
    apply_order_snapshot(SceneItem, entry.get('orders') or [])
    messages.success(request, 'Scene item order restored.')
    focus = entry.get('focus_id')
    if focus:
        return HttpResponseRedirect('/scene/' + str(focus))
    return HttpResponseRedirect('/scene/')


def can_undo(request, kind):
    return peek_undo(request, kind) is not None


def check_save_conflict(request, obj):
    """
    Return (blocked, message).
    blocked=True means caller should not overwrite unless force_save.
    """
    if not obj or not getattr(obj, 'pk', None):
        return False, None
    expected = request.POST.get('expected_updated_at', '')
    force = bool(request.POST.get('force_save'))
    if is_stale(obj, expected) and not force:
        return True, (
            'This item was changed elsewhere (another tab or user). '
            'Reload to see the latest version, or save again with Force overwrite.'
        )
    return False, None


@login_required
@require_POST
def script_autosave(request, scene_id):
    """AJAX autosave for Scene editor fields."""
    from X.view_script import SceneForm
    from X.forms import NoteForm

    env = Env(request)
    try:
        scene = Scene.objects.get(pk=scene_id, project=env.project_id, script=env.script_id)
    except Scene.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Scene not found'}, status=404)

    blocked, msg = check_save_conflict(request, scene)
    if blocked:
        return JsonResponse({
            'status': 'conflict',
            'message': msg,
            'updated_at': token_for(scene),
        }, status=409)

    form = SceneForm(request.POST or None, instance=scene)
    if not form.is_valid():
        return JsonResponse({'status': 'error', 'message': 'Invalid data', 'errors': form.errors}, status=400)

    note = scene.note
    if note is not None:
        form_note = NoteForm(request.POST or None, instance=note)
        if form_note.is_valid():
            form_note.save()

    saved = form.save()
    return JsonResponse({
        'status': 'ok',
        'updated_at': token_for(saved),
        'message': 'Saved',
    })


@login_required
@require_POST
def scene_autosave(request, sceneitem_id):
    """AJAX autosave for SceneItem editor fields."""
    from X.view_scene import SceneItemForm

    env = Env(request)
    try:
        item = SceneItem.objects.get(pk=sceneitem_id, scene=env.scene)
    except SceneItem.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Scene item not found'}, status=404)

    blocked, msg = check_save_conflict(request, item)
    if blocked:
        return JsonResponse({
            'status': 'conflict',
            'message': msg,
            'updated_at': token_for(item),
        }, status=409)

    form = SceneItemForm(request.POST or None, instance=item)
    if not form.is_valid():
        return JsonResponse({'status': 'error', 'message': 'Invalid data', 'errors': form.errors}, status=400)

    saved = form.save()
    return JsonResponse({
        'status': 'ok',
        'updated_at': token_for(saved),
        'message': 'Saved',
    })
