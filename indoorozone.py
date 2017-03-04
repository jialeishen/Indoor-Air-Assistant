import numpy  
import wx  
import wx.lib.plot as wxPyPlot
from collections import OrderedDict

class MyFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, -1, 'Indoor Ozone', size = (600,600))
		panel = wx.Panel(self)
		
		#outdoor ozone
		self.outppb = wx.SpinCtrl(panel, -1, 'Outdoor Ozone', (30,40), (80,-1))
		self.outppb.SetRange(0,10000)
		self.outppb.SetValue(60)
		outppblabel1 = wx.StaticText(panel, -1, 'Outdoor Ozone:', (20,20))
		outppblabel2 = wx.StaticText(panel, -1, 'ppb', (115,40))
		self.outppb.Bind(wx.EVT_TEXT, self.OnOutPpb)

		#air change rate
		self.ach = wx.Slider(panel, -1, 5, 0, 200, (30,90), (80,-1), 
			style = wx.SL_HORIZONTAL|wx.SL_TOP)
		self.ach.Bind(wx.EVT_SCROLL, self.OnScroll)
		self.achvalue = wx.TextCtrl(panel, -1, str(self.ach.GetValue()/10.0), (110,90), (35,-1))
		self.achvalue.Bind(wx.EVT_TEXT, self.OnText)
		achlabel1 = wx.StaticText(panel, -1, 'Air Change Per Hour:', (20,70))
		achlabel2 = wx.StaticText(panel, -1, '/h', (150,90))

		#indoor source
		sourcelist = ['yes', 'no']
		self.indoorsource = wx.RadioBox(panel, -1, 'Indoor Source', (20,120), wx.DefaultSize, 
			sourcelist, 2, wx.RA_SPECIFY_COLS)
		
	
		
		
		materiallist = list(material.keys())
		print materiallist
		#v = d.values()
		self.choice = wx.Choice(panel, -1, pos = (200,-1), size = (100,-1), choices = materiallist)
		self.choice.SetSelection(0)
		print self.choice.Bind(wx.EVT_CHOICE, self.OnCheck)
	
	def OnCheck(self, event):
		print material.get(self.choice.GetStringSelection())
	
	def OnOutPpb(self, event):
		print self.outppb.GetValue()
		#result = wx.StaticText(self, -1, str(self.outppb.GetValue()), (200,40))
	
	def OnScroll(self, event):
		self.achvalue.SetValue(str(self.ach.GetValue()/10.0))
		print 'ACH: ', self.ach.GetValue()/10.0
	
	def OnText(self, event):
		try:
			if float(self.achvalue.GetValue()) >20.0:
				self.ach.SetValue(200)
			elif float(self.achvalue.GetValue()) <0.0:
				self.ach.SetValue(0)
			else:
				self.ach.SetValue(int(float(self.achvalue.GetValue())*10))
			print 'ACH: ', self.ach.GetValue()/10.0
		except ValueError:
			print 'please input a number(0-20)...'

		
		
if __name__ == '__main__':
	material = OrderedDict([
		('a',1), ('b',2), ('c',3), 
		('d',4), ('e',5), ('f',6), 
		('g',7), ('h',8), ('i',9), 
		('j',10)])
	app = wx.App()
	MyFrame().Show()
	app.MainLoop()
