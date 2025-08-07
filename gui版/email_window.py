# @作者：CodeW
# @功能：
# -*- coding:utf-8 -*-
import wx
import wx.adv
import utlis
class EmailFrame(wx.Frame):
	def __init__(self,monitor):
		self.monitor = monitor
		super().__init__(monitor, title='邮箱推送', size=(400, 300),name='frame',style=541072960 & ~wx.RESIZE_BORDER)
		# 设置最大尺寸为相同值（固定大小）
		self.SetMaxSize((600, 600))
		self.启动窗口 = wx.Panel(self)
		self.Centre()
		self.邮箱服务器地址 = wx.StaticText(self.启动窗口,size=(261, 21),pos=(14, 15),label='邮箱服务器地址 smtp.example.com',name='staticText',style=2321)
		邮箱服务器地址_字体 = wx.Font(11,74,90,400,False,'Microsoft YaHei UI',28)
		self.邮箱服务器地址.SetFont(邮箱服务器地址_字体)
		self.server_address = wx.TextCtrl(self.启动窗口,size=(161, 22),pos=(17, 41),value='',name='text',style=0)
		server_address_字体 = wx.Font(11,74,90,400,False,'Microsoft YaHei UI',28)
		self.server_address.SetFont(server_address_字体)
		self.发件人邮箱地址 = wx.StaticText(self.启动窗口,size=(325, 27),pos=(8, 71),label='发件人邮箱地址 your_email@example.com',name='staticText',style=2321)
		发件人邮箱地址_字体 = wx.Font(11,74,90,400,False,'Microsoft YaHei UI',28)
		self.发件人邮箱地址.SetFont(发件人邮箱地址_字体)
		self.email_address = wx.TextCtrl(self.启动窗口,size=(161, 22),pos=(17, 96),value='',name='text',style=0)
		email_address_字体 = wx.Font(11,74,90,400,False,'Microsoft YaHei UI',28)
		self.email_address.SetFont(email_address_字体)
		self.标签3 = wx.StaticText(self.启动窗口,size=(325, 27),pos=(20, 126),label='邮箱授权码',name='staticText',style=17)
		标签3_字体 = wx.Font(11,74,90,400,False,'Microsoft YaHei UI',28)
		self.标签3.SetFont(标签3_字体)
		self.password = wx.TextCtrl(self.启动窗口,size=(161, 22),pos=(17, 151),value='',name='text',style=0)
		self.收件人邮箱 = wx.StaticText(self.启动窗口,size=(283, 21),pos=(20, 182),label='收件人邮箱 recipient@example.com',name='staticText',style=17)
		收件人邮箱_字体 = wx.Font(11,74,90,400,False,'Microsoft YaHei UI',28)
		self.收件人邮箱.SetFont(收件人邮箱_字体)
		self.recipient_email_address = wx.TextCtrl(self.启动窗口,size=(161, 22),pos=(17, 206),value='',name='text',style=0)
		recipient_email_address_字体 = wx.Font(11,74,90,400,False,'Microsoft YaHei UI',28)
		self.recipient_email_address.SetFont(recipient_email_address_字体)
		self.确定 = wx.Button(self.启动窗口, size=(54, 26), pos=(314, 221), label='确定', name='button')
		确定_字体 = wx.Font(11, 74, 90, 400, False, 'Microsoft YaHei UI', 28)
		self.确定.SetFont(确定_字体)
		self.确定.Bind(wx.EVT_BUTTON, self.确定_按钮被单击)

	def 确定_按钮被单击(self, event):
		TicketMonitor = utlis.TicketMonitor()
		email_config = {
			'smtp_server': '',
			'sender_email': '',
			'sender_password': '',
			'receiver_email': ''
		}
		email_config['smtp_server'] = self.server_address.GetValue()
		email_config['sender_email'] = self.email_address.GetValue()
		email_config['sender_password'] = self.password.GetValue()
		email_config['receiver_email'] = self.recipient_email_address.GetValue()
		config = TicketMonitor.ReadConfig()
		config['notifications'] = email_config
		TicketMonitor.WriteConfig(config)
		self.Close()