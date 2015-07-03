# -*- coding: utf8 -*-
"""
 Copyright (C) 2008-2013 NURIGO
 http://www.coolsms.co.kr
"""

__version__ = "1.0beta"

import gui,math
import coolsms

class smsui:
	mtype = 'sms'
	imgfile = None
	page = 1
	total_page = 1
	test = False

	def __get_api__(self):
		api_key, api_secret = self.get_credential()
		return  coolsms.rest(api_key, api_secret, srk=None, test=self.test)

	def __get_balance__(self):
		r = self.__get_api__()
		return r.balance()

	def load(self, evt):
		cash, point = self.__get_balance__()
		mywin['statusbar'].text = "cash : %u, point : %u" % (cash, point)
		return

	def get_credential(self):
		api_key = str(mywin['notebook']['tab_setup']['api_key'].value)
		api_secret = str(mywin['notebook']['tab_setup']['api_secret'].value)
		return api_key, api_secret

	def send_message(self, evt):
		to = mywin['notebook']['tab_message']['to'].value
		sender = mywin['notebook']['tab_message']['from'].value
		message = mywin['notebook']['tab_message']['message'].value
		r = self.__get_api__()
		r.set_type(self.mtype)
		if self.mtype == 'mms':
			r.set_image(self.imgfile)
		status = r.send(to, message, sender)
		if status == False:
			mywin['statusbar'].text = r.get_error()
			gui.alert(r.get_error())
			return

		if int(status['error_count']) > 0:
			gui.alert("%u 개의 메시지에 오류가 발생했습니다." % int(status['error_count']))
		else:
			gui.alert("Sent!")

		print status['result_message']
		mywin['statusbar'].text = status['result_message'].encode('utf-8')

	def close_window(self, evt):
		exit()

	def test_mode(self, evt):
		if evt.target.value:
			self.test = True
		else:
			self.test = False

	def choose_type(self, evt):
		if evt.target.name == 'sms':
			self.mtype = 'sms'
		if evt.target.name == 'lms':
			self.mtype = 'lms'
		if evt.target.name == 'mms':
			self.mtype = 'mms'

	def choose_image(self, evt):
		self.imgfile = gui.open_file("select the file")
		print self.imgfile
		mywin['notebook']['tab_message']['filename'].value = self.imgfile

	def refresh_prev(self, evt):
		if self.page <= 1:
			return
		self.page = self.page - 1
		self.refresh_status(evt)

	def refresh_next(self, evt):
		if self.page > self.total_page:
			return
		self.page = self.page + 1
		self.refresh_status(evt)

	def refresh_status(self, evt):
		r = self.__get_api__()
		status = r.status(page=self.page, count=29)
		print status
		data = status['data']
		total_count = status['total_count']
		list_count = status['list_count']
		page = int(status['page'])
		self.total_page = math.ceil(int(total_count) / int(list_count) + 1)

		mywin['notebook']['tab_list']['label_page'].text = 'Page : %u/%u' % (page, self.total_page)
		mywin['notebook']['tab_list']['listview'].items = []
		for item in data:
			print "item\n"
			print item
			mywin['notebook']['tab_list']['listview'].items[item['message_id']] = {
				'col_accepted_time':item['accepted_time']
				, 'col_callno':item['recipient_number']
				, 'col_text':item['text']
				, 'col_status':item['status']
				, 'col_resultcode':item['result_code']
				, 'col_resultmessage':item['result_message']
				, 'col_sent_time':item['sent_time']
			}
		#for item in mywin['notebook']['tab_list']['listview'].items:
		#	print item
		#	print item['col_mid']
		#	status = r.status(item['col_mid'])
		#	print status
		#	item['col_status'] = status['result_code']

	def get_balance(self, evt):
		cash, point = self.__get_balance__()
		gui.alert('cash : %u, point : %u' % (cash, point))

ui = smsui()

gui.Window(name='mywin', title='COOLSMS Messaging'
		, resizable=True, height='420px'
		, left='180', top='24'
		, width='600px', bgcolor='#E0E0E0')

# menu
gui.MenuBar(name='menubar', fgcolor='#000000', parent='mywin')
gui.Menu(label='File', name='menu', fgcolor='#000000', parent='mywin.menubar')
gui.MenuItem(label='Quit', help='quit program', name='menu_quit', parent='mywin.menubar.menu')

# tab panel
gui.Notebook(name='notebook', height='211', left='10', top='10', width='590', parent='mywin', selection=0, )
gui.TabPanel(name='tab_setup', parent='mywin.notebook', selected=True, text='Setup')
gui.TabPanel(name='tab_message', parent='mywin.notebook', selected=True, text='Message')
gui.TabPanel(name='tab_list', parent='mywin.notebook', selected=True, text='List')

#### setup #####
# user_id
#gui.Label(name='label_userid', left='10', top='22', parent='mywin.notebook.tab_setup', text='User Id')
#gui.TextBox(name='user_id', left='80', top='22', width='150', parent='mywin.notebook.tab_setup', value='test')

# api_key
gui.Label(name='label_api_key', left='10', top='50', parent='mywin.notebook.tab_setup', text='API Key')
gui.TextBox(name='api_key', left='80', top='50', width='150', parent='mywin.notebook.tab_setup', value='NCS52A57F48C3D32')

# api_secret
gui.Label(name='label_secret', left='10', top='84', parent='mywin.notebook.tab_setup', text='API Secret')
gui.TextBox(name='api_secret', left='80', top='84', width='280', parent='mywin.notebook.tab_setup', value='5AC44E03CE8E7212D9D1AD9091FA9966')

# test mode
gui.CheckBox(label='Test Mode', name='test_mode', left='80', top='115', parent='mywin.notebook.tab_setup', onclick=ui.test_mode)

# balance info.
gui.Button(label='Balanece', name='balance', left='80', top='138', width='85', default=True, parent='mywin.notebook.tab_setup', onclick=ui.get_balance)

#### message #####
# type
gui.Label(name='label_type', left='10', top='22', parent='mywin.notebook.tab_message', text='Type')
gui.RadioButton(label='SMS', name='sms', left='80', top='22', parent='mywin.notebook.tab_message', value=True, onclick=ui.choose_type)
gui.RadioButton(label='LMS', name='lms', left='130', top='22', parent='mywin.notebook.tab_message', onclick=ui.choose_type)
gui.RadioButton(label='MMS', name='mms', left='180', top='22', parent='mywin.notebook.tab_message', onclick=ui.choose_type)

# to
gui.Label(name='label_to', left='10', top='50', parent='mywin.notebook.tab_message', text='To')
gui.TextBox(label='To ', name='to', left='80', top='50', width='150', parent='mywin.notebook.tab_message', value='01000000000')

# from
gui.Label(name='label_from', left='10', top='84', parent='mywin.notebook.tab_message', text='From')
gui.TextBox(name='from', left='80', top='84', width='150', parent='mywin.notebook.tab_message', value='01000000000')

# subject
gui.Label(name='label_subject', left='10', top='116', parent='mywin.notebook.tab_message', text='Subject')
gui.TextBox(name='subject', left='80', top='116', width='150', parent='mywin.notebook.tab_message', value='LMS MMS Subject')

# message
gui.Label(name='label_message', left='10', top='142', parent='mywin.notebook.tab_message', text='Message')
gui.TextBox(name='message', left='80', top='142', width='150', height='150', parent='mywin.notebook.tab_message', value=u'메시지를 입력하세요', multiline=True)

gui.Label(name='label_image', left='10', top='306', parent='mywin.notebook.tab_message', text='Image')
gui.Button(label='File', name='choose_image', left='80', top='300', width='85', default=True, parent='mywin.notebook.tab_message', onclick=ui.choose_image)
gui.TextBox(name='filename', left='166', top='301', parent='mywin.notebook.tab_message', value='')

# buttons
gui.Button(label='Send', name='send', left='80', top='326', width='85', default=True, parent='mywin.notebook.tab_message')
gui.StatusBar(name='statusbar', parent='mywin')

#### list ####
gui.Label(name='label_page', left='10', top='5', parent='mywin.notebook.tab_list', text='Page : 0/0')
gui.Button(label='Prev', name='prev', left='100', top='5', width='85', default=True, parent='mywin.notebook.tab_list', onclick=ui.refresh_prev)
gui.Button(label='Next', name='next', left='190', top='5', width='85', default=True, parent='mywin.notebook.tab_list', onclick=ui.refresh_next)
gui.Button(label='Refresh', name='refresh', left='290', top='5', width='85', default=True, parent='mywin.notebook.tab_list', onclick=ui.refresh_status)
gui.ListView(name='listview', height='320', left='0', top='30', width='590', 
             item_count=27, parent='mywin.notebook.tab_list', sort_column=0, 
             onitemselected="print ('sel %s' % event.target.get_selected_items())", )
gui.ListColumn(name='col_accepted_time', text='Date', parent='listview', )
gui.ListColumn(name='col_callno', text='Phone Number', parent='listview', )
gui.ListColumn(name='col_status', text='Status', width=20, parent='listview', )
gui.ListColumn(name='col_resultcode', text='Result Code', width=26, parent='listview', )
gui.ListColumn(name='col_resultmessage', text='Result Message', parent='listview', )
gui.ListColumn(name='col_sent_time', text='Sent time', parent='listview', )
gui.ListColumn(name='col_text', text='Text', parent='listview', )

mywin = gui.get("mywin")

mywin.onload = ui.load
mywin['notebook']['tab_message']['send'].onclick = ui.send_message
mywin['menubar']['menu']['menu_quit'].onclick = ui.close_window

if __name__ == "__main__":
	mywin.show()
	mywin.title = "COOLSMS"
	mywin['statusbar'].text = "COOLSMS Status Bar"
	gui.main_loop()
