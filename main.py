# -*- coding: utf8 -*-
import kivy
kivy.require('1.0.9')

from kivy.app import App
from kivy.properties import *
from kivy.base import EventLoop
from kivy.lang import Builder
from kivy.graphics import Color

from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.factory import Factory
from kivy.clock import Clock

from kivy.support import *
install_android()

import datetime,re,os,random, time, threading
import httplib, socket, urllib2, zipfile

gui = '''
# -*- coding: utf8 -*-
#:kivy 1.0

<installer>:
	BoxLayout:
		orientation: "vertical"
		Label:
			text: "Kite App Installer v  0.3"
		Button:
			text:"Install ressource manager App"
			on_press: app.process_button_click('https://github.com/microelly2/kivy-ressourcen/archive/master.zip')
		Button:
			text:"Install scheduler App"
			on_press: app.process_button_click('https://github.com/microelly2/kivy-stundenplan/archive/master.zip')
		Button:
			text:"Update the Installer"
			on_press: app.process_button_click('https://github.com/microelly2/kivy-installer/archive/master.zip')
		Button:
			text:"Purge Logs"
			on_release: self.text="clear cache, logs and temp data -- not impl. yet"

		Button:
			text:"Installation Status Info"
			on_release: self.text="Huhu, da kommt noch was"
		

<PopupBox>:
	pop_up_text: _pop_up_text
	size_hint: .9, .5
	auto_dismiss: True
	title: 'Status'   

	BoxLayout:
		orientation: "vertical"
		Label:
			id: _pop_up_text
			text: ''
'''



def unzip(zipFilePath, destDir):
	zfile = zipfile.ZipFile(zipFilePath)
	if not os.path.exists(destDir):
			os.mkdir(destDir)
	for name in zfile.namelist():
		print name
		(dirName, fileName) = os.path.split(name)
		newDir = destDir + '/' + dirName
		if not os.path.exists(newDir):
			os.mkdir(newDir)
		if not fileName == '':
			fd = open(destDir + '/' + name, 'wb')
			fd.write(zfile.read(name))
			fd.close()

class PopupBox(Popup):
	pop_up_text = ObjectProperty()
	def update_pop_up_text(self, p_message):
		self.pop_up_text.text = p_message

class installer(Screen):
	def __init__(self, **kwargs):
		super(installer, self).__init__(**kwargs)
	Builder.load_string(gui)

class installerApp(App):

	def build(self):
		c= installer(title='Hello world')
		c= ScreenManager()
		c.add_widget(installer(name='menu'))
		return c

	def show_popup(self):
		#self.pop_up = Factory.PopupBox()
		self.pop_up = PopupBox()
		self.pop_up.update_pop_up_text('Running some task...')
		self.pop_up.open()

	def process_button_click(self,source):
		self.show_popup()
		self.source=source
		mythread1 = threading.Thread(target=self.something_that_takes_5_seconds_to_run)
		mythread = threading.Thread(target=self.readZip)
		mythread1.start()
		mythread.start()

	def something_that_takes_5_seconds_to_run(self):
		thistime = time.time() 
		while thistime + 35 > time.time(): # 5 seconds
			self.pop_up.update_pop_up_text('running ' + '*' * int(time.time()-thistime))
			time.sleep(1)

	def readZip(self,but=None):
		self.pop_up.update_pop_up_text('get git ' + self.source + ' ...')
		try:
			response = urllib2.urlopen(self.source)
			zipcontent= response.read()
			with open("my.zip", 'w') as f:
				f.write(zipcontent)
			f.close()
		except:
			self.pop_up.update_pop_up_text('error getting the git')
			return
		self.pop_up.update_pop_up_text('unzip  ...')
		try:
			unzip("my.zip","..")
		except:
			self.pop_up.update_pop_up_text('error unzip')
			return
		self.pop_up.dismiss()


if __name__ == '__main__' and True:
	app=installerApp()
	app.run()
