import numpy 
import math 
import wx  
import wx.lib.plot as wxPyPlot
from collections import OrderedDict

class MyFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, -1, 'Indoor Ozone', size = (600,600))
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
		
	
		
		
		materiallist = list(material.keys())
		print materiallist
		#v = d.values()
		self.choice = wx.Choice(panel, -1, pos = (200,-1), size = (180,-1), choices = materiallist)
		self.choice.SetSelection(0)
		print self.choice.Bind(wx.EVT_CHOICE, self.ChooseMaterial)

		self.inppb = wx.StaticText(panel, -1, 'Ozone', (350,450))
		self.inppb.SetForegroundColour('blue')
		font = wx.Font(25, wx.DECORATIVE, wx.ITALIC, wx.BOLD)
		self.inppb.SetFont(font)
		inppblabel = wx.StaticText(panel, -1, 'Indoor Ozone: ', (300,350))
        

	
	def ChooseMaterial(self, event):
		print material.get(self.choice.GetStringSelection())
	
	def OutPpb(self, event):
		print self.outppb.GetValue()
		self.inppb.SetLabel(str(eqsteady(float(self.outppb.GetValue()), self.ach.GetValue()/10.0, 45.0, 0, 68.85))+' ppb')
		self.statusbar.SetStatusText('')
	
	def ACHScroll(self, event):
		self.achvalue.SetValue(str(self.ach.GetValue()/10.0))
		self.inppb.SetLabel(str(eqsteady(float(self.outppb.GetValue()), self.ach.GetValue()/10.0, 45.0, 0, 68.85))+' ppb')
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
			self.inppb.SetLabel(str(eqsteady(float(self.outppb.GetValue()), self.ach.GetValue()/10.0, 45.0, 0, 68.85))+' ppb')
			self.statusbar.SetStatusText('')
		except ValueError:
			self.statusbar.SetStatusText('ValueError! Please input a number in (0,20)...')

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
