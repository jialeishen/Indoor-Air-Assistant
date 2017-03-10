#-*-coding:utf-8-*-

import json  
import urllib2
import math
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class IPToLocation():
	def __init__(self):
		url = 'http://api.map.baidu.com/location/ip'
		ak = 'ak=mxjlvFkTekMbKtDbxdaP0TUZmWzfLyRk'
		coor = '&coor=bd09ll'
		url = url + '?' + ak + coor
		temp = urllib2.urlopen(url)  
		self.hjson = json.loads(temp.read()) 
	def city(self):
		c = self.hjson["content"]["address_detail"]["city"]
		c = str(c[:-1])
		return c
	def district(self):
		return self.hjson["content"]["address_detail"]["district"]
	def province(self):
		return self.hjson["content"]["address_detail"]["province"]
	def street(self):
		return self.hjson["content"]["address_detail"]["street"]
	def street_number(self):
		return self.hjson["content"]["address_detail"]["street_number"]
	def lng(self):
		return float(self.hjson["content"]["point"]["x"])
	def lat(self):
		return float(self.hjson["content"]["point"]["y"])
	def position(self):
		self.position = [self.lat(), self.lng()]
		return self.position

class GetAQI():
	def __init__(self, city):
		self.city = city
		url = 'http://www.pm25.in/api/querys/o3.json'
		city = 'city=' + self.city
		token = '&token=5j1znBVAsnSf5xQyNQyq'
		url = url + '?' + city + token
		temp = urllib2.urlopen(url)  
		self.hjson = json.loads(temp.read())
	def ozone(self):
		self.ozone = self.hjson[-1]["o3"]
		return self.ozone