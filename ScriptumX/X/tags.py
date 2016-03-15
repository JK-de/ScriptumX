from crispy_forms.layout import HTML

scene_tag_list = (
    { 'idx': 0, 'name':'Note',      'img':'img/note.png' },
    { 'idx': 1, 'name':'1', 'img':'img/variant/v1.png' },
    { 'idx': 2, 'name':'2', 'img':'img/variant/v2.png' },
    { 'idx': 3, 'name':'3', 'img':'img/variant/v3.png' },
    { 'idx': 4, 'name':'4', 'img':'img/variant/v4.png' },
    { 'idx': 5, 'name':'5', 'img':'img/variant/v5.png' },
    )

gadget_tag_list = (
    { 'idx': 0, 'name':'Note',      'img':'img/note.png' },
    { 'idx': 1, 'name':'Requisite', 'img':'img/g/tag/requisite.png' },
    { 'idx': 2, 'name':'Costume',   'img':'img/g/tag/costume.png' },
    { 'idx': 3, 'name':'MakeUp',    'img':'img/g/tag/makeUp.png' },
    { 'idx': 4, 'name':'Camera',    'img':'img/g/tag/camera.png' },
    { 'idx': 5, 'name':'Gaffer',    'img':'img/g/tag/gaffer.png' },
    { 'idx': 6, 'name':'Grip',      'img':'img/g/tag/grip.png' },
    { 'idx': 7, 'name':'Audio',     'img':'img/g/tag/audio.png' },
    { 'idx': 8, 'name':'Special',   'img':'img/g/tag/special.png' },
    { 'idx': 9, 'name':'Tool',      'img':'img/g/tag/tool.png' },
    { 'idx':10, 'name':'Phyro',     'img':'img/g/tag/phyro.png' },
    { 'idx':11, 'name':'Catering',  'img':'img/g/tag/catering.png' },
    )

all_tag_list = {}
all_tag_list['scene'] = scene_tag_list
all_tag_list['gadget'] = gadget_tag_list


def FormSymbol(imageName):
    htmlLine = '{% load staticfiles %}<img src="{% static "'
    htmlLine += imageName
    htmlLine += '" %}" />'
    return HTML(htmlLine)

def handleTagRequest(request, tag_id, item):
    
    if tag_id == None:
        return

    if tag_id == 'all':
        for i in range(13):
            tagStr = '_' + item + '_tag_' + str(i)
            request.session[tagStr] = True
        return

    if tag_id == 'none':
        for i in range(13):
            tagStr = '_' + item + '_tag_' + str(i)
            request.session[tagStr] = False
        return

    try:
        i = int(tag_id)
    except:
        i = -1

    if (i>=0 and i<=12):
        tagStr = '_' + item + '_tag_' + str(i)
        value = request.session.get(tagStr, True)
        value = not value
        request.session[tagStr] = value
        return

def getTagRequestListX(request, item):
    list = []

    for i in range(13):
        tagStr = '_' + item + '_tag_' + str(i)
        value = request.session.get(tagStr, True)
        list.append(value)

    return list

def getTagRequestList(request, group):
    list = []

    for tag in all_tag_list[group]:
        tagItem = {}

        tagItem['idx'] = tag['idx']
        tagItem['name'] = tag['name']
        tagItem['img'] = tag['img']
        
        tagStr = '_' + group + '_tag_' + str(tag['idx'])
        active = request.session.get(tagStr, True)
        tagItem['active'] = active
        
        list.append(tagItem)

    return list
