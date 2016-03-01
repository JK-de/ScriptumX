from crispy_forms.layout import HTML

gadget_tag_list = (
    { 'bit': 0, 'name':'Requisite', 'img':'app/img/G/tag/Requisite.png' },
    { 'bit': 1, 'name':'Costume',   'img':'app/img/G/tag/Costume.png' },
    { 'bit': 2, 'name':'MakeUp',    'img':'app/img/G/tag/MakeUp.png' },
    { 'bit': 3, 'name':'Camera',    'img':'app/img/G/tag/Camera.png' },
    { 'bit': 4, 'name':'Gaffer',    'img':'app/img/G/tag/Gaffer.png' },
    { 'bit': 5, 'name':'Grip',      'img':'app/img/G/tag/Grip.png' },
    { 'bit': 6, 'name':'Audio',     'img':'app/img/G/tag/Audio.png' },
    { 'bit': 7, 'name':'Special',   'img':'app/img/G/tag/Special.png' },
    { 'bit': 8, 'name':'Tool',      'img':'app/img/G/tag/Tool.png' },
    { 'bit': 9, 'name':'Phyro',     'img':'app/img/G/tag/Phyro.png' },
    { 'bit':10, 'name':'Catering',  'img':'app/img/G/tag/Catering.png' },
    )

all_tag_list = {}
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
        for i in range(12):
            tagStr = '_' + item + '_tag_' + str(i)
            request.session[tagStr] = True
        return

    if tag_id == 'none':
        for i in range(12):
            tagStr = '_' + item + '_tag_' + str(i)
            request.session[tagStr] = False
        return

    try:
        i = int(tag_id)
    except:
        i = -1

    if (i>=0 and i<=11):
        tagStr = '_' + item + '_tag_' + str(i)
        value = request.session.get(tagStr, True)
        value = not value
        request.session[tagStr] = value
        return

def getTagRequestListX(request, item):
    list = []

    for i in range(12):
        tagStr = '_' + item + '_tag_' + str(i)
        value = request.session.get(tagStr, True)
        list.append(value)

    return list

def getTagRequestList(request, group):
    list = []

    for tag in all_tag_list[group]:
        tagItem = {}

        tagItem['bit'] = tag['bit']
        tagItem['name'] = tag['name']
        tagItem['img'] = tag['img']
        
        tagStr = '_' + group + '_tag_' + str(tag['bit'])
        active = request.session.get(tagStr, True)
        tagItem['active'] = active
        
        list.append(tagItem)

    return list
