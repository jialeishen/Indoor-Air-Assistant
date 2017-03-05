import numpy 
import math 
import wx  
import wx.lib.plot as wxPyPlot
from collections import OrderedDict

class MyFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, -1, 'Indoor Ozone', size = (800,600))
		panel = wx.Panel(self)

		self.statusbar = self.CreateStatusBar()
		self.statusbar.SetStatusText('Indoor Ozone Estimation')
		
		#outdoor ozone
		self.outppb = wx.SpinCtrl(panel, -1, 'Outdoor Ozone', (30,40), (80,-1))
		self.outppb.SetRange(0,10000)
		self.outppb.SetValue(60)
		outppblabel1 = wx.StaticText(panel, -1, 'Outdoor Ozone:', (20,20))
		outppblabel2 = wx.StaticText(panel, -1, 'ppb', (115,40))
		self.outppb.Bind(wx.EVT_TEXT, self.OutPpb)

		#air change rate
		self.ach = wx.Slider(panel, -1, 5, 0, 200, (30,90), (80,-1), 
			style = wx.SL_HORIZONTAL|wx.SL_TOP)
		self.ach.Bind(wx.EVT_SCROLL, self.ACHScroll)
		self.achvalue = wx.TextCtrl(panel, -1, str(self.ach.GetValue()/10.0), (110,90), (35,-1))
		self.achvalue.Bind(wx.EVT_TEXT, self.ACHText)
		achlabel1 = wx.StaticText(panel, -1, 'Air Change Per Hour:', (20,70))
		achlabel2 = wx.StaticText(panel, -1, '/h', (150,90))

		#indoor source
		sourcelist = ['yes', 'no']
		self.indoorsource = wx.RadioBox(panel, -1, 'Indoor Source', (20,120), wx.DefaultSize, 
			sourcelist, 2, wx.RA_SPECIFY_COLS)
		#button.Enable()
		
		#room volume
		self.volume = wx.TextCtrl(panel, -1, '1', (200,40), (80,-1))
		self.volume.Bind(wx.EVT_TEXT, self.VolumeText)
		volumelabel1 = wx.StaticText(panel, -1, 'Room Volume:', (190,20))
		volumelabel2 = wx.StaticText(panel, -1, 'm3', (285,40))

		#material 1
		materiallist = list(material.keys())

		self.material1 = wx.Choice(panel, -1, pos = (200,100), size = (180,-1), choices = materiallist)
		self.material1.SetSelection(0)
		self.area1 = wx.TextCtrl(panel, -1, '0', (390,100), (40,-1))
		materiallabel1 = wx.StaticText(panel, -1, 'Floor:', (190,75))
		arealabel1 = wx.StaticText(panel, -1, 'm2', (435,100))
		self.material1.Bind(wx.EVT_CHOICE, self.ChooseMaterial1)
		self.area1.Bind(wx.EVT_TEXT, self.AreaText1)

		#material 2
		self.material2 = wx.Choice(panel, -1, pos = (200,160), size = (180,-1), choices = materiallist)
		self.material2.SetSelection(0)
		self.area2 = wx.TextCtrl(panel, -1, '0', (390,160), (40,-1))
		materiallabel2 = wx.StaticText(panel, -1, 'Ceiling:', (190,135))
		arealabel2 = wx.StaticText(panel, -1, 'm2', (435,160))
		self.material2.Bind(wx.EVT_CHOICE, self.ChooseMaterial2)
		self.area2.Bind(wx.EVT_TEXT, self.AreaText2)

		#material 3
		self.material3 = wx.Choice(panel, -1, pos = (200,220), size = (180,-1), choices = materiallist)
		self.material3.SetSelection(0)
		self.area3 = wx.TextCtrl(panel, -1, '0', (390,220), (40,-1))
		materiallabel3 = wx.StaticText(panel, -1, 'Wall1:', (190,195))
		arealabel3 = wx.StaticText(panel, -1, 'm2', (435,220))
		self.material3.Bind(wx.EVT_CHOICE, self.ChooseMaterial3)
		self.area3.Bind(wx.EVT_TEXT, self.AreaText3)

		#material 4
		self.material4 = wx.Choice(panel, -1, pos = (200,280), size = (180,-1), choices = materiallist)
		self.material4.SetSelection(0)
		self.area4 = wx.TextCtrl(panel, -1, '0', (390,280), (40,-1))
		materiallabel4 = wx.StaticText(panel, -1, 'Wall2:', (190,255))
		arealabel4 = wx.StaticText(panel, -1, 'm2', (435,280))
		self.material4.Bind(wx.EVT_CHOICE, self.ChooseMaterial4)
		self.area4.Bind(wx.EVT_TEXT, self.AreaText4)

		#material 5
		self.material5 = wx.Choice(panel, -1, pos = (500,100), size = (180,-1), choices = materiallist)
		self.material5.SetSelection(0)
		self.area5 = wx.TextCtrl(panel, -1, '0', (690,100), (40,-1))
		materiallabel5 = wx.StaticText(panel, -1, 'Surface:', (490,75))
		arealabel5 = wx.StaticText(panel, -1, 'm2', (735,100))
		self.material5.Bind(wx.EVT_CHOICE, self.ChooseMaterial5)
		self.area5.Bind(wx.EVT_TEXT, self.AreaText5)

		#material 6
		self.material6 = wx.Choice(panel, -1, pos = (500,160), size = (180,-1), choices = materiallist)
		self.material6.SetSelection(0)
		self.area6 = wx.TextCtrl(panel, -1, '0', (690,160), (40,-1))
		materiallabel6 = wx.StaticText(panel, -1, 'Surface:', (490,135))
		arealabel6 = wx.StaticText(panel, -1, 'm2', (735,160))
		self.material6.Bind(wx.EVT_CHOICE, self.ChooseMaterial6)
		self.area6.Bind(wx.EVT_TEXT, self.AreaText6)

		#material 7
		self.material7 = wx.Choice(panel, -1, pos = (500,220), size = (180,-1), choices = materiallist)
		self.material7.SetSelection(0)
		self.area7 = wx.TextCtrl(panel, -1, '0', (690,220), (40,-1))
		materiallabel7 = wx.StaticText(panel, -1, 'Wall1:', (490,195))
		arealabel7 = wx.StaticText(panel, -1, 'm2', (735,220))
		self.material7.Bind(wx.EVT_CHOICE, self.ChooseMaterial7)
		self.area7.Bind(wx.EVT_TEXT, self.AreaText7)

		#material 8
		self.material8 = wx.Choice(panel, -1, pos = (500,280), size = (180,-1), choices = materiallist)
		self.material8.SetSelection(0)
		self.area8 = wx.TextCtrl(panel, -1, '0', (690,280), (40,-1))
		materiallabel8 = wx.StaticText(panel, -1, 'Surface:', (490,255))
		arealabel8 = wx.StaticText(panel, -1, 'm2', (735,280))
		self.material8.Bind(wx.EVT_CHOICE, self.ChooseMaterial8)
		self.area8.Bind(wx.EVT_TEXT, self.AreaText8)

		#show inppb result
		self.inppb = wx.StaticText(panel, -1, 'Ozone', (500,450))
		self.inppb.SetForegroundColour('blue')
		font = wx.Font(25, wx.DECORATIVE, wx.ITALIC, wx.BOLD)
		self.inppb.SetFont(font)
		inppblabel = wx.StaticText(panel, -1, 'Indoor Ozone: ', (400,350))


	def OutPpb(self, event):
		print self.outppb.GetValue()
		self.inppb.SetLabel(str(eqsteady(float(self.outppb.GetValue()), self.ach.GetValue()/10.0, float(self.volume.GetValue()), 0, getsumvda(material.get(self.material1.GetStringSelection()), float(self.area1.GetValue()), material.get(self.material2.GetStringSelection()), float(self.area2.GetValue()), material.get(self.material3.GetStringSelection()), float(self.area3.GetValue()), material.get(self.material4.GetStringSelection()), float(self.area4.GetValue()), material.get(self.material5.GetStringSelection()), float(self.area5.GetValue()), material.get(self.material6.GetStringSelection()), float(self.area6.GetValue()), material.get(self.material7.GetStringSelection()), float(self.area7.GetValue()), material.get(self.material8.GetStringSelection()), float(self.area8.GetValue()), getvt(self.ach.GetValue()/10.0) )))+' ppb')
		self.statusbar.SetStatusText('')
	
	def ACHScroll(self, event):
		self.achvalue.SetValue(str(self.ach.GetValue()/10.0))
		self.inppb.SetLabel(str(eqsteady(float(self.outppb.GetValue()), self.ach.GetValue()/10.0, float(self.volume.GetValue()), 0, getsumvda(material.get(self.material1.GetStringSelection()), float(self.area1.GetValue()), material.get(self.material2.GetStringSelection()), float(self.area2.GetValue()), material.get(self.material3.GetStringSelection()), float(self.area3.GetValue()), material.get(self.material4.GetStringSelection()), float(self.area4.GetValue()), material.get(self.material5.GetStringSelection()), float(self.area5.GetValue()), material.get(self.material6.GetStringSelection()), float(self.area6.GetValue()), material.get(self.material7.GetStringSelection()), float(self.area7.GetValue()), material.get(self.material8.GetStringSelection()), float(self.area8.GetValue()), getvt(self.ach.GetValue()/10.0) )))+' ppb')
		print 'ACH: ', self.ach.GetValue()/10.0
		self.statusbar.SetStatusText('')
	
	def ACHText(self, event):
		try:
			if float(self.achvalue.GetValue()) >20.0:
				self.ach.SetValue(200)
			elif float(self.achvalue.GetValue()) <0.0:
				self.ach.SetValue(0)
			else:
				self.ach.SetValue(int(float(self.achvalue.GetValue())*10))
			print 'ACH: ', self.ach.GetValue()/10.0
			self.inppb.SetLabel(str(eqsteady(float(self.outppb.GetValue()), self.ach.GetValue()/10.0, float(self.volume.GetValue()), 0, getsumvda(material.get(self.material1.GetStringSelection()), float(self.area1.GetValue()), material.get(self.material2.GetStringSelection()), float(self.area2.GetValue()), material.get(self.material3.GetStringSelection()), float(self.area3.GetValue()), material.get(self.material4.GetStringSelection()), float(self.area4.GetValue()), material.get(self.material5.GetStringSelection()), float(self.area5.GetValue()), material.get(self.material6.GetStringSelection()), float(self.area6.GetValue()), material.get(self.material7.GetStringSelection()), float(self.area7.GetValue()), material.get(self.material8.GetStringSelection()), float(self.area8.GetValue()), getvt(self.ach.GetValue()/10.0) )))+' ppb')
			self.statusbar.SetStatusText('')
		except ValueError:
			self.statusbar.SetStatusText('ValueError! Please input a number in (0,20)...')

	def VolumeText(self, event):
		try:
			self.inppb.SetLabel(str(eqsteady(float(self.outppb.GetValue()), self.ach.GetValue()/10.0, float(self.volume.GetValue()), 0, getsumvda(material.get(self.material1.GetStringSelection()), float(self.area1.GetValue()), material.get(self.material2.GetStringSelection()), float(self.area2.GetValue()), material.get(self.material3.GetStringSelection()), float(self.area3.GetValue()), material.get(self.material4.GetStringSelection()), float(self.area4.GetValue()), material.get(self.material5.GetStringSelection()), float(self.area5.GetValue()), material.get(self.material6.GetStringSelection()), float(self.area6.GetValue()), material.get(self.material7.GetStringSelection()), float(self.area7.GetValue()), material.get(self.material8.GetStringSelection()), float(self.area8.GetValue()), getvt(self.ach.GetValue()/10.0) )))+' ppb')
			self.statusbar.SetStatusText('')
		except ValueError:
			self.statusbar.SetStatusText('ValueError! Please input a number...')

	def ChooseMaterial1(self, event):
		self.inppb.SetLabel(str(eqsteady(float(self.outppb.GetValue()), self.ach.GetValue()/10.0, float(self.volume.GetValue()), 0, getsumvda(material.get(self.material1.GetStringSelection()), float(self.area1.GetValue()), material.get(self.material2.GetStringSelection()), float(self.area2.GetValue()), material.get(self.material3.GetStringSelection()), float(self.area3.GetValue()), material.get(self.material4.GetStringSelection()), float(self.area4.GetValue()), material.get(self.material5.GetStringSelection()), float(self.area5.GetValue()), material.get(self.material6.GetStringSelection()), float(self.area6.GetValue()), material.get(self.material7.GetStringSelection()), float(self.area7.GetValue()), material.get(self.material8.GetStringSelection()), float(self.area8.GetValue()), getvt(self.ach.GetValue()/10.0) )))+' ppb')
		self.statusbar.SetStatusText('')

	def AreaText1(self, event):
		try:
			self.inppb.SetLabel(str(eqsteady(float(self.outppb.GetValue()), self.ach.GetValue()/10.0, float(self.volume.GetValue()), 0, getsumvda(material.get(self.material1.GetStringSelection()), float(self.area1.GetValue()), material.get(self.material2.GetStringSelection()), float(self.area2.GetValue()), material.get(self.material3.GetStringSelection()), float(self.area3.GetValue()), material.get(self.material4.GetStringSelection()), float(self.area4.GetValue()), material.get(self.material5.GetStringSelection()), float(self.area5.GetValue()), material.get(self.material6.GetStringSelection()), float(self.area6.GetValue()), material.get(self.material7.GetStringSelection()), float(self.area7.GetValue()), material.get(self.material8.GetStringSelection()), float(self.area8.GetValue()), getvt(self.ach.GetValue()/10.0) )))+' ppb')
			self.statusbar.SetStatusText('')
		except ValueError:
			self.statusbar.SetStatusText('ValueError! Please input a number...')

	def ChooseMaterial2(self, event):
		self.inppb.SetLabel(str(eqsteady(float(self.outppb.GetValue()), self.ach.GetValue()/10.0, float(self.volume.GetValue()), 0, getsumvda(material.get(self.material1.GetStringSelection()), float(self.area1.GetValue()), material.get(self.material2.GetStringSelection()), float(self.area2.GetValue()), material.get(self.material3.GetStringSelection()), float(self.area3.GetValue()), material.get(self.material4.GetStringSelection()), float(self.area4.GetValue()), material.get(self.material5.GetStringSelection()), float(self.area5.GetValue()), material.get(self.material6.GetStringSelection()), float(self.area6.GetValue()), material.get(self.material7.GetStringSelection()), float(self.area7.GetValue()), material.get(self.material8.GetStringSelection()), float(self.area8.GetValue()), getvt(self.ach.GetValue()/10.0) )))+' ppb')
		self.statusbar.SetStatusText('')

	def AreaText2(self, event):
		try:
			self.inppb.SetLabel(str(eqsteady(float(self.outppb.GetValue()), self.ach.GetValue()/10.0, float(self.volume.GetValue()), 0, getsumvda(material.get(self.material1.GetStringSelection()), float(self.area1.GetValue()), material.get(self.material2.GetStringSelection()), float(self.area2.GetValue()), material.get(self.material3.GetStringSelection()), float(self.area3.GetValue()), material.get(self.material4.GetStringSelection()), float(self.area4.GetValue()), material.get(self.material5.GetStringSelection()), float(self.area5.GetValue()), material.get(self.material6.GetStringSelection()), float(self.area6.GetValue()), material.get(self.material7.GetStringSelection()), float(self.area7.GetValue()), material.get(self.material8.GetStringSelection()), float(self.area8.GetValue()), getvt(self.ach.GetValue()/10.0) )))+' ppb')
			self.statusbar.SetStatusText('')
		except ValueError:
			self.statusbar.SetStatusText('ValueError! Please input a number...')

	def ChooseMaterial3(self, event):
		self.inppb.SetLabel(str(eqsteady(float(self.outppb.GetValue()), self.ach.GetValue()/10.0, float(self.volume.GetValue()), 0, getsumvda(material.get(self.material1.GetStringSelection()), float(self.area1.GetValue()), material.get(self.material2.GetStringSelection()), float(self.area2.GetValue()), material.get(self.material3.GetStringSelection()), float(self.area3.GetValue()), material.get(self.material4.GetStringSelection()), float(self.area4.GetValue()), material.get(self.material5.GetStringSelection()), float(self.area5.GetValue()), material.get(self.material6.GetStringSelection()), float(self.area6.GetValue()), material.get(self.material7.GetStringSelection()), float(self.area7.GetValue()), material.get(self.material8.GetStringSelection()), float(self.area8.GetValue()), getvt(self.ach.GetValue()/10.0) )))+' ppb')
		self.statusbar.SetStatusText('')

	def AreaText3(self, event):
		try:
			self.inppb.SetLabel(str(eqsteady(float(self.outppb.GetValue()), self.ach.GetValue()/10.0, float(self.volume.GetValue()), 0, getsumvda(material.get(self.material1.GetStringSelection()), float(self.area1.GetValue()), material.get(self.material2.GetStringSelection()), float(self.area2.GetValue()), material.get(self.material3.GetStringSelection()), float(self.area3.GetValue()), material.get(self.material4.GetStringSelection()), float(self.area4.GetValue()), material.get(self.material5.GetStringSelection()), float(self.area5.GetValue()), material.get(self.material6.GetStringSelection()), float(self.area6.GetValue()), material.get(self.material7.GetStringSelection()), float(self.area7.GetValue()), material.get(self.material8.GetStringSelection()), float(self.area8.GetValue()), getvt(self.ach.GetValue()/10.0) )))+' ppb')
			self.statusbar.SetStatusText('')
		except ValueError:
			self.statusbar.SetStatusText('ValueError! Please input a number...')

	def ChooseMaterial4(self, event):
		self.inppb.SetLabel(str(eqsteady(float(self.outppb.GetValue()), self.ach.GetValue()/10.0, float(self.volume.GetValue()), 0, getsumvda(material.get(self.material1.GetStringSelection()), float(self.area1.GetValue()), material.get(self.material2.GetStringSelection()), float(self.area2.GetValue()), material.get(self.material3.GetStringSelection()), float(self.area3.GetValue()), material.get(self.material4.GetStringSelection()), float(self.area4.GetValue()), material.get(self.material5.GetStringSelection()), float(self.area5.GetValue()), material.get(self.material6.GetStringSelection()), float(self.area6.GetValue()), material.get(self.material7.GetStringSelection()), float(self.area7.GetValue()), material.get(self.material8.GetStringSelection()), float(self.area8.GetValue()), getvt(self.ach.GetValue()/10.0) )))+' ppb')
		self.statusbar.SetStatusText('')

	def AreaText4(self, event):
		try:
			self.inppb.SetLabel(str(eqsteady(float(self.outppb.GetValue()), self.ach.GetValue()/10.0, float(self.volume.GetValue()), 0, getsumvda(material.get(self.material1.GetStringSelection()), float(self.area1.GetValue()), material.get(self.material2.GetStringSelection()), float(self.area2.GetValue()), material.get(self.material3.GetStringSelection()), float(self.area3.GetValue()), material.get(self.material4.GetStringSelection()), float(self.area4.GetValue()), material.get(self.material5.GetStringSelection()), float(self.area5.GetValue()), material.get(self.material6.GetStringSelection()), float(self.area6.GetValue()), material.get(self.material7.GetStringSelection()), float(self.area7.GetValue()), material.get(self.material8.GetStringSelection()), float(self.area8.GetValue()), getvt(self.ach.GetValue()/10.0) )))+' ppb')
			self.statusbar.SetStatusText('')
		except ValueError:
			self.statusbar.SetStatusText('ValueError! Please input a number...')

	def ChooseMaterial5(self, event):
		self.inppb.SetLabel(str(eqsteady(float(self.outppb.GetValue()), self.ach.GetValue()/10.0, float(self.volume.GetValue()), 0, getsumvda(material.get(self.material1.GetStringSelection()), float(self.area1.GetValue()), material.get(self.material2.GetStringSelection()), float(self.area2.GetValue()), material.get(self.material3.GetStringSelection()), float(self.area3.GetValue()), material.get(self.material4.GetStringSelection()), float(self.area4.GetValue()), material.get(self.material5.GetStringSelection()), float(self.area5.GetValue()), material.get(self.material6.GetStringSelection()), float(self.area6.GetValue()), material.get(self.material7.GetStringSelection()), float(self.area7.GetValue()), material.get(self.material8.GetStringSelection()), float(self.area8.GetValue()), getvt(self.ach.GetValue()/10.0) )))+' ppb')
		self.statusbar.SetStatusText('')

	def AreaText5(self, event):
		try:
			self.inppb.SetLabel(str(eqsteady(float(self.outppb.GetValue()), self.ach.GetValue()/10.0, float(self.volume.GetValue()), 0, getsumvda(material.get(self.material1.GetStringSelection()), float(self.area1.GetValue()), material.get(self.material2.GetStringSelection()), float(self.area2.GetValue()), material.get(self.material3.GetStringSelection()), float(self.area3.GetValue()), material.get(self.material4.GetStringSelection()), float(self.area4.GetValue()), material.get(self.material5.GetStringSelection()), float(self.area5.GetValue()), material.get(self.material6.GetStringSelection()), float(self.area6.GetValue()), material.get(self.material7.GetStringSelection()), float(self.area7.GetValue()), material.get(self.material8.GetStringSelection()), float(self.area8.GetValue()), getvt(self.ach.GetValue()/10.0) )))+' ppb')
			self.statusbar.SetStatusText('')
		except ValueError:
			self.statusbar.SetStatusText('ValueError! Please input a number...')

	def ChooseMaterial6(self, event):
		self.inppb.SetLabel(str(eqsteady(float(self.outppb.GetValue()), self.ach.GetValue()/10.0, float(self.volume.GetValue()), 0, getsumvda(material.get(self.material1.GetStringSelection()), float(self.area1.GetValue()), material.get(self.material2.GetStringSelection()), float(self.area2.GetValue()), material.get(self.material3.GetStringSelection()), float(self.area3.GetValue()), material.get(self.material4.GetStringSelection()), float(self.area4.GetValue()), material.get(self.material5.GetStringSelection()), float(self.area5.GetValue()), material.get(self.material6.GetStringSelection()), float(self.area6.GetValue()), material.get(self.material7.GetStringSelection()), float(self.area7.GetValue()), material.get(self.material8.GetStringSelection()), float(self.area8.GetValue()), getvt(self.ach.GetValue()/10.0) )))+' ppb')
		self.statusbar.SetStatusText('')

	def AreaText6(self, event):
		try:
			self.inppb.SetLabel(str(eqsteady(float(self.outppb.GetValue()), self.ach.GetValue()/10.0, float(self.volume.GetValue()), 0, getsumvda(material.get(self.material1.GetStringSelection()), float(self.area1.GetValue()), material.get(self.material2.GetStringSelection()), float(self.area2.GetValue()), material.get(self.material3.GetStringSelection()), float(self.area3.GetValue()), material.get(self.material4.GetStringSelection()), float(self.area4.GetValue()), material.get(self.material5.GetStringSelection()), float(self.area5.GetValue()), material.get(self.material6.GetStringSelection()), float(self.area6.GetValue()), material.get(self.material7.GetStringSelection()), float(self.area7.GetValue()), material.get(self.material8.GetStringSelection()), float(self.area8.GetValue()), getvt(self.ach.GetValue()/10.0) )))+' ppb')
			self.statusbar.SetStatusText('')
		except ValueError:
			self.statusbar.SetStatusText('ValueError! Please input a number...')

	def ChooseMaterial7(self, event):
		self.inppb.SetLabel(str(eqsteady(float(self.outppb.GetValue()), self.ach.GetValue()/10.0, float(self.volume.GetValue()), 0, getsumvda(material.get(self.material1.GetStringSelection()), float(self.area1.GetValue()), material.get(self.material2.GetStringSelection()), float(self.area2.GetValue()), material.get(self.material3.GetStringSelection()), float(self.area3.GetValue()), material.get(self.material4.GetStringSelection()), float(self.area4.GetValue()), material.get(self.material5.GetStringSelection()), float(self.area5.GetValue()), material.get(self.material6.GetStringSelection()), float(self.area6.GetValue()), material.get(self.material7.GetStringSelection()), float(self.area7.GetValue()), material.get(self.material8.GetStringSelection()), float(self.area8.GetValue()), getvt(self.ach.GetValue()/10.0) )))+' ppb')
		self.statusbar.SetStatusText('')

	def AreaText7(self, event):
		try:
			self.inppb.SetLabel(str(eqsteady(float(self.outppb.GetValue()), self.ach.GetValue()/10.0, float(self.volume.GetValue()), 0, getsumvda(material.get(self.material1.GetStringSelection()), float(self.area1.GetValue()), material.get(self.material2.GetStringSelection()), float(self.area2.GetValue()), material.get(self.material3.GetStringSelection()), float(self.area3.GetValue()), material.get(self.material4.GetStringSelection()), float(self.area4.GetValue()), material.get(self.material5.GetStringSelection()), float(self.area5.GetValue()), material.get(self.material6.GetStringSelection()), float(self.area6.GetValue()), material.get(self.material7.GetStringSelection()), float(self.area7.GetValue()), material.get(self.material8.GetStringSelection()), float(self.area8.GetValue()), getvt(self.ach.GetValue()/10.0) )))+' ppb')
			self.statusbar.SetStatusText('')
		except ValueError:
			self.statusbar.SetStatusText('ValueError! Please input a number...')

	def ChooseMaterial8(self, event):
		self.inppb.SetLabel(str(eqsteady(float(self.outppb.GetValue()), self.ach.GetValue()/10.0, float(self.volume.GetValue()), 0, getsumvda(material.get(self.material1.GetStringSelection()), float(self.area1.GetValue()), material.get(self.material2.GetStringSelection()), float(self.area2.GetValue()), material.get(self.material3.GetStringSelection()), float(self.area3.GetValue()), material.get(self.material4.GetStringSelection()), float(self.area4.GetValue()), material.get(self.material5.GetStringSelection()), float(self.area5.GetValue()), material.get(self.material6.GetStringSelection()), float(self.area6.GetValue()), material.get(self.material7.GetStringSelection()), float(self.area7.GetValue()), material.get(self.material8.GetStringSelection()), float(self.area8.GetValue()), getvt(self.ach.GetValue()/10.0) )))+' ppb')
		self.statusbar.SetStatusText('')

	def AreaText8(self, event):
		try:
			self.inppb.SetLabel(str(eqsteady(float(self.outppb.GetValue()), self.ach.GetValue()/10.0, float(self.volume.GetValue()), 0, getsumvda(material.get(self.material1.GetStringSelection()), float(self.area1.GetValue()), material.get(self.material2.GetStringSelection()), float(self.area2.GetValue()), material.get(self.material3.GetStringSelection()), float(self.area3.GetValue()), material.get(self.material4.GetStringSelection()), float(self.area4.GetValue()), material.get(self.material5.GetStringSelection()), float(self.area5.GetValue()), material.get(self.material6.GetStringSelection()), float(self.area6.GetValue()), material.get(self.material7.GetStringSelection()), float(self.area7.GetValue()), material.get(self.material8.GetStringSelection()), float(self.area8.GetValue()), getvt(self.ach.GetValue()/10.0) )))+' ppb')
			self.statusbar.SetStatusText('')
		except ValueError:
			self.statusbar.SetStatusText('ValueError! Please input a number...')

def eqsteady(outppb, ach, v, source, sumvda):
	ppbsteady = float(float(ach)*float(outppb)+float(source)/float(v))/(float(ach)+float(sumvda)/float(v))
	return round(ppbsteady, 1)

def eqdynamic(outppb, achdis, achvent, v, source, sumvda, t, tdis):
	initppb = float(float(achdis)*float(outppb))/(float(achdis)+float(sumvda)/float(v))
	ppbtdis = (initppb-float(float(achdis)*float(outppb)+float(source)/float(v))/(float(achdis)+float(sumvda)/float(v)))*math.exp(-(float(achdis)+float(float(sumvda)/float(v)))*tdis)+float(float(achdis)*float(outppb)+float(source)/float(v))/(float(achdis)+float(sumvda)/float(v))
	if t < tdis:
		ppbt = (initppb-float(float(achdis)*float(outppb)+float(source)/float(v))/(float(achdis)+float(sumvda)/float(v)))*math.exp(-(float(achdis)+float(float(sumvda)/float(v)))*t)+float(float(achdis)*float(outppb)+float(source)/float(v))/(float(achdis)+float(sumvda)/float(v))
	else:
		ppbt = (ppbtdis-float(float(achvent)*float(outppb))/(float(achvent)+float(sumvda)/float(v)))*math.exp(-(float(achvent)+float(float(sumvda)/float(v)))*(t-tdis))+float(float(achvent)*float(outppb))/(float(achvent)+float(sumvda)/float(v))	
	return round(ppbt, 1)	

def getsumvda(r1, a1, r2, a2, r3, a3, r4, a4, r5, a5, r6, a6, r7, a7, r8, a8, vt):
	vd1 = 36.*(float(vt)*float(r1)*36000./(4.*float(vt)+float(r1)*36000.))
	vd2 = 36.*(float(vt)*float(r2)*36000./(4.*float(vt)+float(r2)*36000.))
	vd3 = 36.*(float(vt)*float(r3)*36000./(4.*float(vt)+float(r3)*36000.))
	vd4 = 36.*(float(vt)*float(r4)*36000./(4.*float(vt)+float(r4)*36000.))
	vd5 = 36.*(float(vt)*float(r5)*36000./(4.*float(vt)+float(r5)*36000.))
	vd6 = 36.*(float(vt)*float(r6)*36000./(4.*float(vt)+float(r6)*36000.))
	vd7 = 36.*(float(vt)*float(r7)*36000./(4.*float(vt)+float(r7)*36000.))
	vd8 = 36.*(float(vt)*float(r8)*36000./(4.*float(vt)+float(r8)*36000.))
	sumvda = vd1*float(a1)+vd2*float(a2)+vd3*float(a3)+vd4*float(a4)+vd5*float(a5)+vd6*float(a6)+vd7*float(a7)+vd8*float(a8)
	return sumvda

def getvt(ach):
	vt0 = (float(ach)/20.)*0.6+0.1
	vt = vt0*36.
	return vt
		
if __name__ == '__main__':
	material = OrderedDict([
		('No material',0.0), ('Glass',6.06e-06), 
		('Lucite',5.50e-08), ('Metal, Aluminium',1.08e-07), 
		('Metal, Stainless steel',1.30e-06), ('Metal, Galvanized steel',1.10e-06), 
		('Ceramic',4.44e-07), ('Porcelain clay tile',1.02e-06), 
		('Resilient tile',1.11e-06), ('Concrete, Course',9.65e-06),
		('Concrete, Fine',4.20e-06), ('Stone material, Soft dense',7.82e-06), 
		('Stone material, Hard dense',1.67e-08), ('Floor, Wooden',1.20e-06), 
		('Floor, Finished hardwood',2.45e-06), ('Floor, Finished bamboo',1.95e-06), 
		('Ceiling tile, Perlite',1.02e-05), ('Ceiling tile, Mineral fiber',4.65e-05), 
		('Ceiling tile, Fiberglass',3.74e-05), ('Wallpaper',4.28e-06),
		('Fabric wall covering',5.30e-06), ('Paint, Latex',1.47e-06), 
		('Paint, Clay',5.65e-05), ('Paint, Water-based',4.90e-06), 
		('Paint, Oil-based',6.10e-06), ('Paint, Collagen',3.15e-06), 
		('Gypsum board, Painted',4.72e-06), ('Gypsum board, Untreated',1.73e-05), 
		('Wall plaster, Clay',2.20e-05), ('Green material, Sunflower',3.78e-06),
		('Green material, Cork',5.67e-06), ('Green material, Wheat',5.22e-06), 
		('Nylon',5.50e-08), ('FEP Teflon',5.50e-07), 
		('Rubber',6.86e-06), ('Neoprene',1.90e-06), 
		('Polyethylene sheet',1.10e-06), ('Medium density fibreboard',4.50e-06), 
		('Particle board',5.00e-07), ('Plywood',5.80e-07),
		('Bamboo',4.44e-07), ('Cedar',5.20e-06), 
		('Woodwork, Fine, hard',5.59e-07), ('Woodwork, Course, soft',4.16e-06), 
		('Cloth, <1 year old',8.99e-06), ('Cloth, >1 year old',7.06e-07), 
		('Linoleum',7.89e-07), ('Linen',6.30e-07), 
		('Carpet, Recycled',3.20e-05), ('Carpet, Fabric-backed',2.30e-05),
		('Carpet, Nylon',1.38e-05), ('Carpet, Olefin',1.01e-05), 
		('Carpet, Wool',1.06e-05), ('Brick',1.59e-05), 
		('Activated carbon cloth',2.24e-05)
		])
	app = wx.App()
	MyFrame().Show()
	app.MainLoop()
