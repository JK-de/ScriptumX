from crispy_forms.layout import HTML

scene_tag_list = (
    { 'idx': 0, 'name':'Note',      'img':'app/img/note.png' },
    { 'idx': 1, 'name':'(1)', 'img':'app/img/Variant/v1.png' },
    { 'idx': 2, 'name':'(2)', 'img':'app/img/Variant/v2.png' },
    { 'idx': 3, 'name':'(3)', 'img':'app/img/Variant/v3.png' },
    { 'idx': 4, 'name':'(4)', 'img':'app/img/Variant/v4.png' },
    { 'idx': 5, 'name':'(5)', 'img':'app/img/Variant/v5.png' },
    )

gadget_tag_list = (
    { 'idx': 0, 'name':'Note',      'img':'app/img/note.png' },
    { 'idx': 1, 'name':'Requisite', 'img':'app/img/G/tag/Requisite.png' },
    { 'idx': 2, 'name':'Costume',   'img':'app/img/G/tag/Costume.png' },
    { 'idx': 3, 'name':'MakeUp',    'img':'app/img/G/tag/MakeUp.png' },
    { 'idx': 4, 'name':'Camera',    'img':'app/img/G/tag/Camera.png' },
    { 'idx': 5, 'name':'Gaffer',    'img':'app/img/G/tag/Gaffer.png' },
    { 'idx': 6, 'name':'Grip',      'img':'app/img/G/tag/Grip.png' },
    { 'idx': 7, 'name':'Audio',     'img':'app/img/G/tag/Audio.png' },
    { 'idx': 8, 'name':'Special',   'img':'app/img/G/tag/Special.png' },
    { 'idx': 9, 'name':'Tool',      'img':'app/img/G/tag/Tool.png' },
    { 'idx':10, 'name':'Phyro',     'img':'app/img/G/tag/Phyro.png' },
    { 'idx':11, 'name':'Catering',  'img':'app/img/G/tag/Catering.png' },
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
