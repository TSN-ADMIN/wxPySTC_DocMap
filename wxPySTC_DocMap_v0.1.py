import wx
import wx.stc as stc

import numpy
import time


def now():
    return int(round(time.time() * 1000))  # milliseconds


class DragZone:
    def __init__(self):
        self.bmp = None
        self.pos = (0, 0)
        self.shown = True

    def HitTest(self, pt):
        return self.GetRect().Contains(pt)

    def GetRect(self):
        return wx.Rect(self.pos, self.bmp.Size)

#INFO, wx.DragImage transparency- · Issue #378 · wxWidgets-Phoenix
#INFO, URL=https://github.com/wxWidgets/Phoenix/issues/378
    def SetTransparency(self, alpha=0x80):
        timer = now()
        img = self.bmp.ConvertToImage()
        if not img.HasAlpha():
            img.InitAlpha()
            for x in range(img.Width):
                for y in range(img.Height):
                    img.SetAlpha(x, y, alpha)
            self.bmp = img.ConvertToBitmap()
            # print('SetTransparency: %6d ms' % (now() - timer))

    def Draw(self, dc):
        # print('  Draw')
        self.SetTransparency(0x80)
        dc.DrawBitmap(self.bmp, self.GetRect()[:2])

#INFO, URL=http://www.informit.com/articles/article.aspx?p=405047
#INFO, Drawing on Bitmaps with wxMemoryDC
    def Resize(self, size):
        # print('Resize')
        # limit zone size
        min_width = min_height = 3
        if size[0] < min_width:
            size = (min_width, size[1])
        if size[1] < min_height:
            size = (size[0], min_height)

        # prepare memory bitmap for drawing
        mdc = wx.MemoryDC()
        self.bmp = wx.Bitmap(size)
        mdc.SelectObject(self.bmp)

        # zone area
        mdc.SetPen(wx.Pen('BLUE', 1, wx.PENSTYLE_SOLID))
        mdc.SetBrush(wx.Brush('#FFE7CE'))
        mdc.DrawRectangle(0, 0, *size)

        # zone line, centered
        x, _, w, h = self.GetRect()
        mid = h // 2
        left = (x, mid)
        right = (w, mid)
        mdc.SetPen(wx.Pen('RED', 1, wx.PENSTYLE_DOT))
        mdc.DrawLine(left, right)

        # zone dot, centered
        mdc.SetPen(wx.Pen('BLUE', 1))
        mdc.SetBrush(wx.Brush('BLUE', wx.BRUSHSTYLE_TRANSPARENT))
        mdc.DrawCircle(w // 2, mid, 2)

        mdc.SelectObject(wx.NullBitmap)


class DocumentMap(stc.StyledTextCtrl):
    def __init__(self, parent, doc):
        super(DocumentMap, self).__init__(parent)
        self.parent = parent
        self.doc = doc

        # create 2nd view referencing editor document
        self.doc.AddRefDocument(self.doc.DocPointer)
        self.SetDocPointer(self.doc.DocPointer)
        self.doc.prev_line = -1

        self.dragImage = None
        self.dragShape = None
        self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))

        zone = DragZone()
        zone.pos = (0, 0)
        self.zone = zone

#TODO,
        # wx.CallLater(1, self.doc.SetFirstVisibleLine, 3500)
        # self.doc.SetFirstVisibleLine(3500)

        self.InitSTC()

        self.parent.Bind(wx.EVT_SIZE, self.Size)
        self.Bind(stc.EVT_STC_PAINTED, self.Paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.LeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.LeftUp)
        self.Bind(wx.EVT_MOTION, self.Motion)
        self.doc.Bind(stc.EVT_STC_UPDATEUI, self.DocPositionChanged)
#TODO, optional use of mouse wheel
        self.Bind(wx.EVT_MOUSEWHEEL, lambda e: e.SetWheelRotation(0))

    def InitSTC(self):
        self.SetZoom(-10)
        self.SetExtraAscent(0)
        self.SetExtraDescent(-1)

        self.UsePopUp(False)

        mlh = False  # marker line background colour
        self.SetMarginWidth(0, 0)
        self.SetMarginWidth(1, 0 if mlh else 1)
        self.SetMarginWidth(2, 0)
        self.SetIndentationGuides(stc.STC_IV_NONE)

        # no scrollbars
        self.SetUseHorizontalScrollBar(False)
        self.SetUseVerticalScrollBar(False)
        self.SetScrollWidthTracking(False)

        # hide caret
        self.SetCaretWidth(0)
        self.SetReadOnly(True)
        self.doc.SetReadOnly(False)
        # self.Enable(False)

        self.doc.Styling(self)

    def Size(self, evt):
        # print('Size', self.doc.ClientSize, self.ClientSize)
        self.SetSize(self.parent.Size)
#TODO, ##################################################################
        self.zone.Resize((self.ClientSize[0], self.doc.LinesOnScreen() * self.TextHeight(0)))  # wrong size at startup!
        # keep zone inside window
        x, y, w, h = self.zone.GetRect()
        if y + h > self.ClientSize[1] - self.TextHeight(0):
            self.SetFirstVisibleLine(self.FirstVisibleLine + 1)
            self.zone.pos = (x, y - self.TextHeight(0))
        self.Refresh()

    def Paint(self, evt):
        # print('Paint', self.doc.ClientSize, self.ClientSize)
        self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))  # sometimes text insert cursor shows
        self.zone.Resize((self.ClientSize[0], self.doc.LinesOnScreen() * self.TextHeight(0)))  # wrong size at startup: hack
#TODO,
        dc = wx.PaintDC(self)
        if self.zone.shown:
            self.zone.Draw(dc)

    def LeftDown(self, evt):
        # print('LeftDown', self.doc.ClientSize, self.ClientSize)
        pos = evt.Position
        # Did the mouse go down on drag zone?
        zone = self.zone if self.zone.HitTest(pos) else None

        # If a shape was 'hit', then set that as the shape we're going to
        # drag around. Get our start position. Dragging has not yet started.
        # That will happen once the mouse moves, OR the mouse is released.
        if zone:
            self.dragShape = zone
            self.dragStartPos = pos
            self.doc.Bind(stc.EVT_STC_UPDATEUI, None)
            return

        # calculate drag zone position and top line; use numpy (and add 1) for more precision
        self.SetHeights()
#TODO, ##################################################################
        clicked_line = self.FirstVisibleLine - (self.zone.GetRect()[3] // 2 - pos[1]) // self.TextHeight(0)
        # print(clicked_line)
        top_y = clicked_line * self.scroll_height / (self.LineCount - self.doc.LinesOnScreen())
#TODO,
        top_line = numpy.longdouble(top_y / self.scroll_height * (self.LineCount - self.LinesOnScreen()))

        self.doc.SetFirstVisibleLine(top_line + top_y // self.TextHeight(0))

        self.SyncMap(top_line, top_y)

    def LeftUp(self, evt):
        # print('LeftUp', self.doc.ClientSize, self.ClientSize)
        if not self.dragImage or not self.dragShape:
            self.dragImage = None
            self.dragShape = None
            return

        self.doc.Bind(stc.EVT_STC_UPDATEUI, self.DocPositionChanged)

        # adjust mouse pointer position
        self.WarpPointer(self.dragStartPos[0], evt.Position[1])

        # Hide the image, end dragging, and nuke out the drag image.
        self.dragImage.EndDrag()
        self.dragImage = None

        # adjust position when released past top/bottom edge
        top_y = self.dragShape.pos[1] + evt.Position[1] - self.dragStartPos[1]
        if top_y < 0:
            top_y = 0
        if top_y + self.zone.GetRect()[3] > self.ClientSize[1]:
            top_y = self.ClientSize[1] - self.zone.GetRect()[3]
        self.dragShape.pos = (0, top_y)

        self.dragShape.shown = True
        self.RefreshRect(self.zone.GetRect(), True)
        self.dragShape = None

    def Motion(self, evt):
        # print('Motion', self.doc.ClientSize, self.ClientSize)
        # Ignore mouse movement if we're not dragging.

#TODO, show line number on hover
        # self.SetToolTip(str(self.FirstVisibleLine + evt.Position[1] // self.TextHeight(0)))
        # print(self.FirstVisibleLine + evt.Position[1] // self.TextHeight(0))
#TODO,

        if not self.dragShape or not evt.Dragging() or not evt.LeftIsDown():
            return

        # if we have a shape, but haven't started dragging yet
        if self.dragShape and not self.dragImage:
            pos = evt.Position

            # refresh window area where the shape was so it will get erased.
            self.dragShape.shown = False
            self.RefreshRect(self.zone.GetRect(), True)
            self.Update()

            item = self.dragShape.bmp
            self.dragImage = wx.DragImage(item, wx.Cursor(wx.CURSOR_HAND))
            self.hotspot = self.dragStartPos - self.dragShape.pos

            self.dragImage.BeginDrag(self.hotspot, self, True, wx.Rect(0, 0, 300, 300))
            self.dragImage.Move(pos)
            self.dragImage.Show()
        elif self.dragShape and self.dragImage:
            # now move it and show it again if needed
            # keep position aligned with drag start
            pos = (self.dragStartPos[0], evt.Position[1])

            # drag zone's top/bottom Y coordinates
            self.SetHeights()
            top_y = self.dragShape.pos[1] + evt.Position[1] - self.dragStartPos[1]
            bot_y = top_y + self.zone_height

            # adjust position when dragging past top/bottom edge
            if top_y < 0:
                top_y = 0
                pos = (self.dragStartPos[0], self.hotspot[1])
            if bot_y > self.max_height:
                bot_y = self.max_height
                pos = (self.dragStartPos[0], self.scroll_height + self.hotspot[1])

            top_line = int(top_y / self.scroll_height * (self.LineCount - self.LinesOnScreen()))

            self.SetFirstVisibleLine(top_line)  # in document map

            if self.max_height < self.clt_height:
                top_line = 0

            self.doc.SetFirstVisibleLine(top_line + top_y // self.TextHeight(0))  # in editor

            # adjust mouse pointer position
            self.WarpPointer(*pos)

            self.dragImage.Move(pos)
            self.dragImage.Show()

    def DocPositionChanged(self, evt):
        # print('DocPositionChanged', self.doc.ClientSize, self.ClientSize)
        # skip refresh
        if (self.doc.prev_line == self.doc.FirstVisibleLine
            and self.doc.FirstVisibleLine != 0
            and self.doc.CurrentLine != self.LineCount - 1):
            return

        self.doc.prev_line = self.doc.FirstVisibleLine

        # calculate drag zone position and top line; use numpy (and add 1) for more precision
        self.SetHeights()
        top_y = self.doc.FirstVisibleLine * self.scroll_height / (self.LineCount - self.doc.LinesOnScreen())
        top_line = numpy.longdouble(top_y / self.scroll_height * (self.LineCount - self.LinesOnScreen())) + 1

        self.SyncMap(top_line, top_y)

    def SetHeights(self):
        # print('SetHeights', self.doc.ClientSize, self.ClientSize)
        # calculate document map scroll height
        txt_height = self.LineCount * self.TextHeight(0)
        self.clt_height = self.ClientSize[1]
        self.max_height = txt_height if txt_height < self.clt_height else self.clt_height
        self.zone_height = self.zone.GetRect()[3]
        self.scroll_height = self.max_height - self.zone_height

    def SyncMap(self, top_line, top_y):
        # print('SyncMap', self.doc.ClientSize, self.ClientSize)
        self.RefreshRect(self.zone.GetRect(), True)
        self.SetFirstVisibleLine(top_line)
        self.zone.pos = (0, top_y)
        self.Refresh()


class DocumentEditor(stc.StyledTextCtrl):
    def __init__(self, parent):
        super(DocumentEditor, self).__init__(parent)
        self.parent = parent
        self.InitSTC()
        self.parent.Bind(wx.EVT_SIZE, self.Size)

    def InitSTC(self):
        self.SetMarginType(0, stc.STC_MARGIN_NUMBER)  # 0: LINE numbers
        self.SetMarginWidth(0, 50)
        self.SetMarginType(3, stc.STC_MARGIN_TEXT)    # 3: LEFT
        self.SetMarginLeft(4)
        self.SetSelForeground(True, '#FFFFFF')
        self.SetSelBackground(True, '#3399FF')
        self.SetSelAlpha(256)

        self.LoadFile('.\SPyE - Copy.py')

        self.Styling(self)

    def Styling(self, doc):
        doc.StyleSetSpec(stc.STC_STYLE_DEFAULT, 'face:Courier New,size:10')
        doc.StyleSetBackground(stc.STC_STYLE_DEFAULT, '#E6F2FF')
        doc.StyleClearAll()  # reset all styles to default

        # example language: Python
        STYLE = {
            'Default|0': "fore:#000000,face:Courier New,size:10",
            'String single quoted|4': "fore:#CF0000,face:Courier New,size:10",
            'Class name|8': "fore:#0000FF,bold,underline,size:10",
            'Comment 1|12': "fore:#7F7F7F,size:10",
            'Comment 2|1': "fore:#007F00,face:Consolas,size:10",
            'Function name|9': "fore:#007F7F,bold,size:10",
            'Identifier|11': "fore:#0000FF,face:Courier New,size:10",
            'Number|2': "fore:#007F7F,size:10",
            'Operator|10': "fore:#D66100,bold,size:10",
            'String double quoted|3': "fore:#7F007F,face:Courier New,size:10",
            'String double quoted at EOL|13': "fore:#000000,face:Courier New,back:#E0C0E0,eol,size:10",
            'String triple single quotes|6': "fore:#7F0000,size:10",
            'String triple double quotes|7': "fore:#7F0000,size:10",
            'Keyword|5': "fore:#00007F,bold,size:10",
            'Keyword 2|14': "fore:#FF40FF,bold,size:10",
        }

        doc.SetLexer(stc.STC_LEX_PYTHON)
        lng = [stc.STC_LEX_PYTHON, 'python', 'Python']
        lng = '|'.join(map(str, lng))
        # style code elements for current language
        for elem in STYLE.keys():
            _, tok = elem.split('|')
            sty = STYLE[elem]
            doc.StyleSetSpec(int(tok), sty)

    def Size(self, evt):
        self.SetSize(self.parent.Size)
        self.Refresh()


app = wx.App(redirect=False)
frm = wx.Frame(None, title="wxPython - wx.StyledTextCtrl - DocumentMap Test", pos=(0, 0), size=(500, 1024))

# pnl = wx.Panel(frm, -1)
# dcm = DocumentMap(pnl)

spl = wx.SplitterWindow(frm)
pnl1 = wx.Panel(spl)
pnl2 = wx.Panel(spl)
spl.SplitVertically(pnl1, pnl2, -200)

doc = DocumentEditor(pnl1)
dcm = DocumentMap(pnl2, doc)

# import wx.lib.mixins.inspection as inspection
# wx.lib.inspection.InspectionTool().Show(selectObj=dcm, refreshTree=True)

frm.Show()
app.MainLoop()
