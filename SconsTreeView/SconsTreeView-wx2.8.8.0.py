from wx import *
import os
import sys

ID_OPEN=102

class SconsTreeView(wx.App):
  def OnInit(self):
    frame = wx.Frame(None, -1, 'Scons tree view')
    self.frame=frame
    frame.Show(True)
    self.SetTopWindow(frame)

    filemenu = wx.Menu()
    filemenu.Append(ID_OPEN, '&Open')
    menuBar = wx.MenuBar()
    menuBar.Append(filemenu, '&File')
    frame.SetMenuBar(menuBar)
    EVT_MENU(self, ID_OPEN, self.OnOpen)

    self.tree = wx.TreeCtrl(frame)
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    sizer.Add(self.tree, 1, wx.EXPAND)
    frame.SetSizer(sizer)
    frame.SetAutoLayout(1)
    sizer.Fit(frame)
    if (len(sys.argv) > 1):
      f = open(sys.argv[1], 'r')
      print f
      self.Parse(f)
    return True

  def OnOpen(self, evt):
    dlg = wx.FileDialog(self.frame, "Choose a file", "", "", "*.*", wx.OPEN)
    if dlg.ShowModal() == wx.ID_OK:
      filename = dlg.GetFilename()
      dirname = dlg.GetDirectory()
      f = open(os.path.join(dirname, filename), 'r')
      self.Parse(f)
      f.close()
    dlg.Destroy()

  def Parse(self, f):
    t = self.tree
    t.DeleteAllItems()
    for line in f:
      if line.startswith('+') and line.find('-') != -1:
        lastdepth = line.index('-')/2
        nodes = [ t.AddRoot('.') ]
        break

    lastnode = nodes[-1]
    for line in f:
      if line.find('-') == -1:
        break
      depth=line.index('-')/2
      content = line[line.index('-')+1:]
      if depth > lastdepth:
        nodes.append(lastnode)
        lastnode = t.AppendItem(nodes[-1], content)
      elif depth < lastdepth:
        for i in range(depth, lastdepth):
          nodes.pop()
        lastnode = t.AppendItem(nodes[-1], content)
      else:
        lastnode = t.AppendItem(nodes[-1], content)
      lastdepth = depth

app=SconsTreeView(0)
app.MainLoop()
