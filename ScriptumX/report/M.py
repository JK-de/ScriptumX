from django import template
from django.template.base import TemplateSyntaxError, Node

from itertools import cycle as itertools_cycle

register = template.Library()

class CycleListNode(Node):
    def __init__(self, list_variable, template_variable):
        self.list_variable = list_variable
        self.template_variable = template_variable

    def render(self, context):
        if self not in context.render_context:
            # First time the node is rendered in template
            context.render_context[self] = itertools_cycle(context[self.list_variable])
        cycle_iter = context.render_context[self]
        value = cycle_iter.next()
        if self.template_variable:
            context[self.template_variable] = value
        return ''

@register.tag
def cycle_list(parser, token):
    args = token.split_contents()
    if len(args) != 4 or args[-2] != 'as':
        raise TemplateSyntaxError(u"Cycle_list tag should be in the format {% cycle_list list as variable %}")
    return CycleListNode(args[1], args[3])

class MCell(object):
    text = ''
    color = None
    background_color = None
    symbol = None
    rowRef = None
    colRef = None
    colHeader = False
    rowHeader = False

class MHeader(object):
    text = ''
    color = None
    background_color = None
    symbol = None
    itemX = None
    visible = True


class M(object):
    """description of class"""

    cells = []
    cols = []
    rows = []

    def __init__(self, colListX, rowListX):

        self.cells = []
        self.cols = []
        self.rows = []

        for itemX in colListX:
            header = MHeader()
            try:
                header.text = itemX.name
            except:
                pass
            header.itemX = itemX
            self.cols.append(header)

        for itemX in rowListX:
            header = MHeader()
            try:
                header.text = itemX.name
            except:
                pass
            header.itemX = itemX
            self.rows.append(header)

        i=0
        self.cells.append([])
        cell = MCell()
        cell.colHeader = True
        cell.rowHeader = True
        self.cells[0].append(cell)
        for col in range(len(self.cols)):
            cell = MCell()
            cell.colRef = self.cols[col]
            cell.text = self.cols[col].text
            cell.colHeader = True
            self.cells[0].append(cell)


        for row in range(len(self.rows)):
            self.cells.append([])
            #self.cells[row].header = self.rows[row]
            cell = MCell()
            cell.rowRef = self.rows[row]
            cell.text = self.rows[row].text
            cell.rowHeader = True
            self.cells[row+1].append(cell)
    
            for col in range(len(self.cols)):
                cell = MCell()
                cell.colRef = self.cols[col]
                cell.rowRef = self.rows[row]
                #cell.text = str(i)
                i+=1
                self.cells[row+1].append(cell)


    def getColIndex(self, itemX):
        for col in range(len(self.cols)):
            if itemX == self.cols[col].itemX:
                return col+1
        return None

    def getRowIndex(self, itemX):
        for row in range(len(self.rows)):
            if itemX == self.rows[row].itemX:
                return row+1
        return None



