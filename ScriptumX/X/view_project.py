"""
Definition of views.
"""

from os import path
from datetime import datetime
import random

from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.db.models.functions import Lower

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, ButtonHolder, Div, Field, HTML
from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.utils import render_crispy_form

from django.contrib import messages
from django.http import HttpResponse

from X.models import Project, Script, Scene, ScriptRevision, REVISION_COLOR_CHOICES
from X.forms import NoteForm
from X.common import Env, get_tab_list
from X import backup as project_backup
from X.importer import ImporterBase

from .tags import FormSymbol, handleTagRequest, getTagRequestList

REVISION_PRESETS = REVISION_COLOR_CHOICES

###############################################################################

class ProjectForm(forms.ModelForm):
    """Edit form for Project model"""
    class Meta:
        model = Project
        fields = [
            'name',
            'users',
            'guests',
            'owner',
            ]

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'blueForms'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'
        self.helper.form_tag = False
        self.helper.layout = Layout(

            Field('name', style="width:30em; min-width:30em; max-width:100%; "),

            Field('users', css_class='chosen-select-multi', style="max-width:100%; min-width:100%; min-height:48px;"),

            Field('guests', css_class='chosen-select-multi', style="max-width:100%; min-width:100%; min-height:48px;"),

            Field('owner', css_class='chosen-select-single'),
            )

    def clean_name(self):
      name = self.cleaned_data.get('name')
      return name

###############################################################################

class ScriptForm(forms.ModelForm):
    """Edit form for Script model"""
    class Meta:
        model = Script
        fields = [
            'name',
            'abstract',
            'description',
            'author',
            'version',
            'copyright',
            'revision_label',
            'revision_color',
            'persons',
            ]

    def __init__(self, *args, **kwargs):
        super(ScriptForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'blueForms'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'
        self.helper.form_tag = False
        self.helper.layout = Layout(

            Field('name', style="width:30em; min-width:30em; max-width:100%; "),

            Field('abstract', style="max-width:100%; min-width:100%;", rows=2),

            Field('persons', css_class='chosen-select-multi', style="max-width:100%; min-width:100%; min-height:48px;"),

            Field('author', style="max-width:100%; min-width:100%;"),
            Field('version', style="max-width:100%; min-width:100%;"),
            Field('copyright', style="max-width:100%; min-width:100%;"),

            Field('revision_label', style="max-width:100%; min-width:100%;"),
            Field('revision_color', style="width:10%;", css_class="jscolor {width:243, height:150, position:'right', borderColor:'#FFF', insetColor:'#FFF', backgroundColor:'#666'}"),

            Field('description', style="max-width:100%; min-width:100%;", rows=10),
            )

    def clean_name(self):
      name = self.cleaned_data.get('name')
      return name


IMPORT_FORMAT_CHOICES = (
    ('auto', 'Auto-detect'),
    ('fountain', 'Fountain (.fountain)'),
    ('fdx', 'Final Draft (.fdx)'),
    ('plain', 'Plain text (.txt)'),
    ('celtx', 'Celtx (.celtx)'),
)


class ScriptImportForm(forms.Form):
    """Upload a screenplay file into the current project."""
    script_file = forms.FileField(label='Script file')
    format = forms.ChoiceField(choices=IMPORT_FORMAT_CHOICES, initial='auto', required=False)
    script_name = forms.CharField(max_length=50, required=False, label='Script name (optional)')

    def __init__(self, *args, **kwargs):
        super(ScriptImportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-3'
        self.helper.field_class = 'col-sm-9'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('script_file'),
            Field('format'),
            Field('script_name'),
        )

###############################################################################

@login_required
def project(request, project_id=None, script_id=None):
    """Handles page requests for Projects"""

    env = Env(request, project_id=project_id, script_id=script_id)

    selected_project = None
    selected_script = None
    
    if project_id == '0':
        ### create new project object on request '/project/0'
        selected_project = Project(owner=env.user);
    else:
        try:
            selected_project = Project.objects.get(pk = project_id)
        except ObjectDoesNotExist:
            selected_project = None

        if script_id == '0':
            ### create new project object on request '/project/0'
            if selected_project:
                selected_script = Script(project=selected_project);
            else:
                selected_script = Script(project=env.project);
        else:
            try:
                selected_script = Script.objects.get(pk = script_id)
            except ObjectDoesNotExist:
                selected_script = None


    formItemProject = None
    formItemScript = None
    
    if selected_script:
        
        ### handle buttons
        if request.method == 'POST':
            if not selected_script:   # you shall not pass ... without valid scope
                raise AssertionError 

            # generate forms and/or get data out of the edited forms
            formItemScript = ScriptForm(request.POST or None, instance=selected_script)
            if formItemScript.is_valid():
                selected_script = formItemScript.instance

            # 'Delete'-Button
            if request.POST.get('btn_delete'):
                selected_script.delete()
                return HttpResponseRedirect('/project/' + str(selected_project.id))

            # 'Save'-Button
            if request.POST.get('btn_save'):
                if formItemScript.is_valid():
                    formItemScript.save()

                if script_id == '0':   # previously new item
                    env.setProject(selected_project)
                    env.setScript(selected_script)
                    return HttpResponseRedirect('/project/' + str(selected_project.id) + '/' + str(selected_script.id))

            # Stamp current revision as a named production draft
            if request.POST.get('btn_stamp_revision'):
                if formItemScript.is_valid():
                    formItemScript.save()
                ScriptRevision.objects.create(
                    script=selected_script,
                    label=selected_script.revision_label or 'White',
                    color=selected_script.revision_color or '#FFFFFF',
                    notes=request.POST.get('revision_notes', ''),
                    created_by=env.user,
                )
                messages.success(
                    request,
                    'Stamped revision "%s".' % (selected_script.revision_label or 'White'),
                )
                return HttpResponseRedirect(
                    '/project/' + str(selected_project.id) + '/' + str(selected_script.id)
                )

            # Apply a production color preset (pink/blue pages)
            if request.POST.get('btn_revision_preset'):
                preset = request.POST.get('btn_revision_preset')
                for color, label in REVISION_PRESETS:
                    if color == preset or label.lower() == preset.lower():
                        selected_script.revision_label = label
                        selected_script.revision_color = color
                        selected_script.save()
                        break
                return HttpResponseRedirect(
                    '/project/' + str(selected_project.id) + '/' + str(selected_script.id)
                )

            # 'Activate'-Button
            if request.POST.get('btn_activate'):
                env.setProject(selected_project)
                env.setScript(selected_script)

        else:
            formItemScript = ScriptForm(instance=selected_script)
    
    elif selected_project:

        ### handle buttons
        if request.method == 'POST':
            if not selected_project:   # you shall not pass ... without valid scope
                raise AssertionError 

            # generate forms and/or get data out of the edited forms
            formItemProject = ProjectForm(request.POST or None, instance=selected_project)
            if formItemProject.is_valid():
                selected_project = formItemProject.instance

            # 'Delete'-Button
            if request.POST.get('btn_delete'):
                selected_project.delete()
                return HttpResponseRedirect('/project/')

            # 'Save'-Button
            if request.POST.get('btn_save'):
                if formItemProject.is_valid():
                    formItemProject.save()

                if project_id == '0':   # previously new item
                    return HttpResponseRedirect('/project/' + str(selected_project.id))
        else:
            formItemProject = ProjectForm(instance=selected_project)

    ### conglomerate queries
    
    projects = Project.objects.filter( Q(owner=env.user) | Q(users=env.user) | Q(guests=env.user) ).distinct()

    if selected_project:
        scripts = Script.objects.filter( project=selected_project )
        scenes_project_id = selected_project.id
    else:
        scripts = Script.objects.filter( project=env.project )
        scenes_project_id = env.project_id

    revisions = []
    if selected_script and selected_script.pk:
        revisions = ScriptRevision.objects.filter(script=selected_script)[:20]

    return render(request, 'X/project.html', {
        'title': 'Project',
        'env': env,
        'tab_list': get_tab_list(env),
        'tab_active_id': 'P',
        'projects': projects,
        'scripts': scripts,
        'selected_project': selected_project,
        'selected_script': selected_script,
        'formScript': formItemScript,
        'formProject': formItemProject,
        'scenes_project_id': scenes_project_id,
        'revisions': revisions,
        'revision_presets': REVISION_PRESETS,
        #'error_message': "Please make a selection.",
    })

###############################################################################

@login_required
def project_import(request, project_id=None):
    """Upload Fountain / Final Draft / plain text / Celtx into a project."""

    env = Env(request)

    if project_id:
        try:
            project = Project.objects.get(pk=project_id)
            env.setProject(project)
        except ObjectDoesNotExist:
            messages.error(request, 'Project not found.')
            return HttpResponseRedirect('/project/')

    if not env.project:
        messages.error(request, 'Select a project before importing a script.')
        return HttpResponseRedirect('/project/')

    form = ScriptImportForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        upload = form.cleaned_data['script_file']
        data = upload.read()
        fmt = form.cleaned_data.get('format') or 'auto'
        filename = upload.name or 'upload.txt'

        try:
            imp = ImporterBase(env)
            imported_script = imp.doImport(filename, data=data, fmt=fmt)
            custom_name = (form.cleaned_data.get('script_name') or '').strip()
            if custom_name and imported_script:
                imported_script.name = custom_name[:50]
                imported_script.save()
            messages.success(
                request,
                'Imported "%s" (%d scenes).' % (
                    imported_script.name,
                    Scene.objects.filter(script=imported_script).count(),
                ),
            )
            return HttpResponseRedirect(
                '/project/%s/%s' % (env.project.id, imported_script.id)
            )
        except Exception as exc:
            messages.error(request, 'Import failed: %s' % exc)

    return render(request, 'X/import_script.html', {
        'title': 'Import Script',
        'env': env,
        'tab_list': get_tab_list(env),
        'tab_active_id': 'P',
        'form': form,
        'selected_project': env.project,
    })


###############################################################################

def _user_can_access_project(env, project):
    if not project or not env.user:
        return False
    if env.user.is_superuser or env.user.is_staff:
        return True
    if project.owner_id == env.user.id:
        return True
    if project.users.filter(pk=env.user.id).exists():
        return True
    if project.guests.filter(pk=env.user.id).exists():
        return True
    return False


@login_required
def project_export(request, project_id, fmt='json'):
    """Download a project backup as JSON or ZIP."""
    env = Env(request)
    project = get_object_or_404(Project, pk=project_id)
    if not _user_can_access_project(env, project):
        messages.error(request, 'You do not have access to this project.')
        return HttpResponseRedirect('/project/')

    safe_name = ''.join(c if c.isalnum() or c in '-_' else '_' for c in project.name) or 'project'
    if fmt == 'zip':
        content = project_backup.zip_project(project)
        response = HttpResponse(content, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{safe_name}-backup.zip"'
        return response

    content = project_backup.dumps_project(project)
    response = HttpResponse(content, content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="{safe_name}-backup.json"'
    return response


@login_required
def project_restore(request):
    """Upload a JSON/ZIP backup and create a restored project copy."""
    env = Env(request)

    if request.method == 'POST':
        upload = request.FILES.get('backup_file')
        if not upload:
            messages.error(request, 'Choose a backup JSON or ZIP file to restore.')
            return HttpResponseRedirect('/project/restore')
        try:
            data = project_backup.load_backup_bytes(upload.read(), filename=upload.name)
            project = project_backup.restore_project(data, owner=env.user)
        except Exception as exc:
            messages.error(request, f'Restore failed: {exc}')
            return HttpResponseRedirect('/project/restore')

        env.setProject(project)
        first_script = Script.objects.filter(project=project).first()
        if first_script:
            env.setScript(first_script)
        messages.success(request, f'Restored project "{project.name}".')
        return HttpResponseRedirect('/project/' + str(project.id))

    return render(request, 'X/project_restore.html', {
        'title': 'Restore Backup',
        'env': env,
        'tab_list': get_tab_list(env),
        'tab_active_id': 'P',
    })


###############################################################################
