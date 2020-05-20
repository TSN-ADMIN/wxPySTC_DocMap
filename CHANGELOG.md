[//]: # (NOTE: 'Date' is prefixed with 2 [Alt+255]'s to right align with 'Name')

wxPySTC_DocMap 0.4.1
---------------------------------------------
  **Date:** *2020-05-06  16:27*<br>
**Name:** *wxPySTC_DocMap_v0.4.1.py*<br>
- minor fixes


wxPySTC_DocMap 0.4
---------------------------------------------
  **Date:** *2020-05-06  12:01*<br>
**Name:** *wxPySTC_DocMap_v0.4.py*<br>
- minor fixes
- remove internal config of zone/map (POC)


wxPySTC_DocMap 0.3.2
---------------------------------------------
  **Date:** *2020-04-03  17:03*<br>
**Name:** *wxPySTC_DocMap_v0.3.2 - DragAcceptFiles - TEST.py*<br>
- add *EVT_DROP_FILES* event to test _DragAcceptFiles_


wxPySTC_DocMap 0.3.1
---------------------------------------------
  **Date:** *2020-03-08  20:46*<br>
**Name:** *wxPySTC_DocMap_v0.3.1.py*<br>
- minor fixes
- add internal config of zone/map (as POC):
    + *ARG_DEFAULTS* dict
    + *set_arg_values* function
    + modifiable to external config (e.g. file)


wxPySTC_DocMap 0.3
---------------------------------------------
  **Date:** *2020-03-05  01:58*<br>
**Name:** *wxPySTC_DocMap_v0.3.py*<br>
- minor fixes
- remove *wx.DragImage* related code to improve  efficiency
- remove *shown* attribute from *DragZone* class
- add hand cursor for dragging zone
- add method to *DocumentMap* class:
  + *ShowToolTip*: show top line in document


wxPySTC_DocMap 0.2
---------------------------------------------
  **Date:** *2020-02-29  21:01*<br>
**Name:** *wxPySTC_DocMap_v0.2.py*<br>
- minor fixes
- remove numpy
- add double buffering
- add copy/sync text selection from editor to map
- add zoom event *EVT_STC_ZOOM*
- add *EVT_LEFT_DCLICK* to prevent text selection in map
- add methods to *DocumentMap* class:
  + *GetDocScrollRatio*: document scroll ratio for map sync support
  + *GetTopLine*: top line in map
  + *GetTopY*: top Y coordinate of drag zone
  + *RefreshZone*: recreate drag zone after paint or size event
  + *SyncDoc*: set first visible line in *DocumentEditor* class


wxPySTC_DocMap 0.1
---------------------------------------------
  **Date:** *2020-02-17  22:12*<br>
**Name:** *wxPySTC_DocMap_v0.1.py*<br>
- initial release

