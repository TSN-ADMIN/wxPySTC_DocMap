#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (
    division,
    absolute_import,
    print_function,
    unicode_literals
)

"""Main SPyE module.

#TODO, module docstring

Scintilla Python based Editor
"""


########################
# LEGEND:
# I = INFO
# n = scheduled NEXT
# p = in PROGRESS
# t = TODO
# v = DONE, solved
# x = FIX
##########
# CHECK concepts:
#   I Read wxPyWiki thoroughly, again!
#     I URL=https://wiki.wxpython.org/
#   I Check 'PEP 8 -- Style Guide for Python Code' for naming conventions
#     I URL=https://www.python.org/dev/peps/pep-0008/
#   v evt.Skip(),
#   v from __future__ import ..., i.e. unicode_literals, absolute_import
#   v wx.EVT_MENU_HIGHLIGHT_ALL
##########
# EXAMPLE editors:
#   I ConText, IDLE, IdleX, Notepad3
#   I DrPython   (contrib\TSNmod-DrPython_3.11.4)
#   I Editra     (   "   \TSNmod-Editra-0.7.20)
#   I PyPE       (   "   \TSNmod-PyPE-2.9.4)
#   I UliPad     (   "   \TSNmod-UliPad-4.2)
#   I peppy      (   "   \TSNmod-peppy-master)
#   I Dabo       (   "   \dabo-0.9.14.zip), URL=https://dabodev.com
#   I SciTE      (   "   \Scintilla-SciTE), URL=http://www.scintilla.org/SciTE.html
#   I Notepad++  (   "   \Notepad++),       URL=https://notepad-plus-plus.org
#   I TextEditor (   "   \TextEditor - wxPython, Scintilla, Macros)
#   I Twistpad   (   "   \Twistpad_Trial.zip)
# USEFUL tools:
#   I code navigation:
#     I universal-ctags (new), ctags (old), CTags (SublimeText plugin/wrapper)
#       URL=https://ctags.io/
#       URL=http://ctags.sourceforge.net
#       URL=https://github.com/SublimeText/CTags
#   I code checking/statistics/metrics:
#     I flake8, pychecker, pylint, pymetrics, importchecker
#     I radon -> radon raw <filename>
#     I prospector
#       pip install prospector
#     I OpenStack Bandit
#       URL=https://github.com/openstack/bandit
#   I duplicate code detection:
#     I clonedigger, PMD CPD, pysonarsq (PySonar2 fork)
#   I code quality:
#     I SonarQube, SonarPython
#   I code documentation:
#     I doxygen, doxypy, doxypypy, epydoc, pdoc, pydoc, sphinx
#       URL=https://wiki.python.org/moin/DocumentationTools
#   I code debugging:
#     I winpdb (1.4.8) - platform independent GPL Python debugger
#       URL=http://winpdb.org/
#     I beeprint - friendly debug printing
#       URL=https://github.com/panyanyany/beeprint
# EXAMPLE preferences:
#   I Pyfa (_SRCREF-TSN-Python-Editor\other\Pyfa-1.32.0.zip)
##########
#NOTE
##########
# v PyInstaller problem: invalid bitmap when running .exe
#   I absolute path 'os.path.join(icoPath, <img_file>)': NO SOLUTION
#   I after refactoring images -> PyEmbeddedImage: NO SOLUTION...
#   I temp replace of switch --windowed with --console in 'SPyE-BuildExe.cmd'
#     I error indicated ImportError in pyclbr._readmodule
#     v SOLVED: add THIS_PTH in call to readmodule_ex
##########
#TODO
##########
# FILE:
#   t optimize method/class integration: _split_path/Editor
#   t Recent Files
# EDITOR:
#-> p ruler UNDER page tab area including cursor position indicator, now ABOVE page tabs
#   t (un)comment code, remove comments
#   t convert text: EOLs, tabs, spaces
#   t fill block, insert code from template
#   t syntax highlighting for currently supported languages
#   t smart indent
#   t macro functionality, enhance...
#   t split hor/ver/top/bot for 2nd view on same file as aui.Notebook lacks that feature
#     I URL=http://proton-ce.sourceforge.net/rc/scintilla/pyframe/www.pyframe.com/stc/mult_views.html
# SEARCH:
#   t implement REGEX, refactor wx.FindReplaceDialog to CUSTOM DIALOG
#     I URL=D:\Dev\D\wx\TSN_SPyE\contrib\demo\demo_SearchSTC.py
#   t check boxes: wrap search, from cursor/top, current file/all files
# BOOKMARKS:
#   t testing + add/delete/list; add 1st free bmarknr when margin clicked?
#   t add line text to jump menu item
#   t Find/Replace DIALOG a la UEStudio/ConTEXT
# TOOLBAR:
#   t customize, context menu
#   t search control usage...
#   t append accelerator to toolbar tooltip text, e.g. 'New (Ctrl+N)':
#     t link TB_ <=> MB_ ids (when we have custom accelerator keys)
#   t label text/font:
#         self.tb.SetWindowStyle(self.tb.WindowStyle <-+> wx.TB_TEXT <-+> wx.TB_NO_TOOLTIPS)
#         self.tb.SetOwnFont(wx.Font(wx.FontInfo(8).Bold().Italic().Underlined()))
#         self.tb.SetOwnFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName='Courier New'))
#         self.tb.Realize()
# STATUSBAR:
#   t customize, context menu
#   t field label text/font
# GENERAL:
#   t Function List: manual refresh and/or autofill on new/open
#     t add global/local functions/variables
#   t ContextMenu for tb and sb DOES NOT SHOW CHECK MARK -> in handler: set explicitly w/ mb.Check
#   t tooltips, global enable/disable, wx.ToolTip demo...
#   t flexible logging Module next to current DEBUG
#   t Replace aui.AuiNotebook by wx.lib.agw.flatnotebook ??
#   t Replace _blink_text/_hover_text by EnhancedStatusBar ??
#   t Command line parameter handling, i.e.: sys.argv, getopt, argparse
#   v Config file handling, i.e.: ConfigObj, ConfigParser
#   t Document Map, code overview in side panel in tiny font
#   t Help System, including Context Sensitive Help
# PREFERENCES:
#   t scan THIS source and config.py for candidate options to configure
#   t keyboard SHORTCUT EDITOR in preferences or under separate menu item
#     I URL="D:\Dev\Python27\Lib\site-packages\wx\lib\agw\shortcuteditor.py"
#   t monitor MOUSE STATE info
#     I URL="D:\Dev\Python27\Lib\site-packages\wx\DEMO\demo\GetMouseState.py"
#   t retrieve system-specific info about all known MIME types and FILENAME EXTENSIONS
#     I URL="D:\Dev\Python27\Lib\site-packages\wx\DEMO\demo\MimeTypesManager.py"
#   t determine STANDARD LOCATION of certain types of files in a platform specific manner
#     I URL="D:\Dev\Python27\Lib\site-packages\wx\DEMO\demo\StandardPaths.py"
##########
#FIX
##########
# x 2017-10-02 => replace '__, doc = self._getPagDoc()' by GLOBAL/self.curdoc
# x submenu item can not be disabled, greyed out
# v (solved): save margin views per DOCUMENT OR GLOBALLY, not both; see _update_margins etc...
# x toggle side panel open/close its respective tool's accelerator key
# x how to replace use of 'self.main' with 'import __main__ as _main'?
# v BUG (solved): error when changing page tab and FunctionList visible
##########
#DONE
##########
# v populate frame w/ empty aui.AuiNotebook
# v populate aui.AuiNotebook w/ 1 editor per page/tab
# v line/column indicator in statusbar -> 3rd field
# v ConvertEOLs(eolMode), like ConTEXT, Tools->Convert Text To...
# v use uihandler to enable/disable menu items: self.mb.Enable(evt.Id, True/False)
# v enable/disable menus View, Search, Format, Macro
# v modal wx.Dialog
# v self.appname + filename in main caption
# v self.ed -> Editor: should be instance of Editor
# v missing statusbar msgs, like Ln/Col indicator
# v STATISTICS (like ConTEXT example)
# v View->Menu Icons DOES NOT SHOW CHECK MARK, it doesn't need one!
# v REFACTOR CODE TO NOTEBOOK ARCHITECTURE, MULTIPLE TABS( =~ DOCS):
# v Function List in side panel => VerSplitter
# v blink statustext while recording -> 2nd statfield
# v show 'Top Line' text while scrolling -> 2nd statfield/hovering @top right
# v various DEBUG enhancements: AUCPL, SCMOD, FIND, KEYBD
# v oeuf...
# v set last find string to selected text
# v add doxygen '\' commands: \example \internal
# v Code Context (like IDLE) in top, Editor in bottom window => HorSplitter
# v add Code Context menu items and methods: view/swap
# v remove SetClientSize functions: splitterwindows size children fine now
# v submenu items ALWAYS SHOW ICONS: solved in BuildSubMenu, added parm2 = icons
# v close unfocused page/tab selects focused tab: solved in PageClose
# v split config into 2 modules: debug, language
# v styling per lexer/language: 1st basic setup
# v find next/prev now uses findflg: solved in SearchFindNext/Prev
# v HighlightMatches: saves last find string
# v language indicator in statusbar -> 5th field
# v styling per lexer/language: refactor 1st basic setup
# v DEBUG: show only active options
# v DEBUG: _dbg_MENU, show all items with accelerator keys
# v find flags indicator in statusbar -> 5th field
# v move 7 menu items (tb, sb, sp, ssp, cc, scc, fs) from View to new Window menu
# v add 3 menu items and methods to Search menu: Case, Word, Backwards
# v also check Case, Word and Backwards menu item from FindReplaceDialog._destroy
# v SearchFindNext/Prev sets findflg down/up; starts FindReplaceDialog when empty find string
# v add DELAY['MSG'], DELAY['SPL']: timeout for SBF['MSG'][0] and splash screen
# v REGEX implementation: 1st setup commented out; search: 'REGEX'
# v add 3 icons for case conversion in Format menu
# v refactor menu and statusbar constant prefixes to 'MB_' and 'SB_'
# v replace 4 FindMenuItem method calls: TOOLBAR, STATUSBAR, SIDE_PANEL, CODE_CONTEXT
# v add 4 MB_WIN_ constants: TOOLBAR, STATUSBAR, SIDE_PANEL, CODE_CONTEXT
# v unresponsive page tab - next to dragged tab - after horizontal drag: solved in PageEndDrag
# v add module: images, for embedded images
# v refactor images to PyEmbeddedImage
# v remove use of 'icoPath', 'appIcon', 'os.path.join': now PyEmbeddedImage
# v add BoxSizer to CodeContext for auto sizing its StaticText control
# v shorten CONSTANTS (see config) in all modules: mnemonic naming convention
# v reformat '#TODO/FIX/NOTE/DONE' task tags to start of line
# v FileSave, FileSaveAs: add functionality, also testing
# v add 'pathdata' list to Editor class (doc object)
# v add method _split_path
# v module name change: FIX_PreferencesDialog -> preferences
# v rename menu: Window -> Layout
# v add method LayoutFileTabs to Layout menu
# v style BORDER_SUNKEN for Notebook, FunctionList and CodeContext
# v set (in)active colours for Notebook tabs
# v add method _update_page_tabs, insert new tab and update page/tooltip/app titles
# v new DEBUG['STACK']: indented call levels in '_dbg_whoami'
# v hide toolbar/statusbar leaves empty space: SOLVED by 'SendSizeEvent'
# v refactor 'mb.Check' code block to ternary operator: 'x if True else y' (where viable)
# v refactor '_getPagDoc' and calling code: return when no document open, 'if not doc: return'
# v add 2 methods to Layout menu: LayoutRuler, LayoutRulerSwap
# v add class MidSplitter to support ruler Layout
# v add 3 methods to File menu: FileInsertFile, FileAppendFile, FileWriteBlockToFile
# v file menu ACTIONS, open/save/.../doc.LoadFile(fnm), doc.SaveFile(fnm)
# v move 3 menu items from Edit and View to Layout menu: Tooltips, Menu Icons, Preferences
# v add DropFiles to MainWindow, supports drag and drop
# v add method _open_files: dedupe DropFiles, FileOpen
# v add method _set_language_styling: dedupe FileNew, LanguageSetStyling, _open_files, Editor
# v add method to Layout menu: FileTabIcons toggles display of file tab icons
# v now 1 file extension icon available for file tab: 'file_ext_'
# v moved ContextMenu: Editor -> MainWindow
# v integrate PageMenu from Notebook into ContextMenu and refactor code
# v add method TextChanged to Editor: update mod indicator '*' immediately
# v add method SplitEditor to notebook ctx menu: 2nd view of edited file, 1st basic setup
# v ContextMenu: syntax highlighting menu on right click in statusbar SBF['LNG'][0] field
# v from main to module: gui -> menu, toolbar and statusbar global methods
# v  "    "   "    "   : editor -> class Editor
# v  "    "   "    "   : find -> class FindReplaceDialog
# v  "    "   "    "   : notebook -> class Notebook
# v  "    "   "    "   : splitter -> classes Ver/Hor/MidSplitter
# v  "    "   "    "   : codecontext -> class CodeContext
# v  "    "   "    "   : sidepanel -> classes SidePanel, FunctionList, TreeCtrl
# v add method _get_file_icon: return file tab icon for extension
# v add check marks to toolbar context menu
# v add 5 config processing functions: CfgDefault, CfgCreate, CfgRead, CfgWrite, CfgApply
# v add 2 UI handlers for doc modified and find string: UpdateUIMod, UpdateUIFnd
# v add method _not_implemented: print unimplemented functionality
# v add document and bookmark panels to side panel and View menu
# v add exit_called: discard FileClose actions when called from FileExit
# v add method EditHighlightMatches to editor context menu: calls HighlightMatches
# v ContextMenu: editor margin menu on right click in margin
# v add method _top_line_tooltip to replace _hover_text (used when scrolling)
# v add 4 data type checking functions: is_bool, is_int, is_float, is_list
# v remove CFG_FIL_USE constant: ALWAYS use config file or create default
# v DEBUG: _dbg_BOOKMARK, show bookmarks per file
# v renamed modules to lowercase: codecontext, oeuf, gui, sidepanel
# v removed module oeuf_egami, moved contents to oeuf module
# v submenu item itself DOES NOT SHOW ICON, e.g. see View->Highlighting submenu
# v add module: constant, for global variables; moved globals from config module
#########################

#TODO, use magic names and metadata
#INFO, URL=https://stackoverflow.com/questions/1523427/what-is-the-common-header-format-of-python-files/1523456
__all__ = ['package', 'module', 'class', 'method', 'function', 'variable', '...']
__credits__ = ['Neil Hodgson', 'Robin Dunn', 'Andrea Gavana', 'Mike Driscoll', 'Cody Precord', ]
__version__ = '0.90'
__author__ = 'TSN'
__license__ = 'GPL'
__status__ = 'Development'

#INFO, grep -oh '__[A-Za-z_][A-Za-z_0-9]*__' d:\Dev\Python27\Lib\*.py | sort | uniq
#INFO, - list all Python magic names, documented or not, from Lib directory
#INFO, URL=https://stackoverflow.com/questions/8920341/finding-a-list-of-all-double-underscore-variables


# timing
from lib.util import now_
# from lib.util import Timer, now_
startup_time = session_time = now_()
# tmr = Timer()
# tmr.start()

#NOTE, workaround: enables main module startup outside its own directory
import os
import sys
# print(os.getcwd())
os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
# print(os.getcwd())

from lib.constant import (
    appFull, LOC, TIM_FMT,
    # SsnCreate, SsnRead, SsnWrite,  # SsnApply,
    FAST_EXIT,
    TASKBAR_ICO, HELP_CONTEXT,
    APP_REDIRECT, APP_REDIRECT_FNM, APP_INSPECTION, APP_INSP,
    DELAY,
    # FNL_IMG_ICO_USE, FNL_FIL_USE, FNL_FIL_NAME, FNL_TREE_EXPAND,
    # ICO_GO_FORWARD, ICO_GO_DOWN, ICO_NORMAL_FILE, ICO_GREEN, ICO_YELLOW,
    # ICO_RED, INFINITY,
    appName, appIcon, fno, FNM_CHARS, URL_CHARS,
    SASH, CRLF, CR, LF,
    # NO_ACT, NO_TXT, NO_ICO, NO_TYP, NO_UIH,
    MB, TB, TBX, SBF, SBF_CPY, SBX, DMX,
    SPT, TXT_NIL,
    FOL_STY_NIL, FOL_STY_SQR, FOL_STYLE,
    MGN, MRK,
)
from lib.debug import (
    DEBUG, _dbg_CONFIG,
    DbgCreate, DbgRead,
    _dbg_STARTUP, _dbg_EVENT, _dbg_FILE_HISTORY, _dbg_POSITION_HISTORY, _dbg_CTXTTB,
    _dbg_MODEVTMASK, _dbg_RMTWS, _dbg_FOCUS, _dbg_TRACEFUNC,
    _dbg_BOOKMARK, _dbg_CLRDB, _dbg_SCINTILLA_CMDS, _dbg_whoami, _dbg_funcname
)
from lib.config import (
    CfgCreate, CfgRead, CfgWrite, CfgApply, noit, cnuf,
)
cnuf()
from lib.editor import Editor
from lib.find import FindReplaceDialog
from lib.gui import (
    SetupMenu, BuildMainMenu, RebuildMainMenu, AttachRecentFilesMenu,
    SetupToolBar, BuildToolBar, SetupStatusBar,
    SystemTrayMenu
)
from lib.images import catalog as PNG  # embedded images
from lib.language import (
    LANG, file_exts, SyntaxStyling,
    LngCreate, LngRead,  # LngWrite, LngApply,
)
from lib.notebook import Notebook
from lib.oeuf import Oeuf
from lib.preferences import Preferences
from lib.searchpanel import SearchPanel
from lib.sidepanel import SidePanel
from lib.splitter import (
    WinSplitter  #, VerSplitter, HorSplitter, MidSplitter, EdtSplitter
)
from lib.util import (
    Freeze, Thaw
)

from lib.external.codecontext import CodeContext
from lib.external.ruler import RulerCtrl as Ruler

# import macro
# import menu

#INFO, URL=http://pythonhosted.org/Autologging/examples.html
# from autologging import traced, TRACE
#TODO, Use logging Module integrated with current DEBUG
# import logging, sys
# logging.basicConfig(level=TRACE, stream=sys.stdout,
#     format='%(levelname)s:%(name)s:%(funcName)s:%(message)s')
# import lib.__future__.memory_footprint_object as mem

from beeprint import pp
from datetime import datetime as dtm
#NOTE, introspection, pretty printing
# from inspect import getmembers
from pprint import pprint
from shutil import copyfile
from subprocess import check_output

from wx.lib.agw import advancedsplash as splash
from wx.lib.agw import shortcuteditor as SCE
#FIX, pyclbr includes class 'art' from import below in classbrowser
# from wx.lib.agw.artmanager import ArtManager as art
# import wx.adv as adv
#DONE, wx.lib.mixins.inspection crashed Python, now works 2017-08-25 18:18:27
import wx.lib.mixins.inspection as inspection
# import wx.lib.multisash as sash

import ctypes
import webbrowser
import wx
import wx.stc as stc


#FIX, enable/disable paste on menu, toolbar, context menu
#NOTE, DataObject not used yet
# class DataObject(wx.DataObject):
#     """class DataObject"""
#     def __init__(self, value=''):
#         wx.DataObject.__init__(self)
#         self.formats = [wx.DataFormat(wx.DF_TEXT)]
#         self.data = value

#     def GetAllFormats(self, d):
#         return self.formats

#     def GetFormatCount(self, d):
#         return len(self.formats)

#     def GetPreferredFormat(self, d):
#         return self.formats[0]

#     def GetDataSize(self, format):
#         # On windows strlen is used internally for stock string types
#         # to calculate the size, so we need to make room for and add
#         # a null character at the end for our custom format using
#         # wx.DF_TEXT.
#         return len(self.data)+1


#INFO, URL=http://pythonhosted.org/Autologging/examples.html
# @traced
class MainWindow(wx.Frame):
    """class MainWindow"""
    def __init__(self, *args, **kwargs):
        if DEBUG['STACK']: print(_dbg_whoami())
        super(MainWindow, self).__init__(*args, **kwargs)
#INFO, => prints 'wxFrame'
#         print('MainWindow.ClassName:', self.ClassName)

        self.exit_called = False     # discard FileClose actions when called from FileExit
        self.multi_clipboard = None  # multiple selection clipboard

#         self.findtxt = str(cfg['Search']['FindText'])         # find string
#         self.repltxt = str(cfg['Search']['ReplaceText'])      # replace string
# #TODO, implement incremental search, see ConTEXT
#         self.incrtxt = str(cfg['Search']['IncrementalText'])  # incremental string
#         self.findflg = int(cfg['Search']['FindFlags'])        # find flags, default: search forward
        self.findreg = cfg['Search']['FindRegex']           # find: regular expression
        self.findwrp = cfg['Search']['FindWrap']            # find: wrap to top/bottom
        self.dlg_fnd = None                                 # find dialog object

        # TOOLBAR
        toolbar = SetupToolBar(self)
        self.tb = BuildToolBar(self, toolbar)

#FIX, RULER testing
#         self.rlr = Ruler(self)
#         self.SendSizeEvent()

        # STATUSBAR
        self.sb = SetupStatusBar(self)
        self.SetStatusBar(self.sb)
        self._push_statustext('Welcome to ' + appFull)

        # SPLITTERS
        # horizontal (versp/SearchPanel)
        self.schsp = WinSplitter('SCH', self)
        # vertical (horsp/SidePanel)
        self.versp = WinSplitter('VER', self.schsp)
        # horizontal (CodeContext/midsp)
        self.horsp = WinSplitter('HOR', self.versp)
        # mid horizontal (Ruler/Notebook)
        self.midsp = WinSplitter('MID', self.horsp)

        # CODE CONTEXT, RULER and NOTEBOOK
#FIX, decide on CodeContext parms, now just 2: parent, doc
#FIX, parm2 (doc) = None, for now...??

        self.schtopPanel = self.versp
        self.schbotPanel = self.sch = SearchPanel(self.schsp)

        self.topPanel = self.ccx = CodeContext(self.horsp)
        self.midtopPanel = self.rlr = Ruler(self.midsp, offset=0)
#         self.midtopPanel = self.rlr = Ruler(self.midsp)
        self.midbotPanel = self.nb = Notebook(self.midsp)
        self.bottomPanel = self.midsp
        self.leftPanel = self.horsp
#         # vertical (editor/2nd view)
#         self.edtsp = EdtSplitter(self.nb)
#         dummy1 = wx.Panel(self.edtsp)
#         dummy2 = wx.Panel(self.edtsp)

        # SIDE PANEL
#FIX, parm2 (doc) = None, for now...??
        self.rightPanel = self.spn = SidePanel(self.versp)

#FIX, 'CodeContext' in top left as tiny widget
#NOTE, workaround: split/unsplit immediately...
        self.schsp.SplitHorizontally(self.schtopPanel, self.schbotPanel, SASH['SCH'][self.sch.mode])
        self.versp.SplitVertically(self.leftPanel, self.rightPanel, -SASH['VER'])
        self.horsp.SplitHorizontally(self.topPanel, self.bottomPanel, SASH['HOR'])
        self.midsp.SplitHorizontally(self.midtopPanel, self.midbotPanel, SASH['MID'])
#         self.edtsp.SplitVertically(dummy1, dummy2, SASH['EDT'])
        self.schsp.Unsplit(self.schbotPanel)
        self.versp.Unsplit(self.rightPanel)
        self.horsp.Unsplit(self.topPanel)
        self.midsp.Unsplit(self.midtopPanel)
#         self.edtsp.Unsplit(dummy2)
#         del dummy1, dummy2

        # MENUBAR, main, context, recent file history and system tray menus
        MNU, CTX = SetupMenu(self)
        self.menu, self.ctx, self.icons, self.hlp = MNU, CTX, cfg['Layout']['MenuIcons'], cfg['Layout']['MenuHelpText']
        self.mb = BuildMainMenu(self, self.menu, icons=self.icons, hlp=self.hlp)
        AttachRecentFilesMenu(self, recent_list)
        if cfg['General']['SystemTrayMenu']:
            self.stm = SystemTrayMenu(self)

        # self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.Bind(wx.EVT_SIZE, self.Refresh)
        self.Bind(wx.EVT_CLOSE, self.FileExit)
        self.Bind(wx.EVT_DROP_FILES, self.DropFiles)
        self.Bind(wx.EVT_MAXIMIZE, self.Maximize)

###############################################################################
###############################################################################
#         self.Bind(wx.EVT_PAINT, self.Paint)
#
#     def Paint(self, evt):
#         dc = wx.PaintDC(self.leftPanel)
#         dc.SetBackground(wx.Brush("WHITE"))
#         dc.Clear()
#
#         dc.SetFont(wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True))
#         dc.DrawText("Bitmap alpha blending (on all ports but gtk+ 1.2)", 25, 25)
#
#         bmp = wx.Bitmap(PNG['toucan.png'])
#
#         dc.DrawBitmap(bmp, 25, 100, True)
#
# #         dc.SetFont(self.Font)
# #         y = 75
# #         for line in range(10):
# #             y += dc.CharHeight + 5
# #             dc.DrawText(msg, 200, y)
#         dc.DrawBitmap(bmp, 250, 100, True)
###############################################################################
###############################################################################

#FIX, decorator for _getPagDoc
    def _getdoc(arg):
        def decorator(fnc):
            def wrapper(self, *args, **kwargs):
                print('decorator [_getdoc] for [%s]' % fnc.__name__)
                _dbg_funcname(arg)
                __, doc = self._getPagDoc()
                if not doc: return
                fnc(self, doc, *args, **kwargs)
            return wrapper
        return decorator

    # @_getdoc
    # def OnIdle(self, doc, evt):
    def OnIdle(self, evt):
        __, doc = self._getPagDoc()
        if not doc: return
        if DEBUG['IDLE']: print('OnIdle:', end='')
        if DEBUG['IDLE'] > 1: _dbg_EVENT(evt)
        if DEBUG['IDLE']: print('[%s] - [%s]' % (doc.filename, doc.dirname))

    @staticmethod
    def Refresh(evt):
        if DEBUG['BASIC'] > 1: print('Refresh: ', end='')
        if DEBUG['BASIC'] > 1: _dbg_EVENT(evt)
#         if DEBUG['BASIC'] < 2: print()
#                     print('Frame Min  = %s' % self.MinSize)
#                     print('Frame Max  = %s' % self.MaxSize)
#                     print('Frame Best = %s' % self.BestSize)
#                     print('ToolB Min  = %s' % self.tb.MinSize)
#                     print('ToolB Max  = %s' % self.tb.MaxSize)
#                     print('ToolB Best = %s' % self.tb.BestSize)
#                     print('%s' % '-'*10)
        # resize splitter client area
#         self.versp.SetClientSize(self.ClientSize)
#         self.horsp.SetClientSize(self.ClientSize)
        # resize notebook client area
#         self.nb.SetClientSize(self.ClientSize)
#         self.bottomPanel.SetClientSize(self.ClientSize)
        if evt:
            evt.Skip()

    def UpdateUIDoc(self, evt):
        if DEBUG['UPDUI']: print('UpdateUIDoc: ', end='')
        if DEBUG['UPDUI'] > 1: _dbg_EVENT(evt)

#TODO, hide full menus when NO document open
        # for m in range(12):
        #     self.mb.EnableTop(m, False if m not in [0, 5, 9, 10, 11] and not self.nb.PageCount else True)

        if self.nb.PageCount:  # when document open
            __, doc = self._getPagDoc()
            if not doc: return

#NOTE, using '[Margin][LeftWidth] = 4' in 'SPyE.cfg' to left align ruler
            # update ruler alignment when visible
            if self.midsp.IsSplit():
                doc.new_XOffset = doc.XOffset
                if doc.old_XOffset != doc.new_XOffset:
                    delta = doc.old_XOffset - doc.new_XOffset
                    self.rlr.set_offset(self.rlr.offset + delta)
                    doc.old_XOffset = doc.new_XOffset

            evt.Enable(True)

            # caret position history
            self.mb.Enable(MB['JMP_BCK'], True if cfg['CaretPositionHistory']['Enable'] else False)
            self.mb.Enable(MB['JMP_FWD'], True if cfg['CaretPositionHistory']['Enable'] else False)

            # enable swap when split window visible
            self.mb.Enable(MB['LAY_SCS'], True if self.schsp.IsSplit() else False)
            self.mb.Enable(MB['LAY_RLS'], True if self.midsp.IsSplit() else False)
            self.mb.Enable(MB['LAY_SPS'], True if self.versp.IsSplit() else False)
            self.mb.Enable(MB['LAY_CCS'], True if self.horsp.IsSplit() else False)

#DONE, disable 'FileTabIcons' when 'FileTabs' not checked
            self.mb.Enable(MB['LAY_FTI'], True if self.mb.IsChecked(MB['LAY_FTB']) else False)

            # check open documents for change on disk for reload
#             if not app.focus:
#                 return
#             else:
#                self._detect_file_change()

#FIX, message never shows, see 'EditUndo/EditRedo'
            self.mb.Enable(MB['EDT_UDO'], True if doc.CanUndo() else False)
            self.mb.Enable(MB['EDT_RDO'], True if doc.CanRedo() else False)
#DONE, enable/disable undo/redo buttons on toolbar, too
            self.tb.EnableTool(TB['UDO'], True if doc.CanUndo() else False)
            self.tb.EnableTool(TB['RDO'], True if doc.CanRedo() else False)
#########################################################################
#########################################################################
#FIX, enable/disable paste on menu, toolbar, context menu
            self.mb.Enable(MB['EDT_CUT'], True if doc.CanCut() else False)
            self.mb.Enable(MB['EDT_CPY'], True if doc.CanCopy() else False)
            self.mb.Enable(MB['EDT_PST'], True if doc.CanPaste() else False)
#NOTE, it seems Windows and Scintilla have a SEPARATE clipboard!
#INFO, use 'ECHO OFF|CLIP' in CMD to clear Windows clipboard
#INFO, URL=https://github.com/wxWidgets/Phoenix/blob/master/unittests/test_dataobj.py
#             clp = wx.Clipboard()
#             clp.Open()
#             clp.Clear()
#             data = DataObject()
# #             data = wx.DataObjectSimple(format=wx.DF_TEXT)
#             clp.GetData(data)
#             print(data.GetDataSize(wx.DF_TEXT))
#             self.mb.Enable(MB['EDT_PST'], True if data.GetDataSize(wx.DF_TEXT) > 2 else False)
#########################################################################
#########################################################################
        else:
            evt.Enable(False)

    def UpdateUIFnd(self, evt):
        if DEBUG['UPDUI']: print('UpdateUIFnd: ', end='')
        if DEBUG['UPDUI'] > 1: _dbg_EVENT(evt)
        if self.nb.PageCount:  # when document open, empty find string?
            evt.Enable(True if self.findtxt else False)
        else:
            evt.Enable(False)

    def UpdateUIHst(self, evt):
        if DEBUG['UPDUI']: print('UpdateUIHst: ', end='')
        if DEBUG['UPDUI'] > 1: _dbg_EVENT(evt)
        # recent file history items?
        self.mb.Enable(MB['HST_RCF'], True if self.hist.Count else False)
        self.mb.Enable(MB['HST_RCA'], True if self.hist.Count else False)
        self.mb.Enable(MB['HST_CLI'], True if self.hist.Count else False)

    def UpdateUIMac(self, evt):
        if DEBUG['UPDUI']: print('UpdateUIMac: ', end='')
        if DEBUG['UPDUI'] > 1: _dbg_EVENT(evt)
        if self.nb.PageCount:  # when document open, macro recording?
            __, doc = self._getPagDoc()
            if not doc: return
            if doc.recording:
                evt.Enable(True if evt.Id in [MB['MAC_STP'], MB['MAC_TST']] else False)
            else:
                evt.Enable(False if evt.Id == MB['MAC_STP'] else True)
                if not len(doc._macro) and evt.Id in [MB['MAC_PLY'], MB['MAC_PLM']]:
                    evt.Enable(False)
        else:
            evt.Enable(False)

    def UpdateUIMod(self, evt):
        if DEBUG['UPDUI']: print('UpdateUIMod: ', end='')
        if DEBUG['UPDUI'] > 1: _dbg_EVENT(evt)
        if self.nb.PageCount:  # when document open, modified?
            __, doc = self._getPagDoc()
            if not doc: return
            evt.Enable(True if doc.IsModified() else False)
        else:
            evt.Enable(False)

    def UpdateUISel(self, evt):
        if DEBUG['UPDUI']: print('UpdateUISel: ', end='')
        if DEBUG['UPDUI'] > 1: _dbg_EVENT(evt)
        if self.nb.PageCount:  # when document open, text selected?
            __, doc = self._getPagDoc()
            if not doc: return
            cnt, sel = doc.Selections, doc.GetSelection()
            if cnt > 1 or sel[0] != sel[1]:
                evt.Enable(True)
            else:
                evt.Enable(False)
        else:
            evt.Enable(False)

    def DropFiles(self, evt):
        _dbg_funcname()
        if DEBUG['BASIC']: print(' ', evt.Files)
        if DEBUG['BASIC']: print(' ', evt.NumberOfFiles)

        filelist = [[fnm, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] for fnm in evt.Files]
        self._open_files(filelist)

#FIX, direct call from 'Bind(wx.EVT_MAXIMIZE, ...') does NOT force default sash position
    def Maximize(self, evt):
        _dbg_funcname()
        # print('Maximize')
#TODO, needs better coding...
        if self.versp.IsSplit():
            self.LayoutSidePanel(evt)
            self.LayoutSidePanel(evt)

    def FileNew(self, evt):
        _dbg_funcname()
        global fno

        if DEBUG['STACK']: print(_dbg_whoami())
        if DEBUG['FILE'] > 1: print('   IN: cwd [%s]' % os.getcwd())
        fno += 1
        dnm = ''
        pfx = cfg['General']['NewFilePrefix']
        fnm = pfx + str(fno)
        fbs = ''
        ext = ''
        if DEBUG['FILE']: print('    [%s]' % (fnm))
        self.Freeze()  # avoid flicker
#FIX, SPLIT_EDITOR
#         # vertical (editor/2nd view)
#         self.edtsp = EdtSplitter(self.nb)
#         doc = Editor(self.edtsp, [dnm, fnm, fbs, ext])

        doc = Editor(self.nb, [dnm, fnm, fbs, ext])

        # get language based on menu selection
        lang = [m for m in LANG if self.mb.IsChecked(m[4])]
        doc._set_language_styling(lang)
        self._update_page_tabs(doc, newtab=True)
#         multi = sash.MultiSash(self.nb.CurrentPage, -1, pos=(0,0), size=doc.ClientSize)
#         multi.SetDefaultChildClass(Editor)


        # dcp = doc.spt[SPT['DCM']]
        # if dcp:
        #     dcm = dcp.ctrl
        #     if dcm.IsFrozen():
        #         dcm.Thaw()
        #         self.Freeze()
        #         # dcm.Freeze()
        # self.Thaw()


#FIX, error 'wx._core.wxAssertionError: C++ assertion "m_freezeCount" failed at ..\..\src\common\wincmn.cpp(1257) in wxWindowBase::Thaw(): Thaw() without matching Freeze()'
#INFO, occurs when selecting 'FileNew' while 'DocumentMap' visible
        self.Thaw()

        if DEBUG['SCMOD']: _dbg_MODEVTMASK(doc)
        if DEBUG['FILE'] > 1: print('  OUT: cwd [%s]' % os.getcwd())

    def FileOpen(self, evt):
        _dbg_funcname()
        if DEBUG['FILE'] > 1: print('   IN: cwd [%s]' % os.getcwd())
        sty = wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_PREVIEW | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE
        dlg = wx.FileDialog(self, 'Open', os.getcwd(), '', file_exts, sty)
        if dlg.ShowModal() != wx.ID_OK:
            if DEBUG['FILE']: print('    Cancel')
        else:
            filelist = [[fnm, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] for fnm in dlg.Paths]
            # timing
            if DEBUG['TIMER']: open_time = now_()
            self._open_files(filelist)
            # timing
            if DEBUG['TIMER']:
                open_time = now_() - open_time
                print('   open_time: %6d ms' % (open_time))

        if DEBUG['FILE'] > 1: print('  OUT: cwd [%s]' % os.getcwd())
        dlg.Destroy()

    def FileReopenClosedFromHistory(self, evt):  #, all_files=False
        _dbg_funcname()
        _id = evt.Id
        cnt = self.hist.Count

        if _id == MB['HST_RCA'] and cfg['RecentFilesHistory']['ReopenConfirm']:
            msg = 'Reopen ' + str(cnt) + ' file(s) from recent files history?'
            ans = self._msg_box(self, 'WARN_ASK', msg)
            if ans != wx.ID_YES:
                return

        # walk file history
        for fileNum in range(cnt):
            fnm = self.hist.GetHistoryFile(fileNum)
            # file already open?
            opened = False
            for j in range(self.nb.PageCount):
                pag = self.nb.GetPage(j)
                # print('{}\n  {}\n---'.format(fnm, pag.pathname))
                if fnm == pag.pathname:
                    opened = True
                    # print('  opened = True')
                    break
            # print('\n \n')
            if not opened:
                filelist = [[fnm, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
                self._open_files(filelist)
                fbs = os.path.basename(fnm)
                self._push_statustext('Reopening closed file [%s] from recent file history' % fbs)
            # quit if 1 file selected
            if _id == MB['HST_RCF']:
                break

    def FileOpenFromHistory(self, evt):
        _dbg_funcname()
        fileNum = evt.Id - wx.ID_FILE1
        fnm = self.hist.GetHistoryFile(fileNum)
        self.hist.AddFileToHistory(fnm)  # move up the list
        filelist = [[fnm, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self._open_files(filelist)
        fbs = os.path.basename(fnm)
        self._push_statustext('Opening file [%s] from recent file history' % fbs)

    def FileClearHistory(self, evt):
        _dbg_funcname()
        cnt = self.hist.Count
        for i in range(cnt):
            self.hist.RemoveFileFromHistory(0)
        self._push_statustext('Cleared %d recent file history items' % cnt)

#INFO, URL=https://gist.github.com/jbjornson/1186126
    def FileOpenAtCursor(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        if DEBUG['FILE']: print('  ------')

        fnm = ''
        vld = False
        sel = doc.SelectedText
        if DEBUG['FILE']: print('  Select' if sel else '  Parse')

        if sel:
            if CRLF in sel:
                if DEBUG['FILE']: print('  SKIP : multiple lines selected')
                return
            else:
                if DEBUG['FILE']: print('  sel  : [%s]' % sel)
                fnm = sel
        else:
            # get potential filename from line
            lin, pos = doc.CurLine
            lin = lin.rstrip()  # remove newline
            left = lin[0:pos]
            right = lin[pos:]
            if DEBUG['FILE']: print('  line : [%s]\n  pos  : [%s]' % (lin, pos))
            if DEBUG['FILE']: print('  left : [%s]\n  right: [%s]' % (left, right))

            # walk left until invalid
            txt = ''
            for c in reversed(left):
                if c in FNM_CHARS:
                    txt = c + txt
                else:
                    break
            left = txt

            # walk right until invalid
            txt = ''
            for c in right:
                if c in FNM_CHARS:
                    txt += c
                else:
                    break
            right = txt

            # get filename
            fnm = left + right

        fbs = os.path.basename(fnm)
        vld = os.path.isfile(fnm)

        if DEBUG['FILE']: print('  fnm  : [%s]' % fnm)
        if DEBUG['FILE']: print('  fbs  : [%s]' % fbs)
        if DEBUG['FILE']: print('  valid: [%s]' % vld)

        if vld:
            self._push_statustext('Opening file [%s] at cursor' % fbs)
            filelist = [[fnm, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
            self._open_files(filelist)
        else:
#####################
# temporary code
#####################
#FIX, create function to show error msg in statusbar
            bg = self.sb.BackgroundColour
            self.sb.SetBackgroundColour(cfg['Statusbar']['ErrorBackColour'])
            self._push_statustext('Invalid filename at cursor')
            self.sb.SetBackgroundColour(bg)
            # self._set_statustext('Invalid filename at cursor')
#####################
# temporary code
#####################

#TODO, open URL at cursor, possibly integrate with 'FileOpenAtCursor' later
#INFO, URL=https://stackoverflow.com/questions/1547899/which-characters-make-a-url-invalid/1547940#1547940
    def URLOpenAtCursor(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        if DEBUG['URL']: print('  ------')

        url = ''
        # vld = False
        sel = doc.SelectedText
        if DEBUG['URL']: print('  Select' if sel else '  Parse')

        if sel:
            if CRLF in sel:
                if DEBUG['URL']: print('  SKIP : multiple lines selected')
                return
            else:
                if DEBUG['URL']: print('  sel  : [%s]' % sel)
                url = sel
        else:
            # get potential URL from current line
            lin, pos = doc.CurLine
            lin = lin.rstrip()  # remove newline
            # parse line for valid URI scheme
            schemes = ('http://', 'https://', 'ftp://', 'ftps://', 'file:///', 'file://', 'mailto:')

            # if any(s in lin for s in schemes):
            #     print('*** valid URI scheme ***')
            # else:
            #     print('!!! INVALID URI scheme !!!')
            #     return

            idx = -1
            for s in schemes:
                if s in lin:
                    idx = lin.find(s)
                    sch = s
                    break

            if DEBUG['URL']: print('  URI scheme: [%s]' % (s if idx != -1 else 'NOT found'))

            # scheme not found OR caret before URI scheme?
            if idx == -1 or pos < idx:
                return

            left = lin[0:pos]
            right = lin[pos:]
            if DEBUG['URL']: print('  line : [%s]' % (lin))
            if DEBUG['URL']: print('  pos  : [%d]\n  idx  : [%d]' % (pos, idx))
            if DEBUG['URL']: print('  left : [%s]\n  right: [%s]' % (left, right))

            # walk left until invalid OR at 1st pos of URI scheme
            txt = ''
            for c in reversed(left):
                if DEBUG['URL'] > 1: print('    txt: [%s]' % (txt))
                # at 1st pos of URI scheme?
                if len(txt) == pos - idx:
                    if DEBUG['URL']: print('  SKIP : at 1st pos of URI scheme [%s]' % (sch))
                    break
                if c in URL_CHARS:
                    txt = c + txt
                else:
                    break
            left = txt

            # walk right until invalid
            txt = ''
            for c in right:
                if c in URL_CHARS:
                    txt += c
                else:
                    break
            right = txt

            # get URL
            url = left + right

            if DEBUG['URL']: print('  URL  : [%s]' % (url))

        # fbs = os.path.basename(fnm)
        # vld = os.path.isfile(fnm)

        # if DEBUG['URL']: print('  fnm  : [%s]' % fnm)
        # if DEBUG['URL']: print('  fbs  : [%s]' % fbs)
        # if DEBUG['URL']: print('  valid: [%s]' % vld)

#####################
# temporary code
#####################
        vld = True
#####################
# temporary code
#####################
        if vld:
            self._push_statustext('Opening URL [%s] at cursor' % url)
            webbrowser.open(url)
            # filelist = [[fnm, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
            # self._open_files(filelist)
        else:
#####################
# temporary code
#####################
#FIX, create function to show error msg in statusbar
            bg = self.sb.BackgroundColour
            self.sb.SetBackgroundColour(cfg['Statusbar']['ErrorBackColour'])
            self._push_statustext('Invalid URL at cursor')
            self.sb.SetBackgroundColour(bg)
            # self._set_statustext('Invalid URL at cursor')
#####################
# temporary code
#####################

    def FileSave(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        if DEBUG['FILE'] > 1: print('   IN: cwd [%s]' % os.getcwd())
        res = True
        if doc.IsModified():
            if doc.dirname:
#########################################################################
#########################################################################
                self._not_implemented(None, 'SAVE EXISTING FILE ')
                self.Freeze()  # avoid flicker
#                 res = doc.SaveFile(doc.pathname)
                self.Thaw()
#########################################################################
#########################################################################
            else:
                msg = 'New file ' + doc.filename + ' has been modified, save changes?'
                ans = self._msg_box(self, 'WARN_ASK', msg)
                if ans == wx.ID_YES:
                    res = self.FileSaveAs(evt)
                    _dbg_FOCUS(doc)
                    if DEBUG['FILE']: print('       Yes:[%s]' % doc.pathname)
                elif ans == wx.ID_NO:
                    if DEBUG['FILE']: print('        No:[%s]' % doc.pathname)
                elif ans == wx.ID_CANCEL:
                    if DEBUG['FILE']: print('    Cancel:[%s]' % doc.pathname)
                    res = False
        else:
            if DEBUG['FILE']: print('    NO mod:[%s]' % doc.pathname)

        if DEBUG['FILE'] > 1: print('  OUT: cwd [%s]' % os.getcwd())
        return res

    def FileSaveAs(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        if DEBUG['FILE'] > 1: print('   IN: cwd [%s]' % os.getcwd())
#NOTE, FileSaveAs starts 'Save As' dialog
        sty = wx.FD_SAVE | wx.FD_CHANGE_DIR | wx.FD_PREVIEW | wx.FD_OVERWRITE_PROMPT
        dlg = wx.FileDialog(self, 'Save As', os.getcwd(), doc.pathname, file_exts, sty)
        idx = LANG.index([m for m in LANG if self.mb.IsChecked(m[4])][0])
        print(idx)
        dlg.SetFilterIndex(idx + 1)  # add 1: 'All files' = 0 in 'file_exts'
        res = True
        if dlg.ShowModal() != wx.ID_OK:
            if DEBUG['FILE']: print('    Cancel:[%s]' % doc.pathname)
            res = False
        else:
            if DEBUG['FILE']: print('        OK:[%s]' % doc.pathname)
#FIX, test whether to use '.Path(s) AND if '.strip()' is needed
            pnm = dlg.Path
#             pathname = dlg.Path.strip()
            self.Freeze()  # avoid flicker
            res = doc.SaveFile(pnm)
            dnm, fnm, fbs, ext = self._split_path(pnm)
            doc.dirname, doc.filename, doc.filebase, doc.file_ext = dnm, fnm, fbs, ext
            doc.pathname = pnm
            self._update_page_tabs(doc)
            self.Thaw()

        if DEBUG['FILE'] > 1: print('  OUT: cwd [%s]' % os.getcwd())
#         dlg.Destroy()
        return res

    def FileSaveAll(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        if DEBUG['FILE'] > 1: print('   IN: cwd [%s]' % os.getcwd())
        self.Freeze()  # avoid flicker
        cur = self.nb.Selection     # save current page
        for i in range(self.nb.PageCount):
#FIX, only save when doc is modified (solved?)
#             __, doc = self._getPagDoc()
#             if not doc: return
#             if doc.IsModified():   # modified?
            self.nb.SetSelection(i)
            res = self.FileSave(evt)
        self.nb.SetSelection(cur)  # restore current page
        self.Thaw()

        if DEBUG['FILE'] > 1: print('  OUT: cwd [%s]' % os.getcwd())

    def FileInsertFile(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        if DEBUG['FILE'] > 1: print('   IN: cwd [%s]' % os.getcwd())
        sty = wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_PREVIEW | wx.FD_FILE_MUST_EXIST
        dlg = wx.FileDialog(self, 'Insert File', os.getcwd(), '', file_exts, sty)
        if dlg.ShowModal() != wx.ID_OK:
            if DEBUG['FILE']: print('    Cancel:[%s]' % doc.pathname)
        else:
            pnm = dlg.Path
            if DEBUG['FILE']: print('        OK:[%s]' % pnm)
            fil = open(pnm, 'r')
            txt = fil.read().replace(LF, CRLF)
            fil.close()
            doc.WriteText(txt)
            self._set_statustext('File [%s] inserted' % pnm)

        if DEBUG['FILE'] > 1: print('  OUT: cwd [%s]' % os.getcwd())

    def FileAppendFile(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        if DEBUG['FILE'] > 1: print('   IN: cwd [%s]' % os.getcwd())
        sty = wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_PREVIEW | wx.FD_FILE_MUST_EXIST
        dlg = wx.FileDialog(self, 'Append File', os.getcwd(), '', file_exts, sty)
        if dlg.ShowModal() != wx.ID_OK:
            if DEBUG['FILE']: print('    Cancel:[%s]' % doc.pathname)
        else:
            pnm = dlg.Path
            if DEBUG['FILE']: print('        OK:[%s]' % pnm)
            fil = open(pnm, 'r')
            txt = fil.read().replace(LF, CRLF)
            fil.close()
            doc.DocumentEnd()
            doc.NewLine()
            doc.WriteText(txt)
            self._set_statustext('File [%s] appended' % pnm)

        if DEBUG['FILE'] > 1: print('  OUT: cwd [%s]' % os.getcwd())

    def FileWriteBlockToFile(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        if DEBUG['FILE'] > 1: print('   IN: cwd [%s]' % os.getcwd())
        txt = doc.SelectedText

        sty = wx.FD_SAVE | wx.FD_CHANGE_DIR | wx.FD_PREVIEW | wx.FD_OVERWRITE_PROMPT
        dlg = wx.FileDialog(self, 'Write Block To File', os.getcwd(), '', file_exts, sty)
        dlg.SetFilterIndex(19)  # default: plain text
        if dlg.ShowModal() != wx.ID_OK:
            if DEBUG['FILE']: print('    Cancel:[%s]' % doc.pathname)
        else:
            pnm = dlg.Path
            if DEBUG['FILE']: print('        OK:[%s]' % pnm)
            fil = open(pnm, 'w')
            fil.write(txt.replace(CR, ''))
            fil.close()
            self._set_statustext('Block written to file [%s] ' % pnm)

        if DEBUG['FILE'] > 1: print('  OUT: cwd [%s]' % os.getcwd())

    def FileClose(self, evt):
        _dbg_funcname()
        cur, doc = self._getPagDoc()
        if not doc: return
#DONE, check for macro recording
        if doc.recording:
            msg = 'Stop currently active macro recording?'
#FIX, Yes/No/Cancel dialog unclear
            ans = self._msg_box(self, 'WARN_ASK', msg)
            if ans in [wx.ID_NO, wx.ID_CANCEL]:  # keep in editor
                return False
            doc._macro_stop(None)
        if doc.IsModified():
#NOTE, FileClose starts 'modified' dialog
            msg = doc.filename + ' has been modified, save changes?'
            if not doc.dirname:
                msg = 'New file ' + msg
            ans = self._msg_box(self, 'WARN_ASK', msg)
            if ans == wx.ID_YES:       # save (as) and close
                if doc.dirname:
                    self._not_implemented(None, 'SAVE EXISTING FILE ')
                    res = self.FileSave(evt)
                else:
                    res = self.FileSaveAs(evt)
            elif ans == wx.ID_NO:      # discard and close
                pass
            elif ans == wx.ID_CANCEL:  # keep in editor
                return False

        # destroy this document's side panel tools
        for pnl in doc.spt:
            if pnl:
                pnl.ctrl.Destroy()
                pnl.Destroy()

        if not self.exit_called:
            if cfg['RecentFilesHistory']['Enable']:
                # skip new/unsaved file
                if doc.dirname:
                    self.hist.AddFileToHistory(doc.pathname)
                    if DEBUG['FHIST']: _dbg_FILE_HISTORY(self.hist)

        del doc
        self.nb.DeletePage(cur)

        # when no document open
        if not self.nb.PageCount:
            # clear main title and statusbar fields, close any open panels
            self.SetTitle('%s' % (appName))
#             self.ccx.ctrl.SetLabel('')
            self.schsp.Unsplit(self.schbotPanel)  # search
            self.versp.Unsplit(self.rightPanel)   # side
            self.horsp.Unsplit(self.topPanel)     # code
            self.midsp.Unsplit(self.midtopPanel)  # ruler
#FIX, SPLIT_EDITOR
#             self.edtsp.Destroy()
            # discard these actions when called from FileExit
            if not self.exit_called:
                for _id in ['LAY_SCH', 'LAY_RLR', 'LAY_SPN', 'LAY_CCX']:
                    self.mb.Check(MB[_id], False)
                for fld in SBF.keys():
                    self._set_statustext(TXT_NIL, fld)

        return True

    def FileCloseAll(self, evt):
        _dbg_funcname()
        # timing
        if DEBUG['TIMER']: close_time = now_()

        res = True
        pag = 0

        # update panel config before it's lost closing all files
        cfg['SearchPanel']['Enable'] = self.mb.IsChecked(MB['LAY_SCH'])
        if cfg['SearchPanel']['Enable']:
            cfg['SearchPanel']['Swap'] = self.schsp.swap
            cfg['SearchPanel']['Sash'] = self.schsp.SashPosition
        cfg['SearchPanel']['Mode'] = self.sch.mode
        cfg['SearchPanel']['FindText'] = self.sch.txt_fnd.Value
        cfg['SearchPanel']['WhereText'] = self.sch.txt_whr.Value
        cfg['SearchPanel']['ReplaceText'] = self.sch.txt_rpl.Value
        cfg['SearchPanel']['RegularExpression'] = self.sch.reg.Value
        cfg['SearchPanel']['CaseSensitive'] = self.sch.cas.Value
        cfg['SearchPanel']['WholeWord'] = self.sch.wrd.Value
        cfg['SearchPanel']['WrapAround'] = self.sch.wrp.Value
        cfg['SearchPanel']['InSelection'] = self.sch.isl.Value
        cfg['SearchPanel']['HighlightMatches'] = self.sch.hlm.Value
        cfg['SearchPanel']['PreserveCase'] = self.sch.pcs.Value

        cfg['Ruler']['Enable'] = self.mb.IsChecked(MB['LAY_RLR'])
        if cfg['Ruler']['Enable']:
            cfg['Ruler']['Swap'] = self.midsp.swap
            cfg['Ruler']['Sash'] = self.midsp.SashPosition

        cfg['SidePanel']['Enable'] = self.mb.IsChecked(MB['LAY_SPN'])
        cfg['SidePanel']['Choice'] = SPT['NIL']
        if cfg['SidePanel']['Enable']:
            cfg['SidePanel']['Swap'] = self.versp.swap
            cfg['SidePanel']['Sash'] = self.versp.SashPosition
            cfg['SidePanel']['Choice'] = self.spn.GetSelection()

        cfg['CodeContext']['Enable'] = self.mb.IsChecked(MB['LAY_CCX'])
        if cfg['CodeContext']['Enable']:
            cfg['CodeContext']['Swap'] = self.horsp.swap
            cfg['CodeContext']['Sash'] = self.horsp.SashPosition

        cur = self.nb.CurrentPage
        cfg['General']['ActiveFile'] = cur.pathname if cur else ''
        cfg['OpenFiles'] = dict()
        cnt = 0

        self.Freeze()   # avoid flicker
#FIX, change 'i' by 'pag'?
        for i in range(self.nb.PageCount):
            self.nb.SetSelection(pag)
            doc = self.nb.GetPage(pag)

            # skip new/unsaved file
            if doc.dirname:
                pnm = doc.pathname
                vis = str(doc.FirstVisibleLine + 1)
                pos = str(doc.CurrentPos)
                lin = str(doc.CurrentLine + 1)
                col = str(doc.GetColumn(doc.CurrentPos) + 1)
                lng = doc.langtype
                wrp = str(doc.WrapMode)
                eol = str(1 if doc.ViewEOL else 0)
                wsp = str(doc.ViewWhiteSpace)
                sel_str = str(doc.GetSelection())  # tuple -> string
                bmk_lst = doc._get_bookmarks()
                _dbg_BOOKMARK('EXIT', doc, bmk_lst)
                bmk_str = str(bmk_lst)  # list -> string
                val = '|'.join([pnm, vis, pos, lin, col, lng, wrp, eol, wsp, sel_str, bmk_str])
                cfg['OpenFiles']['File' + str(cnt)] = val
                cnt += 1

            if not self.FileClose(evt):
                pag += 1  # keep in editor, next file tab
                res = False
                # break  # cancel button quits close

#TODO, update many more cfg sections/keys below!
        if cfg['General']['FlushClipboard']:
            wx.TheClipboard.Flush()

#         cfg['General']['OpenSession'] = True
#         cfg['General']['DetectFileChange'] = False

#FIX, use '_update_margins' to derive 'All' value
#         self._update_margins()
#         cfg['Margin']['All'] = self.mb.IsChecked(MB['MGN_ALL'])
        cfg['Margin']['LineNumber'] = self.mb.IsChecked(MB['MGN_NUM'])
        cfg['Margin']['Symbol'] = self.mb.IsChecked(MB['MGN_SYM'])
        cfg['Margin']['Folding'] = self.mb.IsChecked(MB['MGN_FOL'])
#TODO, add fold_style to 3 docstate methods, FOR NOW it is GLOBAL
        cfg['Margin']['FoldingStyle'] = FOL_STYLE

        if self.mb.IsChecked(MB['EDG_NON']):
            cfg['Edge']['Mode'] = stc.STC_EDGE_NONE
        elif self.mb.IsChecked(MB['EDG_BCK']):
            cfg['Edge']['Mode'] = stc.STC_EDGE_BACKGROUND
        elif self.mb.IsChecked(MB['EDG_LIN']):
            cfg['Edge']['Mode'] = stc.STC_EDGE_LINE
        # elif self.mb.IsChecked(MB['EDG_MUL']):
        #     # cfg['Edge']['Mode'] = stc.STC_EDGE_MULTILINE
        #     cfg['Edge']['Mode'] = 3
        # cfg['Edge']['Column'] = doc.EdgeColumn
        # cfg['Edge']['Colour'] = doc.EdgeColour

        if self.mb.IsChecked(MB['IND_GDS']):
            cfg['Indentation']['Guides'] = stc.STC_IV_LOOKBOTH
        else:
            cfg['Indentation']['Guides'] = stc.STC_IV_NONE

        cfg['Caret']['HomeEndKeysBRIEF'] = self.mb.IsChecked(MB['CRT_BRF'])
        cfg['Caret']['LineVisible'] = self.mb.IsChecked(MB['CRT_LIN'])

        if self.mb.IsChecked(MB['CRT_STK']):
            cfg['Caret']['Sticky'] = stc.STC_CARETSTICKY_ON
        else:
            cfg['Caret']['Sticky'] = stc.STC_CARETSTICKY_OFF

        cfg['Search']['FindText'] = self.findtxt
        cfg['Search']['ReplaceText'] = self.repltxt
        # cfg['Search']['IncrementalText'] = self.incrtxt  # [NOT IMPLEMENTED]
        cfg['Search']['FindFlags'] = self.findflg
        cfg['Search']['FindRegex'] = self.findreg
        cfg['Search']['FindWrap'] = self.findwrp

#         cfg['Macro'][''] =

        cfg['Layout']['Toolbar'] = self.mb.IsChecked(MB['LAY_TBR'])
        cfg['Layout']['Statusbar'] = self.mb.IsChecked(MB['LAY_SBR'])
        cfg['Layout']['FileTabs'] = self.mb.IsChecked(MB['LAY_FTB'])
        cfg['Layout']['FileTabIcons'] = self.mb.IsChecked(MB['LAY_FTI'])
        cfg['Layout']['Tooltips'] = self.mb.IsChecked(MB['LAY_TTP'])
        cfg['Layout']['MenuIcons'] = self.icons  # self.mb.IsChecked(MB['LAY_MNI'])
        cfg['Layout']['MenuHelpText'] = self.hlp  # self.mb.IsChecked(MB['LAY_MNH'])
        cfg['Layout']['DistractionFree'] = not self.mb.IsEnabled(MB['LAY_FUL'])
        cfg['Layout']['FullScreen'] = self.mb.IsChecked(MB['LAY_FUL'])
        cfg['TopLineToolTip']['Enable'] = self.mb.IsChecked(MB['LAY_TLT'])

#FIX, handling of 3 ['Sash'] values below
#INFO, FileClose destroys any open panels before we get here
#         print(self.midsp.SashPosition)
#         print(self.versp.SashPosition)
#         print(self.horsp.SashPosition)

        cfg['RecentFiles'] = dict()

        if cfg['RecentFilesHistory']['Enable']:
            for i in range(self.hist.Count):
                cfg['RecentFiles']['File' + str(i)] = self.hist.GetHistoryFile(i)

        # window position, width, height
        cfg['Window']['PositionX'] = self.Position[0]
        cfg['Window']['PositionY'] = self.Position[1]
        cfg['Window']['Width'] = self.Size[0]
        cfg['Window']['Height'] = self.Size[1]

        CfgWrite(cfg)

        # timing
        if DEBUG['TIMER']:
            close_time = now_() - close_time
            print('  close_time: %6d ms' % (close_time))

        self.Thaw()
        return res

#FIX, integrate/finish/test code 'FileCloseOther'/'FileCloseLeftOrRight'
    def FileCloseOther(self, evt):
        _dbg_funcname()
        cnt1 = self.FileCloseLeft(evt)
        cnt2 = self.FileCloseRight(evt)
        self._push_statustext('Closed %d documents' % (cnt1 + cnt2))

#FIX, finish/test code 'FileCloseLeftOrRight'
    def FileCloseLeftOrRight(self, evt):
        _dbg_funcname()
        _id = evt.Id
        if DEBUG['BASIC']: print('  Left' if _id == MB['NBK_CAL'] else '  Right')
        res = True
        cur = self.nb.Selection
        pag = 0 if _id == MB['NBK_CAL'] else cur + 1
        rng = list(range(cur)) if _id == MB['NBK_CAL'] else list(range(cur + 1, self.nb.PageCount))
        cnt = 0

        for i in rng:
            self.nb.SetSelection(pag)
            if not self.FileClose(evt):
                res = False
            else:
                cnt += 1

        if cnt > 0:
            self._push_statustext('Closed %d documents' % (cnt))

        return cnt

#TODO, integrate with 'FileCloseRight' in 'FileCloseLeftOrRight'
    def FileCloseLeft(self, evt):
        _dbg_funcname()
        res = True
        cur = self.nb.Selection
        pag = 0
        cnt = 0

        for i in range(cur):
            self.nb.SetSelection(pag)
            if not self.FileClose(evt):
                res = False
            else:
                cnt += 1

        if cnt > 0:
            self._push_statustext('Closed %d documents' % (cnt))

        return cnt

#TODO, integrate with 'FileCloseLeft' in 'FileCloseLeftOrRight'
    def FileCloseRight(self, evt):
        _dbg_funcname()
        res = True
        cur = self.nb.Selection
        pag = cur + 1
        cnt = 0

        for i in range(cur + 1, self.nb.PageCount):
            self.nb.SetSelection(pag)
            if not self.FileClose(evt):
                res = False
            else:
                cnt += 1

        if cnt > 0:
            self._push_statustext('Closed %d documents' % (cnt))

        return cnt

    def FileExit(self, evt):
        _dbg_funcname()
        self.exit_called = True
        res = False
        if not FAST_EXIT:
            res = self.FileCloseAll(evt)
        noit()
        if res or FAST_EXIT:
            self.Destroy()
            if cfg['General']['SystemTrayMenu']:
                self.stm.Destroy()

    @_getdoc(1)
    def EditUndo(self, doc, evt):
    # def EditUndo(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        if doc.CanUndo():
            doc.Undo()
        else:
#FIX, message never shows, see UpdateUIDoc
            self._set_statustext('End of undo history buffer')

    @_getdoc(2)
    def EditRedo(self, doc, evt):
    # def EditRedo(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        if doc.CanRedo():
            doc.Redo()
        else:
#FIX, message never shows, see UpdateUIDoc
            self._set_statustext('End of redo history buffer')

    def EditClipboard(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        _id = evt.Id

#TODO: create and init dict/list 'cnt' for 'cnt' and 'cut/cpy/pst_cnt' ?
#         cnt = {'sel': 0, 'cut': 0, 'cpy': 0, 'pst': 0, }
        cnt = doc.Selections

        if cfg['MultiEdit']['Clipboard'] and cnt >= 2:
            if _id in [MB['EDT_CUT'], MB['EDT_CPY']]:
                self.multi_clipboard = list()
            elif _id in [MB['EDT_PST']]:
                if not self.multi_clipboard:
                    self._push_statustext('Multi clipboard empty, unable to paste')
                    return
            # set stream selection, rectangular does not work here
            doc.SetSelectionMode(stc.STC_SEL_STREAM)
            doc.BeginUndoAction()
            # save selections
            sel_list = list()
            pos = doc.CurrentPos
            for sel in range(cnt):
                anchor = doc.GetSelectionNAnchor(sel)
                caret = doc.GetSelectionNCaret(sel)
                # process selection left to right
                if anchor > caret:
                    anchor, caret = caret, anchor
                txt = doc.GetTextRange(anchor, caret)
                sel_list.append([anchor, caret, txt])
            # process selections top to bottom
            sel_list.sort()
            # remove selections
            doc.SelectNone()
            doc.SetSelection(pos, pos)
            # clipboard action per selection
            cut_cnt = cpy_cnt = pst_cnt = 0
            for sel in range(cnt):
                if DEBUG['MULCB']: print('%d: %s - ' % (sel, sel_list[sel][:2]), end='')
                anchor, caret, txt = sel_list[sel]
                if _id in [MB['EDT_CUT']]:
                    anchor -= cut_cnt
                    caret = anchor
                    doc.DeleteRange(anchor, len(txt))
                    self.multi_clipboard.append(txt)
                    cut_cnt += len(txt)
                elif _id in [MB['EDT_CPY']]:
                    self.multi_clipboard.append(txt)
                    cpy_cnt += len(txt)
                elif _id in [MB['EDT_PST']]:
                    anchor -= cut_cnt
                    anchor += pst_cnt
                    caret = anchor  # + len(self.multi_clipboard[sel])
                    doc.DeleteRange(anchor, len(txt))
                    cut_cnt += len(txt)
                    # paste if clipboard length permits
                    if sel < len(self.multi_clipboard):
                        doc.InsertText(anchor, self.multi_clipboard[sel])
                        pst_cnt += len(self.multi_clipboard[sel])
                sel_list[sel] = [anchor, caret, txt]
                if DEBUG['MULCB']: print('%s' % (sel_list[sel][:2]))
            # restore selections
            for sel in range(cnt):
                anchor, caret, txt = sel_list[sel]
                if sel == doc.MainSelection:
                    doc.SetSelection(anchor, caret)
                else:
                    doc.AddSelection(caret, anchor)
            # doc.SetSelection(anchor, caret)
            doc.EndUndoAction()
            self._push_statustext('Multi clipboard: cut=%d, copy=%d, paste=%d' % (cut_cnt, cpy_cnt, pst_cnt))
            if DEBUG['MULCB']: print('Multi clipboard[%d]: %s' % (len(self.multi_clipboard), self.multi_clipboard))
        else:
            if _id == MB['EDT_CUT']:
                doc.Cut()
            elif _id == MB['EDT_CPY']:
                doc.Copy()
            elif _id == MB['EDT_PST']:
                doc.Paste()

    def EditDelete(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        txt = doc.SelectedText
        if len(txt):
            doc.Clear()

    def EditHighlightMatches(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        doc.HighlightMatches(None)

    def EditCopyFilename(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        fnm = doc.pathname  # fully qualified
        doc.CopyText(len(fnm), fnm)
#DONE, add list of (dirname, filename, basename, ext) to Editor class (doc object)
        self._set_statustext('Filename [%s] -> copied to clipboard' % fnm)

    def EditMoveCaretTo(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        _id = evt.Id
        top = doc.FirstVisibleLine
        los = doc.LinesOnScreen()
        if _id == MB['CRT_TOP']:
            txt = 'top'
            doc.GotoLine(top)
        elif _id == MB['CRT_CTR']:
            txt = 'centre'
            doc.GotoLine(top + (los // 2))
        elif _id == MB['CRT_BOT']:
            txt = 'bottom'
            doc.GotoLine(top + los - 1)
        if txt:
            if DEBUG['SCROL']: print('  %s' % txt)
            self._push_statustext('Moved caret to ' + txt)

    def EditToParagraph(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        _id = evt.Id
        if _id == MB['PAR_NXT']:
            if DEBUG['BASIC']: print('  Next')
            doc.ParaDown()
        elif _id == MB['PAR_PRV']:
            if DEBUG['BASIC']: print('  Previous')
            doc.ParaUp()

    def EditDuplicateLine(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        doc.LineDuplicate()

    def EditTransposeLine(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        doc.LineTranspose()

    def EditScrollLineTo(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        _id = evt.Id
        if _id == MB['LIN_TOP']:
            txt = 'top'
            doc.SetFirstVisibleLine(doc.CurrentLine)
        elif _id == MB['LIN_CTR']:
            txt = 'centre'
            doc.VerticalCentreCaret()
        elif _id == MB['LIN_BOT']:
            txt = 'bottom'
            doc.ScrollToLine(doc.CurrentLine - doc.LinesOnScreen() + 1)
        if txt:
            if DEBUG['SCROL']: print('  %s' % txt)
            self._push_statustext('Scrolled current line to ' + txt)

    def EditMoveSelectedLines(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        _id = evt.Id
        if _id == MB['LIN_SLD']:
            txt = 'down'
            doc.MoveSelectedLinesDown()
        elif _id == MB['LIN_SLU']:
            txt = 'up'
            doc.MoveSelectedLinesUp()
        if txt:
            if DEBUG['SCROL']: print('  %s' % txt)
            self._push_statustext('Moved selected line(s) ' + txt)
        # doc.SwapMainAnchorCaret()

    def EditAutoComplete(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        doc.AutoComplete(evt)

    def EditSortLines(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return

        # force line-based selection
        txt, slin, elin, spos, epos = doc._selection_to_line()
        # more than 1 line selected?
        if slin != elin:
            doc.BeginUndoAction()
            _id = evt.Id
            txt = txt.split(doc.newline)
            if _id in [MB['SRT_LIN'], TB['SRT']]:
                txt.sort()
            elif _id == MB['SRT_REV']:
                txt.sort(reverse=True)
            elif _id == MB['SRT_UNQ']:
                txt = sorted(set(txt))
            txt = str(doc.newline.join(txt))
            doc.ReplaceSelection(txt)
            # reselect after sort
            epos = spos + len(txt)
            doc.SetSelection(spos, epos)
            doc.EndUndoAction()

    def EditCalcSumText(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        txt = doc.SelectedText
        if len(txt):
#FIX, use '.splitlines()'
            txt = list(txt.split(doc.newline))
            tot = 0.0
            for lin in txt:
                if len(lin):
                    try:
                        val = float(lin)
                    except ValueError:
                        pass
                    else:
                        tot += val
            doc.CopyText(len(str(tot)), str(tot))
            self._set_statustext('Sum of selection: [%.1f] -> copied to clipboard' % tot)

#INFO, URL=https://stackoverflow.com/questions/33783727/how-can-i-update-a-wxpython-listbox-based-on-some-search-string
    def ViewOpenFileList(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return

        # Create list of open documents
        doc_lst = list()
        pag_lst = list()
        for i in range(self.nb.PageCount):
            fnm = self.nb.GetPage(i).dirname + '\\' + self.nb.GetPage(i).filename
            doc_lst.append(fnm)
            pag_lst.append(i)  # track tab page number for file

        if DEBUG['FILE']: print('\nFile List (tab order):') ; pp(list(enumerate(doc_lst, start=1)))
        if DEBUG['FILE']: print('\nFile List (sort name):') ; pp(list(enumerate(sorted(doc_lst), start=1)))

        def on_char(evt):
            evt.Skip()
            # get the entered string in TextCtrl
            getValue = dlg.searchExpectedResults.Value
        #     print(getValue)
            # Clear ListBox
            dlg.listExpectedResults.Clear()
            # Append matching strings in doc_lst to ListBox
            for item in sorted(doc_lst):
                if getValue in item:
        #             print(item)
                    dlg.listExpectedResults.Append(item)

        def on_select(evt):
            if DEBUG['FILE']: print('key OK = [%d], ID = [%d]' % (wx.ID_OK, evt.Id))
            if DEBUG['FILE']: print('select item [%d] = [%s]:' % (evt.Selection + 1, evt.String))
            # print('select item [%d] = [%s]:' % (dlg.listExpectedResults.Selection+1, dlg.listExpectedResults.GetString(dlg.listExpectedResults.Selection)))

#FIX, Enter key not working in dialog: 'ValueError: '' is not in list'
            idx = doc_lst.index(evt.String)     # find selected filename
            self.nb.SetSelection(pag_lst[idx])  # use index for its page tab

            on_exit(None)

        def on_fuzzy(evt):
            dlg.fuzzy = True if dlg.searchFuzzy.IsChecked() else False
        #     print('fuzzy =', dlg.fuzzy)

        def on_exit(evt):
            dlg.Destroy()

        sty = wx.CAPTION | wx.CLOSE_BOX
        dlg = wx.Dialog(self, title='Open File List', style=sty)
        self._set_icon(dlg)

        dlg.okButton = wx.Button(dlg, wx.ID_OK, '&OK', size=(75, 25))
        dlg.cancelButton = wx.Button(dlg, wx.ID_CANCEL, '&Cancel', size=(75, 25))
        dlg.searchExpectedResults = wx.TextCtrl(dlg, -1, '', size=(250, 25))
        dlg.searchFuzzy = wx.CheckBox(dlg, -1, '&Fuzzy Search', size=(250, 25))
        dlg.listExpectedResults = wx.ListBox(dlg, choices=doc_lst, size=(330, 250))

        sizer = wx.GridBagSizer(vgap=5, hgap=5)
        sizer.Add(dlg.okButton, (0, 1), (1, 1), wx.TOP | wx.RIGHT, 10)
        sizer.Add(dlg.cancelButton, (1, 1), (1, 1), wx.RIGHT, 10)
        sizer.Add(dlg.searchExpectedResults, (0, 0), (1, 1), wx.TOP | wx.LEFT, 10)
        sizer.Add(dlg.searchFuzzy, (1, 0), (1, 1), wx.LEFT, 10)
        sizer.Add(dlg.listExpectedResults, (2, 0), (1, 2), wx.LEFT | wx.BOTTOM, 10)

        # Bind an EVT_CHAR event to your TextCtrl
        dlg.okButton.Bind(wx.EVT_BUTTON, on_select)
        dlg.cancelButton.Bind(wx.EVT_BUTTON, on_exit)
        dlg.searchExpectedResults.Bind(wx.EVT_KEY_UP, on_char)
        dlg.searchFuzzy.Bind(wx.EVT_CHECKBOX, on_fuzzy)
        dlg.listExpectedResults.Bind(wx.EVT_LISTBOX_DCLICK, on_select)
        dlg.Bind(wx.EVT_CLOSE, on_exit)

        dlg.okButton.SetDefault()
        _dbg_FOCUS(dlg.searchExpectedResults)

        dlg.Sizer = sizer
        dlg.Sizer.Fit(dlg)
        dlg.Centre(wx.BOTH)
        dlg.Show()

    def ViewSidePanelTool(self, evt):
        _dbg_funcname()
        # open side panel when closed
        if not self.versp.IsSplit():
            self.LayoutSidePanel(evt)
#FIX, error when called from toolbar, "in wxBookCtrlBase::DoSetSelection(): invalid page index"
        self.spn.SetSelection(evt.Id - int(MB['SPT_DCL']) + 1)

    def ViewWordWrap(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        self.mb.Check(evt.Id, evt.IsChecked())
        doc.SetWrapMode(stc.STC_WRAP_NONE if doc.WrapMode else stc.STC_WRAP_WORD)

    def ViewEndOfLine(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        self.mb.Check(evt.Id, evt.IsChecked())
        doc.SetViewEOL(False if doc.ViewEOL else True)

    def ViewWhiteSpace(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        self.mb.Check(evt.Id, evt.IsChecked())
        doc.SetViewWhiteSpace(False if doc.ViewWhiteSpace else True)

    def ViewIndentGuides(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        self.mb.Check(evt.Id, evt.IsChecked())
        doc.SetIndentationGuides(stc.STC_IV_NONE if doc.IndentationGuides else stc.STC_IV_REAL)

    @staticmethod
    def ViewCaretHomeEndKeysBRIEF(evt):
        _dbg_funcname()
        pass  # stub method

    def ViewCaretLine(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        self.mb.Check(evt.Id, evt.IsChecked())
        doc.SetCaretLineVisible(False if doc.CaretLineVisible else True)

    def ViewCaretSticky(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        self.mb.Check(evt.Id, evt.IsChecked())
        doc.SetCaretSticky(stc.STC_CARETSTICKY_OFF if doc.CaretSticky else stc.STC_CARETSTICKY_ON)

    def ViewAllMargins(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        num = cfg['Margin']['LineNumberWidth']
        sym = cfg['Margin']['SymbolWidth']
        fol = cfg['Margin']['FoldingWidth']
        items = (MB['MGN_ALL'], MB['MGN_NUM'], MB['MGN_SYM'], MB['MGN_FOL'])
        types = {MGN['NUM']: num, MGN['SYM']: sym, MGN['FOL']: fol}

        # process all margin menu items
        chk = evt.IsChecked()
        for m in items:
            self.mb.Check(m, True if chk else False)
        for t, w in types.items():
            doc.SetMarginWidth(t, w if chk else 0)
        # update ruler alignment when visible
        if self.midsp.IsSplit():
            self.rlr.set_offset((num + sym + fol if chk else 0) - doc.XOffset)

    def ViewMargin(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        _id = evt.Id
        if _id == MB['MGN_NUM']:
            mgn = MGN['NUM']
            wid = cfg['Margin']['LineNumberWidth']
        elif _id == MB['MGN_SYM']:
            mgn = MGN['SYM']
            wid = cfg['Margin']['SymbolWidth']
        elif _id == MB['MGN_FOL']:
            mgn = MGN['FOL']
            wid = cfg['Margin']['FoldingWidth']
        self.mb.Check(_id, evt.IsChecked())
        doc.SetMarginWidth(mgn, 0 if doc.GetMarginWidth(mgn) != 0 else wid)
        self._update_margins()

    def ViewEdge(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        if self.mb.IsChecked(MB['EDG_NON']):
            print('STC_EDGE_NONE')
            doc.SetEdgeMode(stc.STC_EDGE_NONE)
        elif self.mb.IsChecked(MB['EDG_BCK']):
            print('STC_EDGE_BACKGROUND')
            doc.SetEdgeMode(stc.STC_EDGE_BACKGROUND)
        elif self.mb.IsChecked(MB['EDG_LIN']):
            print('STC_EDGE_LINE')
            doc.SetEdgeMode(stc.STC_EDGE_LINE)
        # elif self.mb.IsChecked(MB['EDG_MUL']):
        #     print('SetEdgeMode(3)')
        #     # doc.SetEdgeMode(stc.STC_EDGE_MULTILINE)
        #     doc.MultiEdgeClearAll()
        #     doc.MultiEdgeAddLine(10, CLR['RED'])
        #     doc.MultiEdgeAddLine(20, CLR['RED'])
        #     doc.MultiEdgeAddLine(30, CLR['RED'])
        #     doc.MultiEdgeAddLine(40, CLR['RED'])
        #     doc.MultiEdgeAddLine(50, CLR['RED'])
        #     doc.MultiEdgeAddLine(60, CLR['RED'])
        #     doc.SetEdgeMode(3)

    def ViewEdgeColumn(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        dlg = wx.TextEntryDialog(self, 'Enter number:', 'Edge column', str(doc.EdgeColumn + 1))
        self._set_icon(dlg)
        ans = dlg.ShowModal()
        col = int(dlg.Value) - 1
        dlg.Destroy()
        if ans == wx.ID_OK:
            doc.SetEdgeColumn(col)

    def ViewEdgeColour(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        # get edge colour
        dta = wx.ColourData()
        dta.SetColour(wx.Colour(doc.EdgeColour))
        # pass it to dialog
        dlg = wx.ColourDialog(self, dta)
        self._set_icon(dlg)
        dlg.ColourData.SetChooseFull(False)
        dlg.Centre()
        ans = dlg.ShowModal()
        # get colour selection
        dta = dlg.ColourData
        rgb = dta.Colour.Get(includeAlpha=False)
        clr = "#%02x%02x%02x" % rgb
        dlg.Destroy()
        # pass it to edge
        if ans == wx.ID_OK:
            doc.SetEdgeColour(clr)

    def ViewFoldingStyle(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        if doc.fold_style < FOL_STY_SQR:
            doc.fold_style += 1
        else:
            doc.fold_style = FOL_STY_NIL
        doc.FoldStyling()

    def ViewZoomReset(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        doc.SetZoom(0)

    def ViewZoomIn(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        doc.SetZoom(doc.Zoom + 1)

    def ViewZoomOut(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        doc.SetZoom(doc.Zoom - 1)

    def ViewStatistics(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
#TODO, only works on Python source code
        if doc.langtype != 'python':
            self._not_implemented(None, '[%s] LANGUAGE STATISTICS' % doc.langname)
            return
#TODO, create better output dialog w/ button for 'clipboard copy'
        wx.BeginBusyCursor()
        out = check_output(['radon', 'raw', doc.pathname])
        wx.EndBusyCursor()
#NOTE, py3: decode 'out' data type: bytes -> str prevents error:
#NOTE,     'TypeError: can only concatenate str (not "bytes") to str'
#FIX, doc.filename -> doc.pathname
        msg = '\'' + doc.filename + '\' statistics\n\n' + out.decode('utf-8')
        ans = self._msg_box(self, 'INFO', msg)

    def ViewReadOnly(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        doc.SetReadOnly(False if doc.ReadOnly else True)
        self._update_page_tabs(doc)

#TODO, integrate with _selection_to_line()
    def SelectSplitIntoLines(self, evt):
        __, doc = self._getPagDoc()
        if not doc: return
        sel = doc.GetSelection()
        spos = sel[0]
        epos = sel[1]
        slin = doc.LineFromPosition(spos)
        elin = doc.LineFromPosition(epos)
        cnt = elin - slin + 1
        # more than 1 line selected?
        if cnt >= 2:
            # remove single selection
            doc.SelectNone()
            doc.SetSelection(spos, spos)
            # split single into multiple selection per line
            for s in range(cnt):
                anchor = spos if s == 0 else doc.PositionFromLine(slin + s)
                caret = epos if s == cnt - 1 else doc.GetLineEndPosition(slin + s)
                if s == doc.MainSelection:
                    doc.SetSelection(anchor, caret)
                else:
                    doc.AddSelection(caret, anchor)
        # else:
        #     self._push_statustext('Need at least 2 selected lines to split')

    def SelectAddLine(self, evt):
        __, doc = self._getPagDoc()
        if not doc: return
        _id = evt.Id
        if _id == MB['SEL_APL']:
            doc.LineUpRectExtend()
        elif _id == MB['SEL_ANL']:
            doc.LineDownRectExtend()
#FIX, weird delete behaviour using Backspace
        doc.SetSelectionMode(stc.STC_SEL_THIN)

    def SelectAll(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        doc.SelectAll()

    def SelectWord(self, evt):
        __, doc = self._getPagDoc()
        if not doc: return
        doc._select_next_word(evt)

    def SelectLine(self, evt):
        __, doc = self._getPagDoc()
        if not doc: return
        sel = doc.GetSelection()
        spos = sel[0]
        epos = sel[1]
        slin = doc.LineFromPosition(spos)
        elin = doc.LineFromPosition(epos)
        if spos != doc.PositionFromLine(slin) or epos != doc.PositionFromLine(elin):
            spos = doc.PositionFromLine(slin)
            epos = doc.PositionFromLine(elin)
            doc.Home()  # caret sticks to 1st column
            doc.SetSelection(spos, epos)
        doc.LineDownExtend()

    def SelectParagraph(self, evt):
        __, doc = self._getPagDoc()
        if not doc: return
        doc.ParaDown()
        doc.Home()  # caret sticks to 1st column
        doc.LineUp()
        doc.ParaUpExtend()
        doc.SwapMainAnchorCaret()

    def SelectBraces(self, evt):
        __, doc = self._getPagDoc()
        if not doc: return

        # check for brace in immediate vicinity and select
        res = self.SearchBraceMatch(evt)

        # check for brace farther away?
        if not res:
            cur = doc.CurrentPos
            prs = cfg['BraceMatch']['CharacterPairs']
            fnd = '[\\' + '\\'.join(prs) + ']'
            flg = stc.STC_FIND_REGEXP
            # search backward for unbalanced opening brace
            cnt_list = [0, 0, 0, 0]
            open_pos = stc.STC_INVALID_POSITION
            pos = cur
            while True:
                pos = doc.FindText(pos, 0, fnd, flags=flg)
                if pos == stc.STC_INVALID_POSITION:
                    break
                brc = chr(doc.GetCharAt(pos))
                idx = prs.index(brc)
                cnt_list[idx % 4] -= 1 if idx < 4 else -1
                chk = len([c for c in cnt_list[:3] if c < 0])  # discard '<'
                if chk:
                    open_pos = pos
                    open_brc = brc
                    # print(chk, pos)
                    break
            # search forward for unbalanced closing brace
            cnt_list = [0, 0, 0, 0]
            close_pos = stc.STC_INVALID_POSITION
            pos = cur
            while True:
                pos = doc.FindText(pos, doc.LastPosition, fnd, flags=flg)
                if pos == stc.STC_INVALID_POSITION:
                    break
                brc = chr(doc.GetCharAt(pos))
                idx = prs.index(brc)
                cnt_list[idx % 4] -= 1 if idx >= 4 else -1
                chk = len([c for c in cnt_list[:3] if c < 0])  # discard '>'
                if chk:
                    close_pos = pos
                    close_brc = brc
                    # print(chk, pos)
                    break
#NOTE, workaround: prevents loop forever
                pos += 1
            # brace pair found?
            if DEBUG['BRACE']: print('  SelectBraces:')
            if stc.STC_INVALID_POSITION not in [open_pos, close_pos]:
                # corresponding braces?
                if prs.index(open_brc) + 4 == prs.index(close_brc):
                    doc.SetSelection(open_pos + 1, close_pos)
                    if DEBUG['BRACE']: print('    found:', open_pos, close_pos, open_brc, close_brc)
            else:
                if DEBUG['BRACE']: print('    NOT found')

            if DEBUG['BRACE']: print('    count: %s, total: %d' % (cnt_list, sum(cnt_list)))

    def SelectIndentation(self, evt):
        __, doc = self._getPagDoc()
        if not doc: return

        # get indentation for current line
        pos = doc.CurrentPos
        cur = doc.LineFromPosition(pos)
        ind = doc.GetLineIndentation(cur)
        print('indent: %d' % (ind))

        if ind > 0:
            # get 1st line above with smaller indentation
            lin = cur
            while True:
                lin -= 1
                if doc.GetLineIndentation(lin) < ind:
                    # discard whitespace only line
                    if not doc.GetLine(lin).strip():
                        continue
                    break
            start = lin + 1
            # get last line below with smaller indentation
            lin = cur
            while True:
                lin += 1
                if doc.GetLineIndentation(lin) < ind:
                    # discard whitespace only line
                    if not doc.GetLine(lin).strip():
                        continue
                    break
            end = lin
            # create selection
            start = doc.PositionFromLine(start)
            end = doc.PositionFromLine(end)
            doc.SetSelection(start, end)

    def SelectSwapAnchorCaret(self, evt):
        __, doc = self._getPagDoc()
        if not doc: return
        cnt = doc.Selections
        # swap selection(s)
        for s in range(cnt):
            anchor = doc.GetSelectionNAnchor(s)
            caret = doc.GetSelectionNCaret(s)
            doc.SetSelectionNAnchor(s, caret)
            doc.SetSelectionNCaret(s, anchor)
        doc.EnsureCaretVisible()
        self._push_statustext('Swapped %d anchor/caret selection pairs' % cnt)

#####################
# temporary code
#####################
    def TESTMETHOD(self, evt):
        # __, doc = self._getPagDoc()
        # if not doc: return

        self.mb.EnableTop(6, False)
        self.mb.EnableTop(11, False)

        pass
#####################
# temporary code
#####################

#FIX, REFACTOR FIND FUNCTIONALITY
    def SearchFind(self, evt):
        _dbg_funcname()
        if not self.schsp.IsSplit():
            self.LayoutSearchPanel(None)
#DONE, update SASH['SCH'] in config
        pos = SASH['SCH']['FND']
        self.schsp.SetSashPosition(pos if self.schsp.swap else -pos)
        self.sch.SetLayout('FND')

#NOTE, OBSOLETE FIND CODE
        # if not isinstance(self.dlg_fnd, FindReplaceDialog):  # prevent > 1 class instance
        #     __, doc = self._getPagDoc()
        #     if not doc: return
        #     self.dlg_fnd = FindReplaceDialog(doc, 'FIND')

#FIX, REFACTOR FIND FUNCTIONALITY
    def SearchReplace(self, evt):
        _dbg_funcname()
        if not self.schsp.IsSplit():
            self.LayoutSearchPanel(None)
#DONE, update SASH['SCH'] in config
        pos = SASH['SCH']['RPL']
        self.schsp.SetSashPosition(pos if self.schsp.swap else -pos)
        self.sch.SetLayout('RPL')

#NOTE, OBSOLETE FIND CODE
        # if not isinstance(self.dlg_fnd, FindReplaceDialog):  # prevent > 1 class instance
        #     __, doc = self._getPagDoc()
        #     if not doc: return
        #     self.dlg_fnd = FindReplaceDialog(doc, 'REPLACE')

#FIX, REFACTOR FIND FUNCTIONALITY
    def SearchFindInFiles(self, evt):
        _dbg_funcname()
        if not self.schsp.IsSplit():
            self.LayoutSearchPanel(None)
#DONE, update SASH['SCH'] in config
        pos = SASH['SCH']['FIF']
        self.schsp.SetSashPosition(pos if self.schsp.swap else -pos)
        self.sch.SetLayout('FIF')

#FIX, REFACTOR FIND FUNCTIONALITY
    def SearchFindNext(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        if self.findtxt:
            FindReplaceDialog(doc, 'NEXT')._exec_find_next(self.findtxt, self.findflg)
        else:
            self._push_statustext('Empty find string: starting dialog')
            if not self.findflg & wx.FR_DOWN:
                self.findflg += wx.FR_DOWN
            self.SearchFind(evt)

#FIX, REFACTOR FIND FUNCTIONALITY
    def SearchFindPrev(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        if self.findtxt:
            FindReplaceDialog(doc, 'PREV')._exec_find_prev(self.findtxt, self.findflg)
        else:
            self._push_statustext('Empty find string: starting dialog')
            if self.findflg & wx.FR_DOWN:
                self.findflg -= wx.FR_DOWN
            self.SearchFind(evt)

#FIX, REFACTOR FIND FUNCTIONALITY
    def SearchToggleCase(self, evt):
        _dbg_funcname()
        if DEBUG['FIND']: print('   IN: findflg =', self.findflg)
        if self.findflg & wx.FR_MATCHCASE:
            self.mb.Check(evt.Id, False)
            self.findflg -= wx.FR_MATCHCASE
        else:
            self.mb.Check(evt.Id, True)
            self.findflg += wx.FR_MATCHCASE
        if DEBUG['FIND']: print('  OUT: findflg =', self.findflg)

#TODO, implement REGEX
#FIX, REFACTOR FIND FUNCTIONALITY
    def SearchToggleRegex(self, evt):
        _dbg_funcname()
        self._not_implemented(None, 'REGEX')
#####################
# temporary code
#####################
        if DEBUG['FIND']: print('   IN: findreg =', self.findreg)
        self.findreg = not self.findreg
        self.mb.Check(MB['SCH_REG'], self.findreg)
        if DEBUG['FIND']: print('  OUT: findreg =', self.findreg)
#####################
# END: temporary code
#####################
#         if DEBUG['FIND']: print('   IN: findflg =', self.findflg)
#         if self.findflg & stc.STC_FIND_REGEXP:
#             self.mb.Check(evt.Id, False)
#             self.findflg -= stc.STC_FIND_REGEXP
#         else:
#             self.mb.Check(evt.Id, True)
#             self.findflg += stc.STC_FIND_REGEXP
#         if DEBUG['FIND']: print('  OUT: findflg =', self.findflg)

#FIX, REFACTOR FIND FUNCTIONALITY
    def SearchToggleWord(self, evt):
        _dbg_funcname()
        if DEBUG['FIND']: print('   IN: findflg =', self.findflg)
        if self.findflg & wx.FR_WHOLEWORD:
            self.mb.Check(evt.Id, False)
            self.findflg -= wx.FR_WHOLEWORD
        else:
            self.mb.Check(evt.Id, True)
            self.findflg += wx.FR_WHOLEWORD
        if DEBUG['FIND']: print('  OUT: findflg =', self.findflg)

#FIX, REFACTOR FIND FUNCTIONALITY
    def SearchToggleBackwards(self, evt):
        _dbg_funcname()
        if DEBUG['FIND']: print('   IN: findflg =', self.findflg)
        if self.findflg & wx.FR_DOWN:
            self.mb.Check(evt.Id, True)
            self.findflg -= wx.FR_DOWN
        else:
            self.mb.Check(evt.Id, False)
            self.findflg += wx.FR_DOWN
        if DEBUG['FIND']: print('  OUT: findflg =', self.findflg)

#FIX, REFACTOR FIND FUNCTIONALITY
    def SearchToggleWrap(self, evt):
        _dbg_funcname()
        if DEBUG['FIND']: print('   IN: findwrp =', self.findwrp)
        self.findwrp = not self.findwrp
        self.mb.Check(MB['SCH_WRP'], self.findwrp)
        if DEBUG['FIND']: print('  OUT: findwrp =', self.findwrp)

##################################################################################
# copied from PyPE
##################################################################################
    def SearchClearBookmarks(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        doc._clear_bookmarks()

    def SearchToggleBookmark(self, evt, line=None):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        lin = doc.CurrentLine if line is None else line

#TODO, integrate with 'MarginBookmark'
        # force bookmark list control creation
        if not doc.spt[SPT['BMK']]:
            self.spn.SetSelection(SPT['BMK'])
            # self.spn.PageChanged(None)

        # update document map panel/control
        dcp = doc.spt[SPT['DCM']]
        if dcp:
            dcp.Refresh()  # force 'preview doc' update

        if DEBUG['BOOKM']: print(doc.MarkerGet(lin))

        # if doc.MarkerGet(lin) & MRK['NTF']['MSK']:
        #     doc.MarkerDelete(lin, MRK['NTF']['NUM'])
        if doc.MarkerGet(lin) & MRK['BMK']['MSK']:
            doc.MarkerDelete(lin, MRK['BMK']['NUM'])
        else:
            doc.MarkerAdd(lin, MRK['BMK']['NUM'])

        if DEBUG['BOOKM']: print(doc.MarkerGet(lin))

#TODO, integrate with 'MarginBookmark'
        # UPDATE bookmarks in list control
        blc = doc.spt[SPT['BMK']].ctrl  # bookmark list control
        blc.DeleteAllItems()
        blc.UpdateListCtrl(doc)

    def SearchBookmark(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        _id = evt.Id
        cur = doc.CurrentLine

        # force panel visibility
        if cfg['Bookmark']['SearchShowPanel']:
            if not self.versp.IsSplit():
                self.LayoutSidePanel(evt)
            if not self.spn.GetSelection() == SPT['BMK']:
                self.spn.SetSelection(SPT['BMK'])

        if _id == MB['BMK_NXT']:
            if DEBUG['BOOKM']: print('  Next bookmark')
            lin = doc.MarkerNext(cur + 1, MRK['BMK']['MSK'])
        elif _id == MB['BMK_PRV']:
            if DEBUG['BOOKM']: print('  Previous bookmark')
            lin = doc.MarkerPrevious(cur - 1, MRK['BMK']['MSK'])

        if lin != stc.STC_INVALID_POSITION:
            doc.GotoLine(lin)
        elif cfg['Bookmark']['SearchWrap']:
            if _id == MB['BMK_NXT']:
                lin = doc.MarkerNext(0, MRK['BMK']['MSK'])
            elif _id == MB['BMK_PRV']:
                lin = doc.MarkerPrevious(doc.LineCount, MRK['BMK']['MSK'])
            if lin != stc.STC_INVALID_POSITION:
                doc.GotoLine(lin)

        if lin != stc.STC_INVALID_POSITION:
            if cfg['Bookmark']['SearchCentreCaret']:
                doc.VerticalCentreCaret()
            # bookmark list control
            blc = doc.spt[SPT['BMK']].ctrl if doc.spt[SPT['BMK']] else None
            if blc and cfg['Bookmark']['SearchSyncPanel']:
                for idx in range(blc.ItemCount):
                    if lin == int(blc.GetItemText(idx, 2)) - 1:  # lineno
                        blc.Select(idx)
                        blc.Focus(idx)

        _dbg_FOCUS(doc)
##################################################################################
# END: copied from PyPE
##################################################################################

    def SearchTask(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        _id = evt.Id
        cur = doc.CurrentPos

        # force panel visibility
        if cfg['Task']['SearchShowPanel']:
            if not self.versp.IsSplit():
                self.LayoutSidePanel(evt)
            if not self.spn.GetSelection() == SPT['TSK']:
                self.spn.SetSelection(SPT['TSK'])

#FIX, Scintilla REGEXP not efficient -> use 're.compile'
#INFO, URL=https://pythex.org
#INFO, URL=https://docs.python.org/2/library/re.html
#INFO, URL="D:\Dev\D\wx\TSN_SPyE\contrib\demo\demo_SearchSTC.py"
#NOTE, workaround TEMP: for now using Scintilla REGEXP syntax
        tsk = '^#[INTDF][NOOOI][FTDNX][OEOE,]'  # '|'.join(TSK_TAGS)
        flg = stc.STC_FIND_MATCHCASE | stc.STC_FIND_REGEXP

        if _id == MB['TSK_NXT']:
            if DEBUG['TASKS']: print('  next')
            cur += 1
            maxPos = doc.LastPosition
        elif _id == MB['TSK_PRV']:
            if DEBUG['TASKS']: print('  previous')
            cur -= 1
            maxPos = 0

        pos = doc.FindText(cur, maxPos, tsk, flags=flg)
        if pos == stc.STC_INVALID_POSITION:
            if cfg['Task']['SearchWrap']:
                if _id == MB['TSK_NXT']:
                    cur = 0
                    maxPos = doc.LastPosition
                    txt = 'TOP'
                elif _id == MB['TSK_PRV']:
                    cur = doc.LastPosition
                    maxPos = 0
                    txt = 'BOTTOM'
                pos = doc.FindText(cur, maxPos, tsk, flags=flg)
                if pos == stc.STC_INVALID_POSITION:
                    return
                else:
                    if DEBUG['TASKS']: print('  wrapped to %s' % txt)
            else:
                if DEBUG['TASKS']: print('  not found')
                return
        # print(len(tsk))
        doc.SetSelection(pos, pos + 5)  # task tag length
        doc.GotoPos(pos)
        if cfg['Task']['SearchCentreCaret']:
            doc.VerticalCentreCaret()

        # task list control
        tlc = doc.spt[SPT['TSK']].ctrl if doc.spt[SPT['TSK']] else None
        if tlc and cfg['Task']['SearchSyncPanel']:
            lin = doc.CurrentLine
            for idx in range(tlc.ItemCount):
                if lin == int(tlc.GetItemText(idx, 3)) - 1:  # lineno
                    tlc.Select(idx)
                    tlc.Focus(idx)
        _dbg_FOCUS(doc)

    def SearchGotoLine(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        lin = str(doc.LineFromPosition(doc.GetSelection()[0]) + 1)
        dlg = wx.TextEntryDialog(self, 'Enter number:', 'Go to line', lin)
        self._set_icon(dlg)
        ans = dlg.ShowModal()
        lin = int(dlg.Value) - 1
        dlg.Destroy()
        if ans == wx.ID_OK:
            doc.GotoLine(lin)
            doc.VerticalCentreCaret()

    def SearchCaretNext(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        doc.crt_bsy = True
        if doc.crt_idx < len(doc.crt_hst) - 1:
            doc.crt_idx += 1
            if DEBUG['PHIST']: _dbg_POSITION_HISTORY(doc)
            doc.GotoPos(doc.crt_hst[doc.crt_idx])
        else:
            self._push_statustext('Already at newest position')

    def SearchCaretPrev(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        doc.crt_bsy = True
        if doc.crt_idx != 0:
            doc.crt_idx -= 1 if doc.crt_idx != len(doc.crt_hst) else 2
            if DEBUG['PHIST']: _dbg_POSITION_HISTORY(doc)
            doc.GotoPos(doc.crt_hst[doc.crt_idx])
        else:
            self._push_statustext('Already at earliest position')

    def SearchBraceMatch(self, evt):
        _dbg_funcname(3)
#        if DEBUG['BRACE']: print('SearchBraceMatch: ', end='')
        if DEBUG['BRACE'] > 1: _dbg_EVENT(evt)
        if DEBUG['BRACE'] == 1: print()
        __, doc = self._getPagDoc()
        if not doc: return

        res = False
        cur = doc.CurrentPos
        prs = cfg['BraceMatch']['CharacterPairs']
        # check for brace
        if cur > 0 and chr(doc.GetCharAt(cur - 1)) in prs:  # left
            cur -= 1
        elif chr(doc.GetCharAt(cur)) not in prs:            # right
            cur = -1

        if cur >= 0:
            brc = doc.BraceMatch(cur)
            if brc != stc.STC_INVALID_POSITION:
#TODO, needs better coding...
                res = True
                tlb = 'ToolBar' in str(evt.EventObject)
                if evt.Id == MB['BRC'] or tlb:   # called from menu/Ctrl+M or toolbar
                    doc.GotoPos(brc)             # ...jump to matching brace
                elif evt.Id == MB['SEL_BRC']:    # called from menu/Ctrl+Shift+M
                    if cur > brc:                # ...create selection between braces
                        cur, brc = brc, cur
                    doc.SetSelection(cur + 1, brc)
                doc.BraceHighlight(cur, brc)  # turn ON
                doc.SetHighlightGuide(doc.GetColumn(cur))
            else:
                doc.BraceBadLight(cur)
                doc.SetHighlightGuide(0)
                self._push_statustext('No matching brace for [%s]' % doc.GetRange(cur, cur + 1))
#                 self._set_statustext('No matching brace for [%s]' % doc.GetRange(cur, cur + 1))
        else:
            doc.BraceHighlight(-1, -1)        # turn OFF
        evt.Skip()
        return res

    def LanguageSetStyling(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        # get language based on menu selection
        lang = [m for m in LANG if evt.Id == m[4]]
        doc._set_language_styling(lang)

    def FormatCase(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        _id = evt.Id
        txt = doc.SelectedText
        if len(txt):
            sel = doc.GetSelection()
            new = None
            if _id == MB['FMT_TTL']:
#INFO, URL=https://docs.python.org/2/library/stdtypes.html#str.title
                new = txt.title()
            elif _id == MB['FMT_UPR']:
                doc.UpperCase()
            elif _id == MB['FMT_LWR']:
                doc.LowerCase()
            elif _id == MB['FMT_INV']:
                new = ''.join(c.lower() if c.isupper() else c.upper() for c in txt)
            if new:
                doc.ReplaceSelection(new)
            doc.SetSelection(sel[0], sel[1])

    def FormatTimestamp(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        tim = dtm.now()
        doc.AddText(tim.strftime(cfg['Editor']['TimestampFormat']))
        self._push_statustext('Timestamp inserted')

    def FormatConvertEOLs(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        _id = evt.Id
        if _id == MB['FMT_CCL']:
            flg = stc.STC_EOL_CRLF
        elif _id == MB['FMT_CLF']:
            flg = stc.STC_EOL_LF
        elif _id == MB['FMT_CCR']:
            flg = stc.STC_EOL_CR
        doc.ConvertEOLs(flg)

    # copied from Editra, ed_stc.py
    def FormatRemoveTrailingWS(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        cpos = doc.CurrentPos
        cline = doc.CurrentLine
        cline_len = len(doc.GetLine(cline))
        epos = cline_len - (doc.GetLineEndPosition(cline) - cpos)
        _dbg_RMTWS('BEFORE:', cpos, cline, cline_len, epos, doc)

        # start removing trailing whitespace
        cnt = 0
        wx.BeginBusyCursor()
        doc.BeginUndoAction()
        for line in range(doc.LineCount):
            eol = ''
            txt = doc.GetLine(line)

            # Scintilla stores text in utf8 internally so we need to
            # encode to utf8 to get the correct length of the text.
            tlen = len(txt.encode('utf-8'))
            if tlen:
                if CRLF in txt:
                    eol = CRLF
                elif LF in txt:
                    eol = LF
                else:
                    eol = txt[-1]

                if not eol.isspace():
                    continue
                elif eol in ' \t':
                    eol = ''
            else:
                continue
            # strip whitespace from line
            end = doc.GetLineEndPosition(line) + len(eol)
            start = max(end - tlen, 0)
            doc.SetTargetStart(start)
            doc.SetTargetEnd(end)
            rtxt = txt.rstrip() + eol
            if rtxt != doc.GetTextRange(start, end):
                if DEBUG['RMTWS']: print('    %d:[%s]' % (line + 1, txt.__repr__()))
                doc.ReplaceTarget(rtxt)
                cnt += 1
                if DEBUG['RMTWS']: print('    %d:[%s]' % (line + 1, rtxt.__repr__()))
        doc.EndUndoAction()
        wx.EndBusyCursor()

        txt = 'Removed %d trailing space occurrences' % cnt if cnt else 'No trailing space found'
        self._push_statustext(txt)

        # restore caret position
        cline_len = len(doc.GetLine(cline))
        end = doc.GetLineEndPosition(cline)

        if epos >= cline_len:
            epos = end
        else:
            start = max(end - cline_len, 0)
            if DEBUG['RMTWS']: print(' ', end, cline_len, start)
            epos += start

        _dbg_RMTWS(' AFTER:', cpos, cline, cline_len, epos, doc)
        if epos != cpos and cline > 0:
            doc.GotoPos(epos)

    def MacroTEST(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        doc._macro_TEST(evt)

    def MacroStart(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        doc._macro_start(evt)

    def MacroStop(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        doc._macro_stop(evt)

    def MacroPlay(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        # at least play once
        cnt = 1
#DONE, Play Multiple Times Dialog
        if evt.Id == MB['MAC_PLM']:
            dlg = wx.TextEntryDialog(self, 'Enter count:', 'Play macro multiple times', '1')
            self._set_icon(dlg)
            ans = dlg.ShowModal()
            cnt = int(dlg.Value)
            dlg.Destroy()
            if ans == wx.ID_CANCEL:
                return

        wx.BeginBusyCursor()
        # doc.BeginUndoAction()
        for i in range(cnt):
            doc._macro_play(evt)
        # doc.EndUndoAction()
        wx.EndBusyCursor()

        if cnt > 1:
            self._push_statustext('Macro executed %s times' % (cnt))

#TODO, integrate with macro load file and play/execution...
############################################################
# Example ipython output:
##########
# In [1]: with open('_todo.txt', 'r') as myfile:
#    ...:     data=myfile.read()
#
# In [2]: print(data)
# ruler (sizing/offset):
#         - sync cursor
#         - check stc fontsize, does not change w/ stc zoom level!
#         - check stc zoom level =>> ranges from -10 to +20 (0=default)
#         - position below tab bar instead of above
# calltip:
#         - bug
#         - CallTipSetForegroundHighlight
# menu:
#         - menu item with multiple shortcuts (AcceleratorTable, AcceleratorEntry)
#           https://www.google.nl/search?q=wxpython+"multiple+shortcuts"+"menu+item"
#
# In [3]: for lin in data.splitlines():
#    ...:     print lin
# ruler (sizing/offset):
#         - sync cursor
#         - check stc fontsize, does not change w/ stc zoom level!
#         - check stc zoom level =>> ranges from -10 to +20 (0=default)
#         - position below tab bar instead of above
# calltip:
#         - bug
#         - CallTipSetForegroundHighlight
# menu:
#         - menu item with multiple shortcuts (AcceleratorTable, AcceleratorEntry)
#           https://www.google.nl/search?q=wxpython+"multiple+shortcuts"+"menu+item"
############################################################

    def MacroEdit(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        print(doc._macro_to_source())

#INFO, URL=http://wxpython-users.1045709.n5.nabble.com/Hide-Remove-a-Toolbar-td2316942.html
    def LayoutToolBar(self, evt):
        _dbg_funcname()
        self.tb.Show(evt.IsChecked())
#NOTE, 2017-07-07 07:06:34, also solved for statusbar
        self.SendSizeEvent()

    # def LayoutMenuBar(self, evt):
    #     _dbg_funcname()
    #     self.mb.Show(evt.IsChecked())
    #     # self.SetMenuBar(None)
    #     self.SendSizeEvent()

    def LayoutStatusBar(self, evt):
        _dbg_funcname()
        self.sb.Show(evt.IsChecked())
        self.SendSizeEvent()

    def LayoutSearchPanel(self, evt):
        _dbg_funcname()
        if DEBUG['SASH']: print('   IN: swap =', self.schsp.swap)
        self.schsp.swap = False
        if self.schsp.IsSplit():
            self.mb.Check(MB['LAY_SCH'], False)
            self.schsp.Unsplit(self.schbotPanel)
        else:
            self.mb.Check(MB['LAY_SCH'], True)
            self.schsp.SplitHorizontally(self.schtopPanel, self.schbotPanel, -SASH['SCH'][self.sch.mode])
        if DEBUG['SASH']: print('  OUT: swap =', self.schsp.swap)

    def LayoutSearchPanelSwap(self, evt):
        _dbg_funcname()
        if DEBUG['SASH']: print('   IN: swap =', self.schsp.swap)
        if self.schsp.IsSplit():
#NOTE, ruler size can not change so keep sash position at SASH['SCH'][self.sch.mode]
            # pos = self.schsp.SashPosition
            # if DEBUG['SASH']: print('   IN:  pos =', pos)
            self.schsp.Unsplit(self.schbotPanel)
            if self.schsp.swap:
                self.schsp.SplitHorizontally(self.schtopPanel, self.schbotPanel, -SASH['SCH'][self.sch.mode])
            else:
                self.schsp.SplitHorizontally(self.schbotPanel, self.schtopPanel, SASH['SCH'][self.sch.mode])
            # if DEBUG['SASH']: print('  OUT:  pos =', pos)
            self.schsp.swap = not self.schsp.swap
        if DEBUG['SASH']: print('  OUT: swap =', self.schsp.swap)

    def LayoutRuler(self, evt):
        _dbg_funcname()
        if DEBUG['SASH']: print('   IN: swap =', self.midsp.swap)
        self.midsp.swap = False
        if self.midsp.IsSplit():
            self.mb.Check(MB['LAY_RLR'], False)
            self.midsp.Unsplit(self.midtopPanel)
        else:
            self.mb.Check(MB['LAY_RLR'], True)
            self.midsp.SplitHorizontally(self.midtopPanel, self.midbotPanel, SASH['MID'])
        if DEBUG['SASH']: print('  OUT: swap =', self.midsp.swap)

    def LayoutRulerSwap(self, evt):
        _dbg_funcname()
        if DEBUG['SASH']: print('   IN: swap =', self.midsp.swap)
        if self.midsp.IsSplit():
#NOTE, ruler size can not change so keep sash position at SASH['MID']
            # pos = self.midsp.SashPosition
            # if DEBUG['SASH']: print('   IN:  pos =', pos)
            self.midsp.Unsplit(self.midbotPanel)
            if self.midsp.swap:
                self.midsp.SplitHorizontally(self.midtopPanel, self.midbotPanel, SASH['MID'])
            else:
                self.midsp.SplitHorizontally(self.midbotPanel, self.midtopPanel, -SASH['MID'])
            # if DEBUG['SASH']: print('  OUT:  pos =', pos)
            self.midsp.swap = not self.midsp.swap
        if DEBUG['SASH']: print('  OUT: swap =', self.midsp.swap)

    def LayoutSidePanel(self, evt):
        _dbg_funcname()
        if DEBUG['SASH']: print('   IN: swap =', self.versp.swap)
        self.versp.swap = False
        if self.versp.IsSplit():
            self.mb.Check(MB['LAY_SPN'], False)
            self.versp.Unsplit(self.rightPanel)
        else:
            self.mb.Check(MB['LAY_SPN'], True)
            self.versp.SplitVertically(self.leftPanel, self.rightPanel, -SASH['VER'])
        if DEBUG['SASH']: print('  OUT: swap =', self.versp.swap)

    def LayoutSidePanelSwap(self, evt):
        _dbg_funcname()
        if DEBUG['SASH']: print('   IN: swap =', self.versp.swap)
        if self.versp.IsSplit():
            pos = self.versp.SashPosition
            if DEBUG['SASH']: print('   IN:  pos =', pos)
            self.versp.Unsplit(self.rightPanel)
            if self.versp.swap:
                self.versp.SplitVertically(self.leftPanel, self.rightPanel, -pos)
            else:
                self.versp.SplitVertically(self.rightPanel, self.leftPanel, -pos)
            if DEBUG['SASH']: print('  OUT:  pos =', pos)
            self.versp.swap = not self.versp.swap
        if DEBUG['SASH']: print('  OUT: swap =', self.versp.swap)

    def LayoutCodeContext(self, evt):
        _dbg_funcname()
        if DEBUG['SASH']: print('   IN: swap =', self.horsp.swap)
        self.horsp.swap = False
        if self.horsp.IsSplit():
            self.mb.Check(MB['LAY_CCX'], False)
            self.horsp.Unsplit(self.topPanel)
        else:
            self.mb.Check(MB['LAY_CCX'], True)
            self.horsp.SplitHorizontally(self.topPanel, self.bottomPanel, SASH['HOR'])
        if DEBUG['SASH']: print('  OUT: swap =', self.horsp.swap)

    def LayoutCodeContextSwap(self, evt):
        _dbg_funcname()
        if DEBUG['SASH']: print('   IN: swap =', self.horsp.swap)
        if self.horsp.IsSplit():
            pos = self.horsp.SashPosition
            if DEBUG['SASH']: print('   IN:  pos =', pos)
            self.horsp.Unsplit(self.topPanel)
            if self.horsp.swap:
                self.horsp.SplitHorizontally(self.topPanel, self.bottomPanel, -pos)
            else:
                self.horsp.SplitHorizontally(self.bottomPanel, self.topPanel, -pos)
            if DEBUG['SASH']: print('  OUT:  pos =', pos)
            self.horsp.swap = not self.horsp.swap
        if DEBUG['SASH']: print('  OUT: swap =', self.horsp.swap)

    def LayoutFileTabs(self, evt):
        _dbg_funcname()
        self.mb.Check(MB['LAY_FTB'], evt.IsChecked())
        self.nb.SetTabCtrlHeight(0 if self.nb.TabCtrlHeight else -1)

    def LayoutFileTabIcons(self, evt):
        _dbg_funcname()
        self.mb.Check(MB['LAY_FTI'], evt.IsChecked())
        for i in range(self.nb.PageCount):
            ico = self._get_file_icon(self.nb.GetPage(i).langtype)
            self.nb.SetPageBitmap(i, ico if evt.IsChecked() else wx.NullBitmap)

    def LayoutToolTips(self, evt):
        _dbg_funcname()
        self.mb.Check(MB['LAY_TTP'], evt.IsChecked())

#TODO, process NOT just TOOLBAR tooltips, ALSO:
#TODO, - NOTEBOOK page tab tooltips
#TODO, - SPLITTER, STATUSBAR, DOCUMENTMAP
#TODO, - TOPLINETOOLTIP
#         sty = self.tb.WindowStyle
# #         if self.mb.IsChecked(MB['LAY_TTP']):
#         if sty & wx.TB_NO_TOOLTIPS:
#             self.mb.Check(MB['LAY_TTP'], True)
#             self.tb.SetWindowStyle(sty & ~wx.TB_NO_TOOLTIPS)  # & ~wx.TB_TEXT
# #             wx.ToolTip.Enable(True)
# #             self.nb.tlt.Enable(True)
#         else:
#             self.mb.Check(MB['LAY_TTP'], False)
#             self.tb.SetWindowStyle(sty | wx.TB_NO_TOOLTIPS)   # |  wx.TB_TEXT
# #             wx.ToolTip.Enable(False)
# #             self.nb.tlt.Enable(False)

    def LayoutTopLineToolTip(self, evt):
        _dbg_funcname()
        self.mb.Check(MB['LAY_TLT'], evt.IsChecked())
#FIX, does not globally enable/disable
        self.nb.tlt.EnableTip(True if self.mb.IsChecked(MB['LAY_TLT']) else False)

    def LayoutMenuIcons(self, evt):
        _dbg_funcname()
        self.icons = not self.icons
        RebuildMainMenu(self, recent_list, self.icons, self.hlp)

    def LayoutMenuHelpText(self, evt):
        _dbg_funcname()
        # self.mb.Check(MB['LAY_MNH'], evt.IsChecked())
        self.hlp = not self.hlp
        RebuildMainMenu(self, recent_list, self.icons, self.hlp)

    def LayoutDistractionFree(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        # enable/disable 'fullscreen'
        self.mb.Enable(MB['LAY_FUL'], False if not self.IsFullScreen() else True)
        flg = wx.FULLSCREEN_ALL
        self.Freeze()
#DONE, hide/show file tabs
        if not self.IsFullScreen():
            self.nb.SetTabCtrlHeight(0)
        else:
            self.nb.SetTabCtrlHeight(-1 if self.mb.IsChecked(MB['LAY_FTB']) else 0)
#FIX, menu and shortcuts NOT accessible, use accelerator table
        # self.mb.Check(MB['LAY_DFM'], self.mb.IsChecked(MB['LAY_DFM']))
        self.ShowFullScreen(not self.IsFullScreen(), flg)
        doc.SetUseHorizontalScrollBar(False if self.IsFullScreen() else cfg['Editor']['HorizontalScrollBar'])
        doc.SetUseVerticalScrollBar(False if self.IsFullScreen() else cfg['Editor']['VerticalScrollBar'])
        # unsplit/split side panel to force default sash position
#TODO, needs better coding...
        self.Maximize(None)
        # if self.versp.IsSplit():
        #     self.LayoutSidePanel(evt)
        #     self.LayoutSidePanel(evt)
        self.Thaw()

    def LayoutFullScreen(self, evt):
        _dbg_funcname()
        # enable/disable 'distraction free mode'
        self.mb.Enable(MB['LAY_DFM'], False if not self.IsFullScreen() else True)
        flg = 0
#NOTE, default: no flags = wx.FULLSCREEN_ALL
#         flg |= wx.FULLSCREEN_ALL
        flg |= wx.FULLSCREEN_NOBORDER
        flg |= wx.FULLSCREEN_NOCAPTION
#         flg |= wx.FULLSCREEN_NOMENUBAR
        flg |= wx.FULLSCREEN_NOTOOLBAR
#         flg |= wx.FULLSCREEN_NOSTATUSBAR
#TODO, fullscreen with staticbox/label: '...F12 to return'
#         if not self.IsFullScreen():
#             self.sizer = wx.StaticBoxSizer(wx.StaticBox(self, label=' Full Screen (F12 to return) '))
#             self.SetSizer(self.sizer)
#             self.Layout()
#         else:
#             del self.sizer
        self.Freeze()
        self.mb.Check(MB['LAY_FUL'], self.mb.IsChecked(MB['LAY_FUL']))
        self.ShowFullScreen(not self.IsFullScreen(), flg)
        # unsplit/split side panel to force default sash position
#TODO, needs better coding...
        self.Maximize(None)
        # if self.versp.IsSplit():
        #     self.LayoutSidePanel(evt)
        #     self.LayoutSidePanel(evt)
        self.Thaw()

#FIX, review and test colour change
        # bg = self.sb.BackgroundColour
        if self.IsFullScreen():
            self.sb.SetBackgroundColour(cfg['Statusbar']['FullScreenBackColour'])
            self._push_statustext('Full Screen (F12 to return)')
        else:
            self.sb.SetBackgroundColour(cfg['Statusbar']['BackColour'])

    def LayoutPreferences(self, evt):
        _dbg_funcname()
        dlg = Preferences(self)
#TODO, handle buttons inside or outside 'Preferences' class?
        ans = dlg.ShowModal()

    def LayoutSyntaxStyling(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        dlg = SyntaxStyling(self, doc)
        self._set_icon(dlg)
        ans = dlg.ShowModal()

    def LayoutShortcutEditor(self, evt):
        _dbg_funcname()
#FIX, search filter not working
        dlg = SCE.ShortcutEditor(self)
        dlg.FromMenuBar(self)
        ans = dlg.ShowModal()
        if ans == wx.ID_OK:
            # changes accepted, send new shortcuts back to TLW wx.MenuBar
            dlg.ToMenuBar(self)
        dlg.Destroy()

    def HelpContents(self, evt):
        _dbg_funcname()
        txt = appName + ' Help Contents\n'
        msg1 = txt + '\nNot implemented, yet.'
        ans = self._msg_box(self, 'HELP', msg1)
        if cfg['General']['Oeuf']:
            msg2 = txt + '\nSorry, not implemented, yet.\n\nWill you accept my apologies?'
            msg3 = txt + '\nSorry, I\'m so sorry.\n\nI just said: "Sorry, not implemented, yet."\n\nWill you please accept..?'
            msg4 = txt + '\nGreatly admiring your humongous persistence, though.\n\nI\'ll be quitting this monologue, too.\n\nSo silly.\n\nAnd sorry..\n\nPS Sorry for my humble advice: get some help, yet.'
            if ans == wx.ID_HELP:
                ans = self._msg_box(self, 'WARN_ASK', msg2)
                if ans == wx.ID_NO:
                    ans = self._msg_box(self, 'WARN_ASK', msg3)
                    if ans == wx.ID_NO:
                        ans = self._msg_box(self, 'ERROR', msg4)

    def HelpCheckUpdates(self, evt):
        _dbg_funcname()
        msg = appName + ' is up to date.\n\n'
        ans = self._msg_box(self, 'INFO', msg)

    def HelpInspectionTool(self, evt):
        _dbg_funcname()
        wx.lib.inspection.InspectionTool().Show(selectObj=self, refreshTree=True)

    def HelpAbout(self, evt):
        _dbg_funcname()
        if cfg['General']['Oeuf']:
            bmp = Oeuf(self.versp)
            bmp.Show(True)
        app.Splash(self.versp)

    def SystemTrayRestoreWindow(self, evt):
        self.Iconize(False if self.IsIconized() else True)
        if not self.IsShown():
            self.Show(True)
        self.Raise()


################################################################################################


#TODO, move 'CtxToolbar', 'CtxStatusbar', 'CtxDocumentMap' to 'gui.py'


    def CtxToolbar(self, evt):
        _dbg_funcname()
        _id = evt.Id
#TODO, needs better coding...
        lbl = [t for t in self.ctx['TBR'] if t != MB['SEP'] and len(t) > 4 and t[6] == _id][0][0]
        if DEBUG['TLBAR']: print('  label = [%s]' % lbl)

        # sty = self.tb.WindowStyle

        # # toggle check mark
        # for key in TBX.keys():
        #     if _id == TBX[key][0]:
        #         TBX[key][1] = not TBX[key][1]

        # # prepare toolbar: style, font, bitmap size
        # sty  = 0                 if TBX['ICO_SHW'][1] else wx.TB_NOICONS
        # sty += wx.TB_TEXT        if TBX['TXT_SHW'][1] else 0
        # bms  = 24                if TBX['ICO_LRG'][1] else 16
        # sfx  = '_24'             if TBX['ICO_LRG'][1] else ''
        # pts  = 9                 if TBX['TXT_LRG'][1] else 7
        # sty += wx.TB_HORZ_LAYOUT if TBX['ALN_HOR'][1] else 0

        # self.tb.SetWindowStyle(sty)
        # self.tb.SetOwnFont(wx.Font(wx.FontInfo(pts)))
        # self.tb.SetToolBitmapSize((bms, bms))
        # for tbt_id, nam in TB['ALL'].items():
        #     self.tb.SetToolNormalBitmap(tbt_id, PNG[nam + sfx].Bitmap)

        # self.tb.Realize()

        sty = self.tb.WindowStyle

        _dbg_CTXTTB('B', TBX, cfg)
        # update toolbar context menu check marks
        for key in TBX.keys():
            if _id == TBX[key][0]:
                TBX[key][1] = not TBX[key][1]

        # update them in config, too
        cfg['Toolbar']['ShowIcons'] = TBX['ICO_SHW'][1]
        cfg['Toolbar']['ShowText'] = TBX['TXT_SHW'][1]
        cfg['Toolbar']['LargeIcons'] = TBX['ICO_LRG'][1]
        cfg['Toolbar']['LargeText'] = TBX['TXT_LRG'][1]
        cfg['Toolbar']['AlignHorizontally'] = TBX['ALN_HOR'][1]
        _dbg_CTXTTB('A', TBX, cfg)

        # prepare toolbar: style, font, bitmap size
        if _id == TBX['ICO_SHW'][0]:
            self.tb.SetWindowStyle(sty ^ wx.TB_NOICONS)
        elif _id == TBX['TXT_SHW'][0]:
            self.tb.SetWindowStyle(sty ^ wx.TB_TEXT)
            self.tb.SetOwnFont(wx.Font(wx.FontInfo(9 if self.tb.Font.PointSize == 7 else 7)))
        elif _id == TBX['ICO_LRG'][0]:
            self.tb.SetToolBitmapSize((24, 24) if TBX['ICO_LRG'][1] else (16, 16))
            sfx = '_24' if TBX['ICO_LRG'][1] else ''  # suffix
            for tbt_id, nam in TB['ALL'].items():
                self.tb.SetToolNormalBitmap(tbt_id, PNG[nam + sfx].Bitmap)
        elif _id == TBX['TXT_LRG'][0]:
            self.tb.SetOwnFont(wx.Font(wx.FontInfo(9 if self.tb.Font.PointSize == 7 else 7)))
        elif _id == TBX['ALN_HOR'][0]:
#TODO, close but not a cigar yet...
            if TBX['ICO_SHW'][1] and TBX['TXT_SHW'][1]:
                self.tb.SetWindowStyle(sty ^ wx.TB_HORZ_LAYOUT)

        self.tb.Realize()

################################################################################################

    def CtxStatusbar(self, evt):
#FIX: show/hide statusbar fields
        _dbg_funcname()
        _id = evt.Id
#TODO, needs better coding...
        lbl = [t for t in self.ctx['SBR'] if t != MB['SEP'] and len(t) > 4 and t[6] == _id][0][0]
        if DEBUG['STBAR']: print('  label = [%s]' % lbl)

        # sbx = sorted(SBX.items(), key=lambda elem: elem[1])
        # print(sbx)

        # update statusbar context menu check marks
#DONE, use 'SBX.keys()' in list comprehension: all but 'ALL'...
        _all = [key for key in SBX.keys() if key != 'ALL']
        if _id == SBX['ALL'][1]:
            SBX['ALL'][2] = not SBX['ALL'][2]
            for key in _all:
                SBX[key][2] = True if SBX['ALL'][2] else False
        else:
            for key in _all:
                if _id == SBX[key][1]:
                    if DEBUG['STBAR']: print('   [%s] -> clicked' % (key))
                    SBX[key][2] = not SBX[key][2]
                    SBX['ALL'][2] = all([SBX[key][2] for key in _all])
                # else:
                #     if DEBUG['STBAR']: print('    %s' % (key))

################################################################################################

        sbf = sorted(SBF_CPY.items(), key=lambda elem: elem[1])  # 'sbf' is a list!
        wid = [w[1][1] for w in sbf if w[0] != 'MSG' and SBX[w[0]][2]]
        sty = [s[1][2] for s in sbf if s[0] != 'MSG' and SBX[s[0]][2]]
        cnt = len(wid)

        # print(cnt, wid, sty)
        # print(type(cnt), type(wid), type(sty))

        # rebuild statusbar fields
        for key in sbf:
            if key[0] != 'MSG':
                del SBF[key[0]]
        cnt = 0
        for key in sbf:
            if key[0] != 'MSG' and SBX[key[0]][2]:
                print(key[0], SBX[key[0]][2])
                SBF[key[0]] = (cnt + 1, wid[cnt], sty[cnt])
                cnt += 1
        # pprint(SBF)

        # self.sb.SetFieldsCount(cnt)
        # self.sb.SetStatusWidths(wid)
        # self.sb.SetStatusStyles(sty)

#FIX, ...
        # self.sb = SetupStatusBar(self)
        # self.SetStatusBar(self.sb)

################################################################################################


    def CtxDocumentMap(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        _id = evt.Id if evt else None
#TODO, needs better coding...
        lbl = [t for t in self.ctx['DCM'] if t != MB['SEP'] and len(t) > 4 and t[6] == _id][0][0]
        if DEBUG['DCMAP']: print('  label = [%s]' % lbl)

        # update document map context menu check marks
        for key in DMX.keys():
            if _id == DMX[key][0]:
                DMX[key][1] = not DMX[key][1]

        # update them in config, too
        cfg['DocumentMap']['ZoneRectRounded'] = DMX['ZRC_RND'][1]
        cfg['DocumentMap']['ZoneCentreLine'] = DMX['ZCT_LIN'][1]
        cfg['DocumentMap']['ZoneCentreDot'] = DMX['ZCT_DOT'][1]
        cfg['DocumentMap']['EdgeTextIndicator'] = DMX['EDG_TXT'][1]
        cfg['DocumentMap']['AutoFocus'] = DMX['AUT_FCS'][1]
        cfg['DocumentMap']['MarkerLineHighlight'] = DMX['MRK_LHL'][1]

#FIX, update 'MarkerLineHighlight' in 'DocumentMap._draw_view_zone'
#FIX, - now it's set - only once - in 'DocumentMap.__init__'
#TODO, create method for 'update document map panel/control'
        # update document map panel/control
        dcp = doc.spt[SPT['DCM']]
        if dcp:
            dcp.Refresh()  # force 'preview doc' update
            dcp._draw_view_zone(None)
            dcm = dcp.ctrl
            dcm.SetMarginWidth(MGN['SYM'], 0 if DMX['MRK_LHL'][1] else 1)

        # print('ZoneRectRounded     =', DMX['ZRC_RND'][0])
        # print('ZoneCentreLine      =', DMX['ZCT_LIN'][0])
        # print('ZoneCentreDot       =', DMX['ZCT_DOT'][0])
        # print('EdgeTextIndicator   =', DMX['EDG_TXT'][0])
        # print('AutoFocus           =', DMX['AUT_FCS'][0])
        # print('MarkerLineHighlight =', DMX['MRK_LHL'][0])
        # print('--------------------------------')
        # print(_id, opt)
        # opt = not opt
        # print(_id, opt)

################################################################################################


    def SplitEditor(self, evt):
#FIX, SPLIT_EDITOR
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        self._not_implemented(None, 'SPLIT EDITOR')
#
#   #         self.edtsp.ReplaceWindow(doc, doc)
#
#           print('doc           =', doc)
#           print('doc.parent    =', doc.parent)
#           print('edtsp         =', self.edtsp)
#           print('edtsp.Window1 =', self.edtsp.Window1)
#           print('edtsp.Window2 =', self.edtsp.Window2)
#
#           self.edtsp.SplitVertically(doc, doc, SASH['EDT'])
#   #         self.edtsp.Unsplit(doc)

    def CtxTEST(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        doc.CtxTEST(evt)

    def CtxTEST2(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        doc.CtxTEST2(evt)

    def CtxTextSplit(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        doc.CtxTextSplit(evt)

    def CtxTextJoin(self, evt):
        _dbg_funcname()
        __, doc = self._getPagDoc()
        if not doc: return
        doc.CtxTextJoin(evt)

    def _detect_file_change(self, delay=DELAY['DFC']):
        _dbg_funcname(2)
        if DEBUG['DFCHG']: print('_detect_file_change:')
#         return

        self.Freeze()  # avoid flicker
        win = self.FindFocus()  # save current focus
        cur = self.nb.GetPageIndex(self.nb.CurrentPage)  # save current page
        for idx in range(self.nb.PageCount):
            doc = self.nb.GetPage(idx)
            if not doc: continue
            # skip new/unsaved file
            if not doc.dirname:
                continue
            # disk and edit buffer modification times
            if not os.path.exists(doc.pathname):
                if not doc.detect_del:
                    doc.detect_del = True
                    msg = doc.filename + ' deleted from disk'
                    ans = self._msg_box(self, 'INFO', msg)
            elif not doc.detect_chg:
                cur_mod = os.path.getmtime(doc.pathname)
                if cur_mod != doc.date_mod:
                    doc.detect_chg = True
                    msg = doc.filename + ' timestamps differ:\n\n'
                    msg += '%s => on Disk\n' % dtm.fromtimestamp(cur_mod).strftime(TIM_FMT)
                    msg += '%s => in Editor\n' % dtm.fromtimestamp(doc.date_mod).strftime(TIM_FMT)
                    ans = self._msg_box(self, 'INFO', msg)

#FIX, focus changes to doc when it is elsewhere, e.g. sidepanel
        # _dbg_FOCUS(win)  # restore current focus
        self.nb.SetSelection(cur)  # restore current page
        __, doc = self._getPagDoc()
        # 1st call at startup: doc = None
        if doc:
            _dbg_FOCUS(doc)
        if DEBUG['DFCHG'] > 1: print('  back in %d ms' % delay)
        # call myself frequently
        wx.CallLater(delay, self._detect_file_change, delay)
        self.Thaw()

    @staticmethod
    def _get_file_icon(langtype):
        _dbg_funcname(2)
        if DEBUG['BASIC']: print('_get_file_icon:')
        try:
            ico = PNG['ext_' + langtype].Bitmap
        except KeyError:
            ico = wx.NullBitmap
        return ico

    def _getPagDoc(self, clicked_tab=-1):
        _dbg_funcname(3)
        if DEBUG['BASIC'] > 1: print('_getPagDoc:')
        # get active or clicked notebook tab
        pag = self.nb.Selection if clicked_tab < 0 else clicked_tab
        if pag >= 0:
            return pag, self.nb.GetPage(pag)
#DONE, 'TypeError: 'NoneType' object is not iterable' when no document open
        else:
            return -1, None

    def _msg_box(self, parent, typ='INFO', msg='', extra=''):
        _dbg_funcname()
        # style and caption
        if typ == 'HELP':
            sty = wx.HELP  # | wx.ICON_NONE
            cap = appName + ' Help'
        elif typ == 'INFO':
            sty = wx.OK | wx.ICON_INFORMATION
            cap = 'Information'
        elif typ == 'WARN':
            sty = wx.OK | wx.ICON_EXCLAMATION
            cap = 'Warning'
        elif typ == 'ERROR':
#             adv.Sound.PlaySound('C:\Windows\Media\Windows Exclamation.wav')
            sty = wx.OK | wx.ICON_ERROR
            cap = 'Error'
        elif typ == 'WARN_ASK':
            sty = wx.YES_NO | wx.CANCEL | wx.CANCEL_DEFAULT | wx.ICON_EXCLAMATION
            cap = 'Warning'
        else:
            err = '_msg_box: Unknown type [%s]' % (typ)
            raise AssertionError(err)
        # append text to caption
        if extra:
            cap += ' (%s)' % extra
        dlg = wx.MessageDialog(parent, msg, cap, style=sty)
#FIX, icon not shown
        self._set_icon(dlg)
        ans = dlg.ShowModal()
        dlg.Destroy()
        return ans

    def _not_implemented(self, evt, txt=None):
        _dbg_funcname(2)
        if evt:
            obj = evt.EventObject
            txt = obj.GetLabel(evt.Id)
        if DEBUG['NOIMP']: print('NOIMP: [%s]' % txt)
        txt = '[%s] => NOT implemented' % txt
        bg = self.sb.BackgroundColour
        self.sb.SetBackgroundColour(cfg['Statusbar']['ErrorBackColour'])
        self._push_statustext(txt)
        self.sb.SetBackgroundColour(bg)

    def _open_files(self, filelist):
        _dbg_funcname(2)
        if DEBUG['BASIC']: print('_open_files:')
        if not filelist:
            return
        # self.Freeze()  # avoid flicker
        Freeze(self, '_open_files')  # avoid flicker
        for pnm, vis, pos, lin, col, lng, wrp, eol, wsp, sel_lst, bmk_lst in filelist:
            if DEBUG['FILE']: print('  OK:[%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s]' %
                                    (pnm, vis, pos, lin, col, lng, wrp, eol, wsp, sel_lst, bmk_lst))

            if not os.path.isfile(pnm):
                if DEBUG['FILE']: print('    File NOT found: skipping [%s]' % (pnm))
                continue

#DONE, focus on page tab if that file is already open => needs 'doc registry'
            # check if file already open
            skip = False
            for i in range(self.nb.PageCount):
                doc = self.nb.GetPage(i)
                if pnm == doc.pathname:
                    _dbg_FOCUS(doc)
                    skip = True
                    break
            if skip:
                continue

            dnm, fnm, fbs, ext = self._split_path(pnm)
#FIX, SPLIT_EDITOR
#             # vertical (editor/2nd view)
#             self.edtsp = EdtSplitter(self.nb)
#             doc = Editor(self.edtsp, [dnm, fnm, fbs, ext])
            doc = Editor(self.nb, [dnm, fnm, fbs, ext])
            res = doc.LoadFile(pnm)
#FIX, enable full doc search
            # enable full doc search
            doc.SetTargetStart(0)
            doc.SetTargetEnd(doc.LastPosition)

            # restore caret's last position
            if int(pos):
                doc.GotoPos(int(pos))
                doc.SetFirstVisibleLine(int(vis) - 1)

            # get language based on file extension
            lang = [e for e in LANG if ext in e[3].split('|')]

            # restore language
            if DEBUG['CONF']: print('%2s*** LANG:INIT = [%s]' % ('', lang))
            if lng and lang and lng not in lang[0]:
                if DEBUG['CONF']: print('%11sCONF = [%s]' % ('', lng))
                # get language based on langtype
                lang = [t for t in LANG if lng == t[1]]
            if DEBUG['CONF']: print('%11sEXIT = [%s]' % ('', lang))
            doc._set_language_styling(lang)
            self._update_page_tabs(doc, newtab=True)

            # restore word wrap
            if DEBUG['CONF']: print('%2s*** WRAP:INIT =       i[%d]' % ('', doc.WrapMode))
            if int(wrp):
                if DEBUG['CONF']: print('%11sCONF = s[%s], i[%d]' % ('', wrp, doc.WrapMode))
                doc.SetWrapMode(int(wrp))  # stc.STC_WRAP_WORD
                self.mb.Check(MB['DOC_WRP'], True)
            if DEBUG['CONF']: print('%11sEXIT =       i[%d]\n' % ('', doc.WrapMode))

            # restore EOL view
            if int(eol):
                doc.SetViewEOL(int(eol))
                self.mb.Check(MB['DOC_EOL'], True)

            # restore whitespace view
            if int(wsp):
                doc.SetViewWhiteSpace(int(wsp))
                self.mb.Check(MB['DOC_WSP'], True)

            # restore margins
            val = cfg['Margin']['LineNumber']
            self.mb.Check(MB['MGN_NUM'], val)
            doc.SetMarginWidth(MGN['NUM'], 0 if not val else cfg['Margin']['LineNumberWidth'])

            val = cfg['Margin']['Symbol']
            self.mb.Check(MB['MGN_SYM'], val)
            doc.SetMarginWidth(MGN['SYM'], 0 if not val else cfg['Margin']['SymbolWidth'])

            val = cfg['Margin']['Folding']
            self.mb.Check(MB['MGN_FOL'], val)
            doc.SetMarginWidth(MGN['FOL'], 0 if not val else cfg['Margin']['FoldingWidth'])

            self._update_margins()

            # restore edge
            val = cfg['Edge']['Mode']
            if val == stc.STC_EDGE_NONE:
                self.mb.Check(MB['EDG_NON'], val)
            elif val == stc.STC_EDGE_BACKGROUND:
                self.mb.Check(MB['EDG_BCK'], val)
            elif val == stc.STC_EDGE_LINE:
                self.mb.Check(MB['EDG_LIN'], val)
            # elif val == 3:
            # # elif val == stc.STC_EDGE_MULTILINE:
            #     self.mb.Check(MB['EDG_MUL'], val)
            doc.SetEdgeMode(val)
            doc.SetEdgeColumn(cfg['Edge']['Column'])
            doc.SetEdgeColour(cfg['Edge']['Colour'])

#TODO, add fold_style to 3 docstate methods, FOR NOW it is GLOBAL
#             # restore folding style
#             if int(fst) > -1:
#                 doc.fold_style = fst

            # restore selection
            if sel_lst and sel_lst[0] != sel_lst[1]:
                doc.SetSelection(sel_lst[0], sel_lst[1])

            # restore bookmarks
            if bmk_lst:
                doc._set_bookmarks(bmk_lst)
            _dbg_BOOKMARK('INIT', doc, bmk_lst)

#NOTE, workaround: bring selected page tab into view
        if self.nb.PageCount:  # when document open
            doc.nb.AdvanceSelection(False)
            doc.nb.AdvanceSelection(True)
            _dbg_FOCUS(doc)
        # self.Thaw()
        Thaw(self, '_open_files')

    def _set_statustext(self, msg, fld='MSG'):
        _dbg_funcname(2)
        msg = msg if fld == 'MSG' or SBX[fld][2] else ''
        if fld == 'MSG' or SBX[fld][2]:
            self.SetStatusText(msg, SBF[fld][0])

    def _push_statustext(self, msg, fld='MSG'):
        _dbg_funcname(2)
        msg = msg if fld == 'MSG' or SBX[fld][2] else ''
        self.PushStatusText(msg, SBF[fld][0])
        self.tmr_pop = wx.CallLater(cfg['Statusbar']['DelayHideMsg'], self._pop_statustext, fld)

    def _pop_statustext(self, fld):  # (self, fld, *args, **kwargs)
        _dbg_funcname(2)
#         print('CallLater called with args=%s, kwargs=%s\n' % (args, kwargs))
        self.sb.PopStatusText(SBF[fld][0])
#NOTE, workaround: 'AttributeError: 'MainWindow' object has no attribute 'tmr_pop''
        if hasattr(self, 'tmr_pop'):
            self.tmr_pop.Stop()
            del self.tmr_pop

    @staticmethod
    def _set_icon(parent, ico=None):
        _dbg_funcname()
        if DEBUG['BASIC']: print('_set_icon:')
        if not ico:
            ico = appIcon.Icon
        parent.SetIcon(ico)
        parent.SetBackgroundColour(cfg['General']['DialogBackColour'])

    @staticmethod
    def _split_path(path):
        _dbg_funcname(2)
        if DEBUG['BASIC']: print('_split_path:')
        dnm = os.path.dirname(path)
        fnm = os.path.basename(path)
        fbs = os.path.splitext(fnm)[0]
        ext = os.path.splitext(fnm)[1][1:].lower()
        if DEBUG['FILE'] > 1: print('  [%s]\n  [%s]\n  [%s]\n  [%s]' % (dnm, fnm, fbs, ext))
        return dnm, fnm, fbs, ext

    def _update_margins(self):
        _dbg_funcname(2)
        __, doc = self._getPagDoc()
        if not doc: return
        """will doxygen detect this docstring?"""
        all = [MB['MGN_NUM'], MB['MGN_SYM'], MB['MGN_FOL']]
        self.mb.Check(MB['MGN_ALL'], all == [m for m in all if self.mb.IsChecked(m)])
        # update ruler alignment when visible
#FIX, at startup ruler not visible yet, 'if' condition commented for now
        # if self.midsp.IsSplit():
        num = cfg['Margin']['LineNumberWidth']
        sym = cfg['Margin']['SymbolWidth']
        fol = cfg['Margin']['FoldingWidth']
        tot = 0
        tot += num if self.mb.IsChecked(MB['MGN_NUM']) else 0
        tot += sym if self.mb.IsChecked(MB['MGN_SYM']) else 0
        tot += fol if self.mb.IsChecked(MB['MGN_FOL']) else 0
        self.rlr.set_offset(tot - doc.XOffset)

    def _update_page_tabs(self, doc, newtab=False):
        _dbg_funcname(2)
        if DEBUG['BASIC']: print('_update_page_tabs:')

        fnm = doc.filename
        pnm = doc.pathname
        pag = self.nb.Selection
        # add new tab to right of current tab
        if newtab:
            pag += 1
            ico = self._get_file_icon(doc.langtype)
            bmp = ico if self.mb.IsChecked(MB['LAY_FTI']) else wx.NullBitmap
            self.nb.InsertPage(pag, doc, fnm, bitmap=bmp)
#             self.nb.InsertPage(pag, self.edtsp, fnm, bitmap=bmp)
#             self.edtsp.SplitVertically(doc, doc, SASH['EDT'])
#             self.edtsp.Unsplit(doc)

        # build page tab tooltip
        tti = cfg['Notebook']['TabToolTipFileInfo']
        tip = pnm if 'P' in tti else fnm  # pathname or filename for all files
        # timestamps/size for existing files (having a dirname)
        if doc.dirname:
            doc._get_timestamps_size()
            cre = dtm.fromtimestamp(doc.date_cre).strftime(TIM_FMT)
            mod = dtm.fromtimestamp(doc.date_mod).strftime(TIM_FMT)
            acc = dtm.fromtimestamp(doc.date_acc).strftime(TIM_FMT)
#FIX, 'Size' string wraps at 'bytes'
            tip += '\n%s: %d Kb (%s bytes)' % ('Size\t', doc.file_szk, doc.file_szb) if 'S' in tti else ''
            tip += '\n%s: %s' % ('Created\t', cre) if 'C' in tti else ''
            tip += '\n%s: %s' % ('Modified', mod) if 'M' in tti else ''
            tip += '\n%s: %s' % ('Accessed', acc) if 'A' in tti else ''
#             print('  CRE:', cre, '  MOD:', mod, '  ACC:', acc)

        # file (tab) indicators
        if doc.IsModified():
            mod = cfg['General']['FileModifiedIndicator']
            fnm += mod
            pnm += mod
        if doc.ReadOnly:
            lck = cfg['General']['FileReadOnlyIndicator']
            fnm += lck
            pnm += lck

        self.SetTitle('%s - [%s]' % (appName, pnm))
#         self.nb.GetPageToolTip(pag)
        self.nb.SetPageToolTip(pag, tip)
        self.nb.SetPageText(pag, fnm)
        # self.spn.PageChanged(None)
        _dbg_FOCUS(doc)


# class Application(wx.App):
class Application(wx.App, inspection.InspectionMixin):
    """class Application"""
    def OnInit(self):
        _dbg_funcname()

        # set interval for UI update events
        wx.UpdateUIEvent.SetUpdateInterval(cfg['General']['UIEventUpdateInterval'])

#INFO, URL=https://stackoverflow.com/questions/21444951/wxpython-3-0-breaks-older-apps-locale-error
#NOTE, workaround: 'wx._core.wxAssertionError: C++ assertion "strcmp(setlocale(LC_ALL, NULL), "C") == 0" failed'
        # set system default locale
        self.locale = wx.Locale(wx.LANGUAGE_DEFAULT)

        # # desktop width, height
        # _W = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
        # _H = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)

        # window position, width, height
        _X = cfg['Window']['PositionX']
        _Y = cfg['Window']['PositionY']
        _W = cfg['Window']['Width']
        _H = cfg['Window']['Height']

        self.frame = frame = MainWindow(None, title=appName, pos=(_X, _Y), size=(_W, _H))
        frame.SetIcon(appIcon.Icon)

        # initialize InspectionMixin base class
        if APP_INSPECTION:
            self.InitInspection(alt=APP_INSP['ALT'],
                                cmd=APP_INSP['CTRL'],
                                shift=APP_INSP['SHIFT'],
                                keyCode=ord(APP_INSP['KEY']))

#TODO, use 'wx.adv.TaskBarIcon' for system tray icon
#INFO, URL=https://wxpython.org/Phoenix/docs/html/wx.adv.TaskBarIcon.html
#INFO, see demo  "D:\Dev\D\wx\TSN_SPyE\_ToDo\demo\archive\demo_TSN_SystemTrayIcon.7z"

#INFO, URL=https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
        if TASKBAR_ICO:
            myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

#TODO, style=wx.FRAME_EX_CONTEXTHELP
#INFO, URL=https://docs.wxpython.org/wx.Frame.html?highlight=window%20extra%20styles#extra-styles-window-extra-styles
#NOTE, MAXIMIZE/MINIMIZE_BOX are automatically turned off if this style is used
        if HELP_CONTEXT:
            frame.SetExtraStyle(wx.FRAME_EX_CONTEXTHELP)

#         _s = wx.BoxSizer(wx.HORIZONTAL)
# #         _s.Add(frame.nb, 1, wx.EXPAND)
#         frame.SetSizer(_s)
#         frame.SetAutoLayout(True)

        self.SetTopWindow(frame)
        frame.Show(True)

        if cfg['General']['ShowSplash']:
            self.Splash(frame, timeout=cfg['General']['DelayHideSplash'])

######################################################
######################################################
        self.Bind(wx.EVT_SET_FOCUS, self.GotFocus)
#         self.Bind(wx.EVT_ENTER_WINDOW, self.GotFocus)
#         self.Bind(wx.EVT_LEAVE_WINDOW, self.LostFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.LostFocus)
######################################################
######################################################

#FIX: get window name under mouse cursor
        if DEBUG['WINNM']:
            self.Bind(wx.EVT_SET_CURSOR, self._win_under_cursor)
            self.prv_nam = None

        return True

############################################################################
############################################################################

#FIX: get window name under mouse cursor
    def _win_under_cursor(self, evt):
        if not (wx.GetKeyState(wx.WXK_CONTROL) and wx.GetKeyState(wx.WXK_ALT)):
            return
        pos = wx.GetMouseState().Position
        win = wx.FindWindowAtPoint(pos)
        nam = str(win)
        end = nam.find(' object at ')
        start = nam.rfind('.') + 1
        nam = nam[start:end]
        if self.prv_nam == nam:
            return
        self.prv_nam = nam
        print(nam)
    #     self.HighlightWindow(win)

    # def HighlightWindow(self, win):
    #     rect = win.GetRect()
    #     tlw = win.TopLevelParent
    #     pos = win.ClientToScreen((0,0))
    #     rect.SetPosition(pos)
    #     for i in range(10):
    #         self.DoHighlight(tlw, rect, 'RED')
    #     for i in range(10):
    #         self.DoHighlight(tlw, rect, None, mode='Clear')

    # def DoHighlight(self, tlw, rect, colour, penWidth=2, mode=0):
    #     dc = wx.ScreenDC()
    #     dc.SetPen(wx.Pen(colour, penWidth))
    #     dc.SetBrush(wx.TRANSPARENT_BRUSH)

    #     drawRect = wx.Rect(*rect)
    #     drawRect.Deflate(2,2)
    #     if mode == 'Clear':
    #         dc.SetPen(wx.TRANSPARENT_PEN)
    #     dc.DrawRectangle(drawRect)

############################################################################
############################################################################

    def OnExit(self):
        _dbg_funcname()
        pass
        # print('OnExit')
        return True

######################################################
######################################################
    @staticmethod
    def GotFocus(evt):
        _dbg_funcname(2)
        if DEBUG['FOCUS']: print('+%s  got focus' % appName)
        app.focus = True
#DONE, workaround: unresponsive Choicebook in side panel
        evt.Skip()

    @staticmethod
    def LostFocus(evt):
        _dbg_funcname(2)
        if DEBUG['FOCUS']: print('-%s lost focus' % appName)
        app.focus = False
#DONE, workaround: wx.TextCtrl focus issues in search panel
        evt.Skip()
######################################################
######################################################

    @staticmethod
    def Splash(frame, timeout=0):
        _dbg_funcname()
        bmp = PNG['app_splash_SPyE_NEW'].Bitmap
        sty = splash.AS_TIMEOUT if timeout else splash.AS_NOTIMEOUT
        bmp = splash.AdvancedSplash(frame, bitmap=bmp, timeout=timeout,
                                    agwStyle=splash.AS_CENTER_ON_PARENT | sty)
        # bmp.SetText('SPyE')
        # bmp.SetTextColour('DARK GRAY')
        # bmp.SetTextFont(wx.Font(wx.FontInfo(77).Bold().Italic()))
        # bmp.SetTextPosition((0, 78))


########################### SafeShowMessage RESEARCH ##########################
# wx.SafeShowMessage('wx.SafeShowMessage (TITLE)', 'wx.SafeShowMessage (TEXT)')
###############################################################################


if __name__ == '__main__':
    # debug file
    fnm = LOC['DBG']['FIL']
    if not os.path.isfile(fnm):
#NOTE, variable 'dbg' not used
        dbg = DbgCreate(fnm)
    dbg = DbgRead(fnm)

    # startup info
    _dbg_STARTUP()

#TODO, put sessions in 'config\SPyE.ssn' (no .default?):
    # fnm = LOC['SSN']['FIL']
    # if not os.path.isfile(fnm):
    #     ssn = SsnCreate(fnm)
    # ssn = SsnRead(fnm)

    # config file
    fnm = LOC['CFG']['FIL']
    if not os.path.isfile(fnm):
        cfg = CfgCreate(fnm)
    cfg, open_list, recent_list = CfgRead(fnm)

    _dbg_CONFIG(cfg)

    # language file
    fnm = LOC['LNG']['FIL']
    if not os.path.isfile(fnm):
#NOTE, variable 'lng' not used
        lng = LngCreate(fnm)
    lng = LngRead(fnm)

    # default file copy
    for loc in (LOC['DBG'], LOC['CFG'], LOC['LNG']):
    # for loc in (LOC['DBG'], LOC['SSN'], LOC['CFG'], LOC['LNG']):
        if not os.path.isfile(loc['DFT']):
            copyfile(loc['FIL'], loc['DFT'])

    app = Application(redirect=APP_REDIRECT, filename=APP_REDIRECT_FNM)

    CfgApply(app, cfg, open_list, recent_list)
    # LngApply(app, lng)

#     import win32ui
#     print(win32ui.GetAppName())
#     print(win32ui.GetApp())
#     win32ui.SetDialogBkColor(int(wx.Colour(192, 192, 192).RGB), int(wx.Colour(0, 0, 0).RGB))

    # ColourDatabase
    _dbg_CLRDB()
    # Scintilla commands
    _dbg_SCINTILLA_CMDS()

    # system trace function
    if DEBUG['SYSTF']:
        sys.settrace(_dbg_TRACEFUNC)

#######################
# temporary code: TRACE
#######################
    # DO_NOT_TRACEFUNCS = [
    #     '<lambda>',
    #     '__getitem__',
    #     '__init__',
    #     '__new__',
    #     '__setitem__',
    #     '__stop',
    #     '_a_to_u',
    #     '_checkInstance',
    #     '_complain_ifclosed',
    #     '_dbg_funcname',
    #     '_decode_element',
    #     '_EvtHandler_Bind',
    #     '_exitfunc',
    #     '_get_bookmarks',
    #     '_get_docstate',
    #     '_get_file_icon',
    #     '_get_single_quote',
    #     '_get_timestamps_size',
    #     '_get_triple_quote',
    #     '_getPagDoc',
    #     '_handle_comment',
    #     '_initialise',
    #     '_interpolate',
    #     '_is_owned',
    #     '_note',
    #     '_pickSomeNonDaemonThread',
    #     '_pop_statustext',
    #     '_PyEvent_Clone',
    #     '_quote',
    #     '_run_exitfuncs',
    #     '_set_docstate',
    #     '_set_language_styling',
    #     '_update_page_tabs',
    #     '_Window___nonzero__',
    #     '_write_line',
    #     '_write_marker',
    #     'b64decode',
    #     'Bind',
    #     'Codec',
    #     'daemon',
    #     'encode',
    #     'enumerate',
    #     'getatime',
    #     'generate_tokens',
    #     'GetBitmap',
    #     'getctime',
    #     'getmtime',
    #     'getregentry',
    #     'getsize',
    #     'GotFocus',
    #     'IncrementalDecoder',
    #     'interpolate',
    #     'isAlive',
    #     'isAlive',
    #     'islink',
    #     'isSet',
    #     'isSet',
    #     'join',
    #     'LostFocus',
    #     'normalize_encoding',
    #     'Notify',
    #     'notify',
    #     'notifyAll',
    #     'OnIdle',
    #     'read',
    #     'RestoreStdio',
    #     'seek',
    #     'SetArgs',
    #     'splitdrive',
    #     'Start',
    #     'Stop',
    #     'StreamConverter',
    #     'StreamReader',
    #     'StreamWriter',
    #     'Styling',
    #     'tell',
    #     'update_code_context',
    #     'UpdateUI',
    #     'UpdateUIDoc',
    #     'UpdateUIFnd',
    #     'UpdateUIMod',
    #     'UpdateUISel',
    #     'walk',
    #     'write',
    # ]

    # def tracefunc(frame, event, arg, indent=[0]):
    #     if frame.f_code.co_name in DO_NOT_TRACEFUNCS:
    #         return None
    #     if event == "call":
    #         indent[0] += 2
    #         print("-" * indent[0] + "> call function", frame.f_code.co_name)
    #     elif event == "return":
    #         print("<" + "-" * indent[0], "exit function", frame.f_code.co_name)
    #         indent[0] -= 2
    #     return tracefunc

    # sys.settrace(tracefunc)
#######################
# temporary code: TRACE
#######################

#TODO, move 'print' to 'now_' in 'util.py' at 2nd call
    # timing
    if DEBUG['TIMER']:
        startup_time = now_() - startup_time
        print('startup_time: %6d ms' % (startup_time))
    # print(tmr.stop())

############################################################################
    # TEST: BusyInfo banner
############################################################################

    # # 0. wx version (simple)
    # import time
    # wait = wx.BusyInfo('wx version (simple):\n\nPlease wait, working...')
    # time.sleep(2)
    # del wait

    # # 1. wx version
    # disableAll = wx.WindowDisabler()
    # wait = wx.BusyInfo('wx version:\n\nPlease wait, working...', app.frame)
    # for i in range(10000000):
    #     if i % 1000 == 0:
    #         wx.GetApp().Yield()
    # del wait, disableAll

    # # 2. wx.lib version
    # from wx.lib.busy import BusyInfo
    # disableAll = wx.WindowDisabler()
    # wait = BusyInfo('wx.lib version:\n\nPlease wait, working...', app.frame)
    # for i in range(10000000):
    #     if i % 1000 == 0:
    #         wx.GetApp().Yield()
    # del wait, disableAll

    # # 3. wx.lib.agw.pybusyinfo version
    # import wx.lib.agw.pybusyinfo as PBI
    # busy = PBI.PyBusyInfo('wx.lib.agw.pybusyinfo:\n\nPlease wait, working...', parent=app.frame, title='Really Busy')
    # wx.MilliSleep(2000)
    # del busy

############################################################################
    # TEST: BusyInfo banner
############################################################################

    app.MainLoop()

#TODO, move 'print' to 'now_' in 'util.py' at 2nd call
    # timing
    if DEBUG['TIMER'] > 1:
        session_time = now_() - session_time
        print('session_time: %6d ms' % (session_time))
