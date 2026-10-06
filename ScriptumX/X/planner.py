"""
Production planner helpers (F9–F12).

Builds stripboard / day-out-of-days, cast conflict, location grouping,
and progress rollup data from existing Scene / Appointment / Role / Person /
Location models — no new entities.
"""

from collections import defaultdict, OrderedDict

from django.db.models import Prefetch

from X.models import (
    Appointment,
    Appointment2Scene,
    Scene,
    SceneItem,
    Script,
)


def location_ie_label(location):
    """INT/EXT-style label from Location tags (Intern/Extern/Green/Blue)."""
    if location is None:
        return '—'
    parts = []
    if location.tag1:
        parts.append('INT')
    if location.tag2:
        parts.append('EXT')
    if location.tag3:
        parts.append('GREEN')
    if location.tag4:
        parts.append('BLUE')
    if location.tag5:
        parts.append('UNK')
    return '/'.join(parts) if parts else '—'


def strip_tone(location, story_time):
    """Classic stripboard-ish tone from INT/EXT + day/night hour."""
    is_int = bool(location and location.tag1 and not location.tag2)
    is_ext = bool(location and location.tag2)
    hour = story_time.hour if story_time else 12
    is_night = hour < 6 or hour >= 18
    if is_ext and is_night:
        return 'ext-night'
    if is_ext:
        return 'ext-day'
    if is_int and is_night:
        return 'int-night'
    return 'int-day'


def scene_roles(scene):
    """Distinct roles appearing on a scene via SceneItems."""
    roles = []
    seen = set()
    for item in scene.sceneitem_set.all():
        if item.role_id and item.role_id not in seen:
            seen.add(item.role_id)
            roles.append(item.role)
    return roles


def scene_cast_persons(scene):
    """Persons cast via Role.actor for roles used in the scene, plus Scene.persons."""
    persons = OrderedDict()
    for person in scene.persons.all():
        persons[person.id] = person
    for role in scene_roles(scene):
        if role.actor_id and role.actor_id not in persons:
            persons[role.actor_id] = role.actor
    return list(persons.values())


def project_shoot_days(project, script=None):
    """
    Appointments ordered as shoot days, with linked scenes for the script.
    Returns list of dicts: {appointment, date_label, scenes, a2s}.
    """
    scene_items = Prefetch(
        'scene__sceneitem_set',
        queryset=SceneItem.objects.select_related('role', 'role__actor'),
    )
    appointments = (
        Appointment.objects.filter(project=project)
        .prefetch_related(
            Prefetch(
                'appointment2scene_set',
                queryset=Appointment2Scene.objects.select_related(
                    'scene',
                    'scene__story_location',
                    'scene__story_time',
                    'scene__script',
                ).prefetch_related(
                    scene_items,
                    'scene__persons',
                ).order_by('time', 'scene__order'),
            ),
            'persons',
            'meeting_point',
        )
        .order_by('time_all', 'name')
    )

    days = []
    for appt in appointments:
        links = list(appt.appointment2scene_set.all())
        if script is not None:
            links = [a2s for a2s in links if a2s.scene and a2s.scene.script_id == script.id]
        scenes = [a2s.scene for a2s in links if a2s.scene_id]
        if appt.time_all:
            date_label = appt.time_all.strftime('%Y-%m-%d')
            day_key = appt.time_all.date().isoformat()
        else:
            date_label = 'Unscheduled'
            day_key = 'unscheduled-%s' % appt.id
        days.append({
            'appointment': appt,
            'date_label': date_label,
            'day_key': day_key,
            'scenes': scenes,
            'links': links,
            'meeting_point': appt.meeting_point,
            'call_persons': list(appt.persons.all()),
        })
    return days


def unscheduled_scenes(project, script, shoot_days):
    scheduled_ids = set()
    for day in shoot_days:
        for scene in day['scenes']:
            scheduled_ids.add(scene.id)
    qs = Scene.objects.filter(project=project)
    if script:
        qs = qs.filter(script=script)
    return list(
        qs.exclude(id__in=scheduled_ids)
        .select_related('story_location', 'story_time')
        .order_by('order')
    )


def build_stripboard(project, script):
    """F9 — stripboard rows grouped by appointment / shoot day."""
    days = project_shoot_days(project, script)
    strips = []
    for day in days:
        day_strips = []
        for a2s in day['links']:
            scene = a2s.scene
            if not scene:
                continue
            loc = scene.story_location
            day_strips.append({
                'scene': scene,
                'short': scene.short or scene.order,
                'name': scene.name,
                'ie': location_ie_label(loc),
                'location': loc.name if loc else '—',
                'time': a2s.time,
                'duration': a2s.duration or scene.duration,
                'tone': strip_tone(loc, scene.story_time),
                'roles': scene_roles(scene),
            })
        strips.append({
            'day': day,
            'strips': day_strips,
        })
    return {
        'days': strips,
        'unscheduled': [
            {
                'scene': scene,
                'short': scene.short or scene.order,
                'name': scene.name,
                'ie': location_ie_label(scene.story_location),
                'location': scene.story_location.name if scene.story_location else '—',
                'tone': strip_tone(scene.story_location, scene.story_time),
                'roles': scene_roles(scene),
            }
            for scene in unscheduled_scenes(project, script, days)
        ],
    }


def dood_code(day_indices, index, total):
    """Classic day-out-of-days cell codes: SW / W / WF / SWF."""
    if index not in day_indices:
        return ''
    first = min(day_indices)
    last = max(day_indices)
    if first == last:
        return 'SWF'
    if index == first:
        return 'SW'
    if index == last:
        return 'WF'
    return 'W'


def build_dood(project, script):
    """F9 — day-out-of-days matrix: roles × shoot days."""
    days = [d for d in project_shoot_days(project, script) if d['scenes']]
    # Prefetch scene items + roles for DOOD
    role_days = defaultdict(set)  # role_id -> set of day indices
    role_map = OrderedDict()

    for idx, day in enumerate(days):
        for scene in day['scenes']:
            for role in scene_roles(scene):
                role_map[role.id] = role
                role_days[role.id].add(idx)

    # Also include roles with actors even if unused? Only scheduled roles.
    columns = []
    for idx, day in enumerate(days):
        columns.append({
            'index': idx,
            'label': day['date_label'],
            'name': day['appointment'].name,
            'appointment': day['appointment'],
        })

    rows = []
    for role_id, role in role_map.items():
        indices = role_days[role_id]
        cells = [dood_code(indices, i, len(days)) for i in range(len(days))]
        work_days = sum(1 for c in cells if c)
        rows.append({
            'role': role,
            'actor': role.actor,
            'cells': cells,
            'work_days': work_days,
        })

    return {'columns': columns, 'rows': rows, 'day_count': len(days)}


def build_cast_availability(project, script):
    """
    F10 — cast availability vs scene roles.

    For each shoot day / appointment:
    - roles required by linked scenes (via SceneItem.role)
    - actors implied by Role.actor
    - persons listed on the Appointment
    Conflicts:
    - needed: role has actor but actor not on appointment call sheet
    - extra: person on call but not required by any scene role that day
    - overlap: same person booked on two appointments the same calendar day
    """
    days = project_shoot_days(project, script)

    # Overlap map: person_id -> list of (day_key, appointment)
    person_day_bookings = defaultdict(list)
    for day in days:
        if not day['appointment'].time_all:
            continue
        key = day['day_key']
        for person in day['call_persons']:
            person_day_bookings[person.id].append((key, day['appointment']))

    reports = []
    for day in days:
        needed_roles = OrderedDict()
        needed_persons = OrderedDict()
        for scene in day['scenes']:
            for role in scene_roles(scene):
                needed_roles[role.id] = role
                if role.actor_id:
                    needed_persons[role.actor_id] = role.actor
            for person in scene.persons.all():
                needed_persons[person.id] = person

        call_ids = {p.id for p in day['call_persons']}
        needed_ids = set(needed_persons.keys())

        missing = [
            {'person': needed_persons[pid], 'roles': [
                r for r in needed_roles.values() if r.actor_id == pid
            ]}
            for pid in sorted(needed_ids - call_ids)
            if needed_persons[pid]
        ]
        # roles with no actor assigned
        uncast = [r for r in needed_roles.values() if not r.actor_id]

        extras = [p for p in day['call_persons'] if p.id not in needed_ids]

        overlaps = []
        if day['appointment'].time_all:
            for person in day['call_persons']:
                bookings = person_day_bookings.get(person.id, [])
                same_day = [
                    appt for key, appt in bookings
                    if key == day['day_key'] and appt.id != day['appointment'].id
                ]
                for other in same_day:
                    overlaps.append({'person': person, 'other': other})

        reports.append({
            'day': day,
            'needed_roles': list(needed_roles.values()),
            'needed_persons': list(needed_persons.values()),
            'call_persons': day['call_persons'],
            'missing': missing,
            'uncast_roles': uncast,
            'extras': extras,
            'overlaps': overlaps,
            'ok': not missing and not overlaps and not uncast,
        })

    return {'reports': reports}


def build_location_groups(project, script):
    """
    F11 — group scenes by INT/EXT + story_location and suggest shoot-day clusters.
    Suggestion: contiguous order runs at the same location/IE share a day bucket.
    """
    qs = Scene.objects.filter(project=project).select_related(
        'story_location', 'story_time'
    ).order_by('order')
    if script:
        qs = qs.filter(script=script)
    scenes = list(qs)

    groups = OrderedDict()
    for scene in scenes:
        loc = scene.story_location
        ie = location_ie_label(loc)
        loc_name = loc.name if loc else '(no location)'
        loc_id = loc.id if loc else 0
        key = (loc_id, ie, loc_name)
        if key not in groups:
            groups[key] = {
                'location': loc,
                'location_name': loc_name,
                'ie': ie,
                'scenes': [],
            }
        groups[key]['scenes'].append(scene)

    # Contiguous order clusters → suggested shooting days
    suggestions = []
    cluster = []
    prev_key = None
    for scene in scenes:
        loc = scene.story_location
        ie = location_ie_label(loc)
        loc_name = loc.name if loc else '(no location)'
        loc_id = loc.id if loc else 0
        key = (loc_id, ie)
        if prev_key is not None and key != prev_key and cluster:
            suggestions.append(_cluster_suggestion(cluster))
            cluster = []
        cluster.append(scene)
        prev_key = key
    if cluster:
        suggestions.append(_cluster_suggestion(cluster))

    return {
        'groups': list(groups.values()),
        'suggestions': suggestions,
    }


def _cluster_suggestion(scenes):
    loc = scenes[0].story_location
    return {
        'ie': location_ie_label(loc),
        'location_name': loc.name if loc else '(no location)',
        'location': loc,
        'scenes': scenes,
        'scene_count': len(scenes),
        'shorts': [s.short or str(s.order) for s in scenes],
    }


def _avg(values):
    values = list(values)
    if not values:
        return 0
    return int(round(sum(values) / float(len(values))))


def build_progress_dashboard(project, script=None):
    """
    F12 — roll up scene progress sliders to script (and project) percentages.
    """
    scripts = Script.objects.filter(project=project).order_by('name')
    if script:
        scripts = scripts.filter(pk=script.id)

    script_rows = []
    for scr in scripts:
        scenes = list(Scene.objects.filter(project=project, script=scr))
        count = len(scenes)
        row = {
            'script': scr,
            'scene_count': count,
            'progress_script': _avg(s.progress_script for s in scenes),
            'progress_pre': _avg(s.progress_pre for s in scenes),
            'progress_shot': _avg(s.progress_shot for s in scenes),
            'progress_post': _avg(s.progress_post for s in scenes),
            'scenes': [
                {
                    'scene': s,
                    'short': s.short or s.order,
                    'progress_script': s.progress_script,
                    'progress_pre': s.progress_pre,
                    'progress_shot': s.progress_shot,
                    'progress_post': s.progress_post,
                    'overall': _avg([
                        s.progress_script,
                        s.progress_pre,
                        s.progress_shot,
                        s.progress_post,
                    ]),
                }
                for s in scenes
            ],
        }
        row['overall'] = _avg([
            row['progress_script'],
            row['progress_pre'],
            row['progress_shot'],
            row['progress_post'],
        ])
        script_rows.append(row)

    all_scenes = Scene.objects.filter(project=project)
    if script:
        all_scenes = all_scenes.filter(script=script)
    scenes_list = list(all_scenes)
    project_totals = {
        'scene_count': len(scenes_list),
        'progress_script': _avg(s.progress_script for s in scenes_list),
        'progress_pre': _avg(s.progress_pre for s in scenes_list),
        'progress_shot': _avg(s.progress_shot for s in scenes_list),
        'progress_post': _avg(s.progress_post for s in scenes_list),
    }
    project_totals['overall'] = _avg([
        project_totals['progress_script'],
        project_totals['progress_pre'],
        project_totals['progress_shot'],
        project_totals['progress_post'],
    ])

    return {
        'scripts': script_rows,
        'project_totals': project_totals,
    }
