from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def forwards_memberships(apps, schema_editor):
    Project = apps.get_model('X', 'Project')
    ProjectMembership = apps.get_model('X', 'ProjectMembership')

    def perms(role):
        # Keep in sync with X.access.ROLE_PRESETS (historical migration copy).
        empty = {
            t: {'read': False, 'edit': False}
            for t in (
                'project', 'script', 'scene', 'shot', 'role', 'person', 'time',
                'location', 'gadget', 'audio', 'sfx', 'scheduler', 'plan', 'reports',
            )
        }

        def set_tabs(pairs):
            out = {k: dict(v) for k, v in empty.items()}
            for tab, (r, e) in pairs.items():
                out[tab] = {'read': r, 'edit': e}
            return out

        if role == 'actor':
            return set_tabs({
                'script': (True, False),
                'scene': (True, False),
                'reports': (True, False),
            })
        if role == 'writer':
            return set_tabs({
                'script': (True, True),
                'scene': (True, True),
                'role': (True, False),
                'reports': (True, False),
            })
        if role == 'crew':
            return set_tabs({
                'shot': (True, True),
                'location': (True, True),
                'time': (True, True),
                'gadget': (True, True),
                'audio': (True, True),
                'sfx': (True, True),
                'script': (True, False),
                'scene': (True, False),
                'reports': (True, False),
            })
        # producer / director: all
        out = {k: {'read': True, 'edit': True} for k in empty}
        if role == 'director':
            out['person'] = {'read': True, 'edit': False}
        return out

    for project in Project.objects.all():
        seen = set()
        owner_id = getattr(project, 'owner_id', None)
        if owner_id:
            ProjectMembership.objects.get_or_create(
                project=project,
                user_id=owner_id,
                defaults={
                    'role': 'producer',
                    'can_invite': True,
                    'permissions': perms('producer'),
                },
            )
            seen.add(owner_id)
        for u in project.users.all():
            if u.id in seen:
                continue
            ProjectMembership.objects.get_or_create(
                project=project,
                user=u,
                defaults={
                    'role': 'crew',
                    'can_invite': False,
                    'permissions': perms('crew'),
                },
            )
            seen.add(u.id)
        for g in project.guests.all():
            if g.id in seen:
                continue
            ProjectMembership.objects.get_or_create(
                project=project,
                user=g,
                defaults={
                    'role': 'actor',
                    'can_invite': False,
                    'permissions': perms('actor'),
                },
            )
            seen.add(g.id)


def backwards_memberships(apps, schema_editor):
    ProjectMembership = apps.get_model('X', 'ProjectMembership')
    ProjectMembership.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('X', '0003_writer_breakdown_revisions'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(
                    choices=[
                        ('actor', 'Actor'),
                        ('writer', 'Writer'),
                        ('crew', 'Crew'),
                        ('director', 'Director'),
                        ('producer', 'Producer'),
                    ],
                    default='crew',
                    max_length=20,
                )),
                ('can_invite', models.BooleanField(default=False)),
                ('permissions', models.JSONField(blank=True, default=dict)),
                ('project', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='memberships',
                    to='X.project',
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='project_memberships',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'ordering': ['project_id', 'user_id'],
                'unique_together': {('project', 'user')},
            },
        ),
        migrations.RunPython(forwards_memberships, backwards_memberships),
    ]
