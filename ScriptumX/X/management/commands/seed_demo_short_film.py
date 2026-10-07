"""Seed a clearly named short-film demo project for Live / local testing.

Idempotent for the project name: deletes and recreates "Demo Short Film" only.
Does not wipe other projects.
"""
from datetime import datetime, timedelta, time
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from X.common import ORDER_STEP
from X.models import (
    Appointment,
    Appointment2Scene,
    Audio,
    Gadget,
    Location,
    Person,
    Project,
    Role,
    Scene,
    SceneItem,
    Script,
    SFX,
    Shot,
    Time,
)

PROJECT_NAME = 'Demo Short Film'
SCRIPT_NAME = 'Night Shift'


SCENES = [
    ('INT. RADIO STATION LOBBY - NIGHT', 'Maya arrives late for the overnight shift.'),
    ('INT. CONTROL ROOM - NIGHT', 'First call-in of the night goes sideways.'),
    ('INT. HALLWAY - NIGHT', 'Maya follows a static trail toward Studio B.'),
    ('INT. STUDIO B - NIGHT', 'An empty mic and a voice that should not be there.'),
    ('EXT. STATION ROOFTOP - NIGHT', 'City lights; a transmission dish hums.'),
    ('INT. ARCHIVE ROOM - NIGHT', 'Dusty tapes labeled with tomorrow\'s date.'),
    ('INT. CONTROL ROOM - LATER', 'Signal spikes; callers vanish mid-sentence.'),
    ('INT. BREAK ROOM - NIGHT', 'Coffee, fluorescent buzz, a confession.'),
    ('EXT. ALLEY BEHIND STATION - NIGHT', 'Someone watches the loading dock.'),
    ('INT. CONTROL ROOM - DAWN', 'Sunrise bleed through blinds; last broadcast.'),
]

ROLES = [
    ('MAYA CHEN', 'Night DJ; stubborn, kind, sleep-deprived.'),
    ('JULES ORTEGA', 'Call-in regular who knows too much.'),
    ('STATION MANAGER RUIZ', 'Wants ratings, not ghosts.'),
    ('TECH LEAD SAM', 'Keeps the board alive.'),
    ('THE VOICE', 'Unknown; speaks through dead channels.'),
    ('SECURITY GUARD LEO', 'Night rounds, flashlight, nerves.'),
]

PERSONS = [
    ('Ava Park', 'maya@example.com'),
    ('Diego Morales', 'jules@example.com'),
    ('Kim Ruiz', 'ruiz@example.com'),
    ('Sam Okonkwo', 'sam@example.com'),
    ('Casey Wren', 'voice@example.com'),
    ('Leo Nguyen', 'leo@example.com'),
]

LOCATIONS = [
    'Radio Station Lobby',
    'Control Room',
    'Hallway',
    'Studio B',
    'Rooftop',
    'Archive Room',
    'Break Room',
    'Back Alley',
]

TIMES = [
    (1, 23, 'Clear', 'City hum'),
    (1, 0, 'Fog', 'Distant traffic'),
    (1, 2, 'Overcast', 'Fluorescent buzz'),
    (1, 4, 'Wind', 'Antenna rattle'),
    (1, 6, 'Dawn haze', 'Birds starting'),
]

GADGETS = [
    'Broadcast Console',
    'Headset Mic',
    'Red On-Air Lamp',
    'Cassette Deck',
    'Flashlight',
    'Coffee Mug',
    'Walkie-Talkie',
    'USB Drive',
]

AUDIOS = [
    'Station ID Bed',
    'Phone Ring Loop',
    'Static Wash',
    'City Night Ambience',
    'Rooftop Wind',
    'Tape Hiss Bed',
]

SFXS = [
    'Mic Pop',
    'Door Slam',
    'Static Spike',
    'Footsteps Hall',
    'Glass Clink',
    'Antenna Buzz',
]

DIALOGS = [
    'You hear that? It is not the board.',
    'Keep the fader up. Someone is still on the line.',
    'I told Ruiz the overnight slot was cursed.',
    'Say your name again for the listeners.',
    'We are live whether we like it or not.',
    'Do not cut the call. Not yet.',
    'Studio B has been dark for months.',
    'Then why is the on-air lamp red?',
    'Play the ID. Buy us thirty seconds.',
    'I am not afraid of a ghost. I am afraid of silence.',
    'Check the archive for tonight\'s date.',
    'These tapes are labeled tomorrow.',
    'If tomorrow already spoke, what are we doing?',
    'Sam, talk to me. Is the compressor lying?',
    'Levels look normal. Ears say otherwise.',
    'Jules, if that is you, stop joking.',
    'It is never joking when it knows your name.',
    'Leo, sweep the hallway. Flashlight only.',
    'Copy. Moving.',
    'Whoever you are, the city is listening.',
    'We can dump to tape and walk away.',
    'Walking away is how it got louder.',
    'One more song. Then we open the doors.',
    'Dawn will not save us if we mute it.',
    'Stay with me. On three we go to commercial.',
]

ACTIONS = [
    'Maya taps the VU meter. The needle trembles without input.',
    'A red light flickers, then holds.',
    'She slides a cassette into the deck. It is already warm.',
    'Static blooms across the monitors like frost.',
    'Footsteps pass the door and do not return.',
]


class Command(BaseCommand):
    help = 'Seed Demo Short Film project (~10 scenes, ~25 dialogs each, filled tabs)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--owner',
            default='admin',
            help='Username that owns the demo project (default: admin)',
        )

    def handle(self, *args, **options):
        User = get_user_model()
        owner_name = options['owner']
        try:
            owner = User.objects.get(username=owner_name)
        except User.DoesNotExist:
            owner = User.objects.filter(is_superuser=True).first()
            if not owner:
                raise SystemExit('No suitable owner user found')
            self.stdout.write(self.style.WARNING(
                'Owner %r missing; using %r' % (owner_name, owner.username)
            ))

        deleted, _ = Project.objects.filter(name=PROJECT_NAME).delete()
        if deleted:
            self.stdout.write('Removed previous %r (%s objects)' % (PROJECT_NAME, deleted))

        project = Project.objects.create(name=PROJECT_NAME, owner=owner)
        project.users.add(owner)
        from X.access import ROLE_PRODUCER, ensure_membership
        ensure_membership(project, owner, ROLE_PRODUCER)

        script = Script.objects.create(
            project=project,
            name=SCRIPT_NAME,
            abstract='Overnight radio, wrong numbers, and a voice that arrives early.',
            description='A short film set in a city radio station over one long night.',
            author='ScriptumX Demo',
            version='1.0',
            copyright='Demo content — not for production.',
            revision_label='White',
        )

        persons = []
        for name, email in PERSONS:
            persons.append(Person.objects.create(
                project=project,
                name=name,
                email=email,
                contact='Demo cast',
                abstract='Cast for %s' % SCRIPT_NAME,
            ))

        roles = []
        for i, (name, abstract) in enumerate(ROLES):
            role = Role.objects.create(
                project=project,
                name=name,
                abstract=abstract,
                actor=persons[i % len(persons)],
                color='#FFFFFF',
            )
            role.setAllTags(True)
            role.save()
            roles.append(role)

        locations = []
        for name in LOCATIONS:
            loc = Location.objects.create(
                project=project,
                name=name,
                abstract='Location for %s' % SCRIPT_NAME,
                description='Practical set / location unit.',
            )
            loc.setTag(1, True)
            loc.persons.add(persons[0], persons[1])
            locations.append(loc)

        times = []
        for day, hour, weather, ambient in TIMES:
            t = Time.objects.create(
                project=project,
                name='Day %s %02d:00' % (day, hour),
                day=day,
                hour=hour,
                weather=weather,
                ambient=ambient,
                abstract='%s / %s' % (weather, ambient),
            )
            t.persons.add(persons[0])
            times.append(t)

        gadgets = []
        for name in GADGETS:
            g = Gadget.objects.create(
                project=project,
                name=name,
                abstract='Prop / kit item',
                progress=40,
            )
            g.setTag(2, True)
            gadgets.append(g)

        for role in roles[:3]:
            role.gadgets.add(gadgets[0], gadgets[1])

        audios = []
        for name in AUDIOS:
            a = Audio.objects.create(
                project=project,
                name=name,
                abstract='Audio bed / cue',
                progress=30,
            )
            a.setTag(3, True)
            audios.append(a)

        sfxs = []
        for name in SFXS:
            s = SFX.objects.create(
                project=project,
                name=name,
                abstract='SFX cue',
                progress=25,
            )
            s.setTag(4, True)
            sfxs.append(s)

        script.persons.add(*persons[:4])

        scenes = []
        dialog_count = 0
        item_count = 0
        shot_count = 0
        order = ORDER_STEP
        for idx, (heading, abstract) in enumerate(SCENES):
            scene = Scene.objects.create(
                project=project,
                script=script,
                name=heading[:50],
                short=str(idx + 1),
                abstract=abstract,
                description=abstract + ' Production notes for demo.',
                order=order,
                story_location=locations[idx % len(locations)],
                story_time=times[idx % len(times)],
                progress_script=min(100, 10 * (idx + 1)),
                progress_pre=min(100, 5 * (idx + 1)),
                progress_shot=min(100, 8 * (idx + 1)),
                progress_post=min(100, 3 * (idx + 1)),
            )
            scene.setAllTags(True)
            scene.save()
            scene.persons.add(persons[idx % len(persons)], persons[(idx + 1) % len(persons)])
            scene.gadgets.add(gadgets[idx % len(gadgets)])
            scene.audios.add(audios[idx % len(audios)])
            scene.sfxs.add(sfxs[idx % len(sfxs)])
            scenes.append(scene)
            order += ORDER_STEP

            item_order = ORDER_STEP
            # Opening action
            SceneItem.objects.create(
                scene=scene,
                type='A',
                text=ACTIONS[idx % len(ACTIONS)],
                order=item_order,
            )
            item_order += ORDER_STEP
            item_count += 1

            for d in range(25):
                role = roles[d % len(roles)]
                text = DIALOGS[d % len(DIALOGS)]
                parenthetical = '(into mic)' if d % 5 == 0 else ''
                item = SceneItem.objects.create(
                    scene=scene,
                    type='D',
                    role=role,
                    text=text,
                    parenthetical=parenthetical,
                    order=item_order,
                    gadget=gadgets[d % len(gadgets)] if d % 7 == 0 else None,
                    sfx=sfxs[d % len(sfxs)] if d % 9 == 0 else None,
                )
                item_order += ORDER_STEP
                dialog_count += 1
                item_count += 1

                if d % 6 == 0:
                    SceneItem.objects.create(
                        scene=scene,
                        type='A',
                        text=ACTIONS[(d + idx) % len(ACTIONS)],
                        order=item_order,
                    )
                    item_order += ORDER_STEP
                    item_count += 1

                if d % 11 == 0:
                    # Shot linked to this dialog beat
                    Shot.objects.create(
                        name='S%s-%s' % (idx + 1, d + 1),
                        column=d % 3,
                        length=1,
                        cam_field_size='MS',
                        cam_angle='EYE',
                        description='Coverage on %s' % role.name,
                        sceneitem=item,
                        scene=scene,
                    )
                    shot_count += 1

            # Closing transition
            SceneItem.objects.create(
                scene=scene,
                type='T',
                text='CUT TO:',
                order=item_order,
            )
            item_count += 1

        # Scheduler / appointments across shoot days
        appt_count = 0
        base = timezone.now().replace(hour=9, minute=0, second=0, microsecond=0)
        for i in range(4):
            appt = Appointment.objects.create(
                project=project,
                name='Shoot Day %s — %s' % (i + 1, SCENES[i][0][:20]),
                abstract='Call sheet block for demo.',
                time_all=base + timedelta(days=i),
                duration_all=timedelta(hours=8),
                meeting_point=locations[i % len(locations)],
            )
            appt.setTag(1, True)
            appt.persons.add(persons[i % len(persons)], persons[(i + 1) % len(persons)])
            appt.gadgets.add(gadgets[i % len(gadgets)])
            Appointment2Scene.objects.create(
                appointment=appt,
                scene=scenes[i],
                time=time(9 + i, 0),
                duration=timedelta(hours=2),
            )
            if i + 1 < len(scenes):
                Appointment2Scene.objects.create(
                    appointment=appt,
                    scene=scenes[i + 1],
                    time=time(13, 0),
                    duration=timedelta(hours=2),
                )
            appt_count += 1

        self.stdout.write(self.style.SUCCESS(
            'Seeded %s / %s (project_id=%s script_id=%s)'
            % (PROJECT_NAME, SCRIPT_NAME, project.id, script.id)
        ))
        self.stdout.write(
            'counts scenes=%s dialogs=%s items=%s shots=%s '
            'roles=%s persons=%s times=%s locations=%s '
            'gadgets=%s audios=%s sfxs=%s appointments=%s'
            % (
                len(scenes),
                dialog_count,
                item_count,
                shot_count,
                len(roles),
                len(persons),
                len(times),
                len(locations),
                len(gadgets),
                len(audios),
                len(sfxs),
                appt_count,
            )
        )
        self.stdout.write(
            'Open: /project/%s/%s  or  /p/%s/s/%s/script/'
            % (project.id, script.id, project.id, script.id)
        )
