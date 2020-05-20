import wx
import wx.stc as stc


    ##########################################################################################
    ##########################################################################################

    # ZoneRectRounded = True
    # ZoneRectRoundedRadius = 5
    # ZoneRectLineColour = "#0000FF"
    # ZoneRectLineStyle = 112
    # ZoneRectLineWidth = 1

    # ZoneFillColour = "#FFE7CE"
    # ZoneFillAlpha = 64

    # ZoneCentreLine = True
    # ZoneCentreLineColour = RED
    # ZoneCentreLineStyle = 101
    # ZoneCentreLineWidth = 1

    # ZoneCentreDot = True
    # ZoneCentreDotColour = BLUE
    # ZoneCentreDotRadius = 2

    # ScrollNumLinesWheel = 10
    # ScrollNumLinesEdge = 25
    # ScrollFactorWheel = 11

    # EdgeTextIndicator = True
    # EdgeTextTop = " [ Top ] "
    # EdgeTextBottom = " [ Bottom ] "
    # EdgeTextFont = Courier New
    # EdgeTextForeColour = BLUE
    # EdgeTextBackColour = "#FFD5AA"

    # CursorTypeNormal = 1
    # CursorTypeHover = 19
    # CursorTypeDrag = 6
    # CursorTypeScroll = 24
    # CursorTypeEdge = 11

    # CursorTypeHoverShow = True
    # CursorTypeDragShow = True

    # TooltipHoverShow = True
    # TooltipDragShow = True



    # # use local 'cfg' for convenient short naming
    # cfg = self.cfg['DocumentMap']

    # # zone rectangle, outline and fill
    # dc.SetPen(wx.Pen(cfg['ZoneRectLineColour'], cfg['ZoneRectLineWidth'], cfg['ZoneRectLineStyle']))
    # clr = [int(cfg['ZoneFillColour'][i:i + 2], 16) for i in (1, 3, 5)]  # (r, g, b)
    # clr.append(cfg['ZoneFillAlpha'])  # transparency -> (r, g, b, a)
    # dc.SetBrush(wx.Brush(clr))
    # if cfg['ZoneRectRounded']:
    #     dc.DrawRoundedRectangle(self.zone_rect, cfg['ZoneRectRoundedRadius'])
    # else:
    #     dc.DrawRectangle(self.zone_rect)  # WHEN USING wx.GraphicsContext: dc.DrawRectangle(*self.zone_rect)

    # mid = self.zone_size[1] // 2
    # # zone line, centered
    # if cfg['ZoneCentreLine']:
    #     left = (0, self.zone_startPos[1] + mid)
    #     right = (self.zone_endPos[0], self.zone_endPos[1] - mid)
    #     dc.SetPen(wx.Pen(cfg['ZoneCentreLineColour'], cfg['ZoneCentreLineWidth'], cfg['ZoneCentreLineStyle']))  # , wx.PENSTYLE_DOT
    #     dc.DrawLine(left, right)         # WHEN USING wx.GraphicsContext: dc.DrawLines((left, right))

    # # zone dot, centered
    # if cfg['ZoneCentreDot']:
    #     dc.SetPen(wx.Pen(cfg['ZoneCentreDotColour'], 1))  # , wx.PENSTYLE_DOT
    #     # dc.SetBrush(wx.Brush('BLUE'))
    #     dc.DrawCircle(self.zone_size[0] // 2, self.zone_startPos[1] + mid, cfg['ZoneCentreDotRadius'])

    # # zone text, top/bottom indicator
    # if cfg['EdgeTextIndicator']:
    #     txt = ''
    #     if self.top and self.bof:
    #         txt = cfg['EdgeTextTop']
    #     if self.bot and self.eof:
    #         txt = cfg['EdgeTextBottom']
    # #FIX, cfg['DocumentMap']['Edge...'], fine tuning, EdgeTextPosition
    #     if txt:
    #         dc.SetBackgroundMode(wx.SOLID)  # wx.TRANSPARENT
    #         dc.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, cfg['EdgeTextFont']))
    #         dc.SetTextForeground(cfg['EdgeTextForeColour'])
    #         dc.SetTextBackground(cfg['EdgeTextBackColour'])
    #         wid = dc.GetTextExtent(txt)[0] + 5
    #         dc.DrawText(txt, self.zone_rect[:2] + wx.Point(self.zone_size[0] - wid, 5))

    ##########################################################################################
    ##########################################################################################


class DragZone:
    def __init__(self):
        self.bmp = None
        self.pos = (0, 0)
        self.shown = True

    def Contains(self, pt):
        return self.GetRect().Contains(pt)

    def GetRect(self):
        return wx.Rect(self.pos, self.bmp.Size)

    def Draw(self, dc):
        self.SetTransparency(0x80)
        dc.DrawBitmap(self.bmp, self.GetRect()[:2])

#INFO, wx.DragImage transparency- · Issue #378 · wxWidgets-Phoenix
#INFO, URL=https://github.com/wxWidgets/Phoenix/issues/378
    def SetTransparency(self, alpha=0x80):
        img = self.bmp.ConvertToImage()
        if not img.HasAlpha():
            img.InitAlpha()
            for x in range(img.Width):
                for y in range(img.Height):
                    img.SetAlpha(x, y, alpha)
            self.bmp = img.ConvertToBitmap()

#INFO, URL=http://www.informit.com/articles/article.aspx?p=405047
#INFO, Drawing on Bitmaps with wxMemoryDC
    def Create(self, size):
        # limit zone size
        min_size = 3
        size = (max(min_size, size[0]), max(min_size, size[1]))
        # self.pos = (0, max(0, self.pos[1]))

        # prepare memory bitmap for drawing
        mdc = wx.MemoryDC()
        self.bmp = wx.Bitmap(size)
        mdc.SelectObject(self.bmp)
        # mdc.Clear()

        # zone surface
        mdc.SetPen(wx.Pen('BLUE', 1, wx.PENSTYLE_SOLID))
        mdc.SetBrush(wx.Brush('#FFE7CE'))
        mdc.DrawRectangle(0, 0, *size)  # mdc.DrawRoundedRectangle(0, 0, *size, 5)

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

        # # zone text, top/bottom indicator
        # txt = ''
        # if self.pos[1] <= 0:
        #     txt = ' [ Top ] '
        # if self.pos[1] > 300:
        #     txt = ' [ Bottom ] '
        # if txt:
        #     mdc.SetBackgroundMode(wx.SOLID)  # wx.TRANSPARENT
        #     mdc.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, 'Courier New'))
        #     mdc.SetTextForeground('BLUE')
        #     mdc.SetTextBackground('#FFD5AA')
        #     wid = mdc.GetTextExtent(txt)[0] + 5
        #     mdc.DrawText(txt, (0, 0) + wx.Point(size[0] - wid, 5))

        mdc.SelectObject(wx.NullBitmap)


class DocumentMap(stc.StyledTextCtrl):
    def __init__(self, parent, doc):
        super(DocumentMap, self).__init__(parent)
        self.parent = parent
        self.doc = doc

        # create 2nd view for document
        self.doc.AddRefDocument(self.doc.DocPointer)
        self.SetDocPointer(self.doc.DocPointer)

        self.dragImage = None
        self.dragShape = None
        self.zone = DragZone()
        self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))

        self.InitSTC()

        # wx.CallAfter(self.RefreshZone)

        self.parent.Bind(wx.EVT_SIZE, self.Size)
        self.doc.Bind(stc.EVT_STC_UPDATEUI, self.DocPosChanged)
        self.doc.Bind(stc.EVT_STC_ZOOM, lambda e: self.Refresh())
        self.Bind(stc.EVT_STC_PAINTED, self.Paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.LeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.LeftUp)
        self.Bind(wx.EVT_MOTION, self.Motion)
        # disable map text selection and mouse wheel
        self.Bind(wx.EVT_LEFT_DCLICK, lambda e: e.Skip)
        self.Bind(wx.EVT_MOUSEWHEEL, lambda e: e.SetWheelRotation(0))

    def InitSTC(self):
        self.SetZoom(-10)
        self.SetExtraAscent(0)
        self.SetExtraDescent(-1)

        self.SetDoubleBuffered(True)  # ensure smooth zone drawing
        self.UsePopUp(False)  # disable popup menu

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
        # self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))  # sometimes text insert cursor shows

#TODO, tightly coupled with DocumentEditor!
        self.doc.Styling(self)

    def Size(self, evt):
        self.SetSize(self.parent.Size)
        self.RefreshZone()
        # keep zone inside map
        x, y, _, h = self.zone.GetRect()
        if y + h > self.ClientSize[1] - self.TextHeight(0):
            self.SetFirstVisibleLine(self.FirstVisibleLine + 1)
            self.zone.pos = (x, y - self.TextHeight(0))
        self.Refresh()

    def Paint(self, evt):
        dc = wx.PaintDC(self)
        self.RefreshZone()
        if self.zone.shown:
            self.zone.Draw(dc)

    def LeftDown(self, evt):
        pos = evt.Position
        # If drag zone was 'hit', then set that as the shape we're going to
        # drag around. Get our start position. Dragging has not yet started.
        if self.zone.Contains(pos):
            self.dragShape = self.zone
            self.dragStartPos = pos
            # prevent interfering with drag
            self.doc.Bind(stc.EVT_STC_UPDATEUI, None)
            return

        # center drag zone around clicked line
        self.CalcHeights()
        clicked_line = self.FirstVisibleLine - (self.zone_height // 2 - pos[1]) // self.TextHeight(0)
        top_y = clicked_line * self.GetDocScrollRatio()
        top_y = min(top_y, self.scroll_height)
        top_line = self.GetTopLine(top_y)
        self.SyncDoc(top_line, top_y)
        self.SyncMap(top_line, top_y)

    def LeftUp(self, evt):
        self.SetToolTip('')
        if not self.dragImage or not self.dragShape:
            self.dragImage = None
            self.dragShape = None
            return

        self.doc.Bind(stc.EVT_STC_UPDATEUI, self.DocPosChanged)

        # adjust mouse pointer position
        # self.WarpPointer(self.dragStartPos[0], evt.Position[1])

        # Hide the image, end dragging, and nuke out the drag image.
        self.dragImage.EndDrag()
        self.dragImage = None

        top_y = self.GetTopY(evt.Position[1])
        self.dragShape.pos = (0, top_y)

        self.dragShape.shown = True
        self.RefreshRect(self.zone.GetRect(), True)
        self.dragShape = None

    def Motion(self, evt):
        # Ignore mouse movement if we're not dragging.
        if not self.dragShape or not evt.Dragging() or not evt.LeftIsDown():
            return

        # if we have a shape, but haven't started dragging yet
        if self.dragShape and not self.dragImage:
            pos = evt.Position

            # refresh map area where the drag zone was so it will get erased.
            self.dragShape.shown = False
            self.RefreshRect(self.zone.GetRect(), True)
            self.Update()

            img = self.dragShape.bmp

#TODO, mask zone surface colour
            # mask = wx.Mask(img, '#FFE7CE')
            # img.SetMask(mask)
            # img.SetMaskColour('#FFE7CE')
#TODO,
            # img = wx.Bitmap.FromRGBA(img.Width, img.Height, 0xFF, 0xE7, 0xCE, 0xFF,)
#TODO,
            self.dragImage = wx.DragImage(img, wx.Cursor(wx.CURSOR_HAND))
            self.hotspot = self.dragStartPos - self.dragShape.pos

            self.dragImage.BeginDrag(self.hotspot, self, fullScreen=True)
            self.dragImage.Move(pos)
            self.dragImage.Show()
        # if we have shape and image then move drag zone
        elif self.dragShape and self.dragImage:
            self.CalcHeights()
            top_y = self.GetTopY(evt.Position[1])

            # align position with drag start
            pos = (self.dragStartPos[0], top_y + self.hotspot[1])
            top_line = self.GetTopLine(top_y)
            self.SyncDoc(top_line, top_y)
            self.SetFirstVisibleLine(top_line)  # in document map
            # show line number during drag
            self.SetToolTip('Top Line: %7d' % (self.doc.FirstVisibleLine + 1))

            # adjust mouse pointer position
            self.WarpPointer(*pos)

            self.dragImage.Move(pos)
            self.dragImage.Show()

    def DocPosChanged(self, evt):
        # copy text selection to map
        self.SetSelection(*self.doc.GetSelection())

        self.CalcHeights()
        top_y = self.doc.FirstVisibleLine * self.GetDocScrollRatio()
        top_line = self.GetTopLine(top_y) + 1
        self.SyncMap(top_line, top_y)

    def CalcHeights(self):
        # calculate document map height values
        txt_height = self.LineCount * self.TextHeight(0)
        self.clt_height = self.ClientSize[1]
        self.max_height = min(txt_height, self.clt_height)
        self.zone_height = self.zone.GetRect()[3]
        self.scroll_height = max(.1, self.max_height - self.zone_height)
        # print(txt_height, self.clt_height, self.max_height, self.zone_height, self.scroll_height)

    def GetDocScrollRatio(self):
        ratio = self.doc.LineCount - self.doc.LinesOnScreen()
        # prevent division by zero
        if ratio == 0:
            ratio = -1
        return self.scroll_height / ratio

    def GetTopLine(self, top_y):
        top_line = top_y / self.scroll_height * (self.LineCount - self.LinesOnScreen())
        return top_line

    def GetTopY(self, posY):
        # drag zone's top Y coordinate
        top_y = self.zone.pos[1] + posY - self.dragStartPos[1]
        # prevent 'drag stutter' at top edge
        if top_y < 1:
            top_y = 0
        # adjust position when mouse released past top/bottom edge
        top_y = max(top_y, 0)
        top_y = min(top_y, self.scroll_height)
        return top_y

    def RefreshZone(self):
        self.zone.Create((self.ClientSize[0], self.doc.LinesOnScreen() * self.TextHeight(0)))

    def SyncDoc(self, top_line, top_y):
        if self.max_height < self.clt_height:
            top_line = 0

        self.doc.SetFirstVisibleLine(top_line + top_y // self.TextHeight(0))

    def SyncMap(self, top_line, top_y):
        self.RefreshRect(self.zone.GetRect(), True)
        # adjust map top line
        if top_line == 1:
            top_line = 0
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

#TODO, optional: restore location
        # wx.CallAfter(self.SetFirstVisibleLine, 3500)

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
        # style code elements for current language
        for elem in STYLE.keys():
            _, tok = elem.split('|')
            sty = STYLE[elem]
            doc.StyleSetSpec(int(tok), sty)

    def Size(self, evt):
        self.SetSize(self.parent.Size)
        self.Refresh()


if __name__ == '__main__':
    app = wx.App(redirect=False)
    frm = wx.Frame(None, title="wxPython - wx.StyledTextCtrl - Document Map Demo", pos=(0, 0), size=(500, 1024))

    # pnl = wx.Panel(frm, -1)
    # dcm = DocumentMap(pnl)

    spl = wx.SplitterWindow(frm)
    pn1 = wx.Panel(spl)
    pn2 = wx.Panel(spl)
    spl.SplitVertically(pn1, pn2, -200)

    doc = DocumentEditor(pn1)
#TODO,
    dcm = DocumentMap(pn2, doc)  #, style=Styling)  # 3rd parm: styling function, default: None??

    # import wx.lib.mixins.inspection as inspection
    # wx.lib.inspection.InspectionTool().Show(selectObj=dcm, refreshTree=True)

    frm.Show()
    app.MainLoop()
