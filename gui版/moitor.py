# @作者：CodeW
# @功能：
import wx.adv
import wx
import threading

import api
import time
import utlis
import json
from email_window import EmailFrame
class MonitorFrame(wx.Frame):
	def __init__(self,main):
		# 以主窗口为父窗口，避免子窗口成为独立进程
		super().__init__(main,title='余票监控', size=(600, 600), name='余票监控', style=541072896 & ~wx.RESIZE_BORDER)
		# 设置最大尺寸为相同值（固定大小）
		self.SetMaxSize((600, 600))
		# 1. 创建状态栏（默认1个字段）
		self.status_bar = self.CreateStatusBar()

		# 2. 设置状态栏文本（默认显示在第一个字段）
		self.status_bar.SetStatusText("就绪")  # 初始状态
		#创建一个菜单栏
		menubar = wx.MenuBar()
		self.SetMenuBar(menubar)
		#创建一个菜单
		menu = wx.Menu()
		#添加一个菜单栏项
		menubar.Append(menu,'功能')
		#添加一个菜单项
		menuitem_configedit = menu.Append(wx.ID_ANY,'编辑配置','编辑配置文件')
		menuitem_email = menu.Append(wx.ID_ANY, '邮箱推送', '编辑邮箱配置文件')
		self.Bind(wx.EVT_MENU,self.Config_Edit,menuitem_configedit)
		self.Bind(wx.EVT_MENU, self.Email_Edit, menuitem_email)

		self.启动窗口 = wx.Panel(self)
		self.Centre()
		self.编辑框1 = wx.TextCtrl(self.启动窗口, size=(600, 400), pos=(2, 0), value='', name='text',style=1073741872)
		编辑框1_字体 = wx.Font(10, 74, 90, 400, False, 'Microsoft YaHei UI', 28)
		self.编辑框1.SetFont(编辑框1_字体)
		self.退出监控 = wx.Button(self.启动窗口, size=(71, 35), pos=(12, 450), label='退出监控', name='button')
		退出监控_字体 = wx.Font(10, 74, 90, 400, False, 'Microsoft YaHei UI', 28)
		self.退出监控.SetFont(退出监控_字体)
		self.is_config_edit = False  # 是否在编辑标志
		self.t = threading.Thread(target=self.StartMonitor)
		self.t.setDaemon(True)  # 设为守护线程
		self.t.start()
		self.退出监控.Bind(wx.EVT_BUTTON, self.退出监控_按钮被单击)

	def Email_Edit(self,event):
		#编辑邮箱推送配置文件
		email_show = EmailFrame(self) # 创建子窗口实例，传入self作为父窗口
		email_show.Show()




	def Config_Edit(self, event):
		#编辑配置文件
		def 确认编辑_按钮被单击(event):
			#回调函数
			config_str = self.编辑框1.GetValue()
			try:
				config_str_temp = json.loads(config_str)
				config_str = TicketMonitor.WriteConfig(config_str_temp)
				self.编辑框1.SetEditable(False)  # 设为只读模式
				self.编辑框1.Clear()
				self.确认编辑.Hide()  # 隐藏按钮
				self.编辑框1.SetValue(monitor_temp)
				self.is_config_edit = False
			except json.JSONDecodeError:
				wx.MessageBox('错误的JSON格式！', '提示', style=wx.OK | wx.ICON_ERROR)
		self.is_config_edit = True #正在编辑标志
		TicketMonitor = utlis.TicketMonitor()	#实例化
		monitor_temp = self.编辑框1.GetValue()
		self.编辑框1.Clear()	#清空编辑框
		self.编辑框1.SetValue(json.dumps(TicketMonitor.ReadConfig(),indent=4,ensure_ascii=False))	#展示配置文件
		self.编辑框1.SetEditable(True)	#设为可编辑模式
		self.确认编辑 = wx.Button(self.启动窗口, size=(71, 35), pos=(12, 410), label='确认编辑', name='button')
		退出监控_字体 = wx.Font(10, 74, 90, 400, False, 'Microsoft YaHei UI', 28)
		self.确认编辑.Bind(wx.EVT_BUTTON, 确认编辑_按钮被单击)



	def 退出监控_按钮被单击(self, event):
		self.Close()
	def StartMonitor(self):
		print('子线程已开启')
		TicketMonitor = utlis.TicketMonitor()
		while 1:
			if not self.is_config_edit	:#是否在编辑标志
				monitor_str, interval_time= api.Monitor()
				email_config = TicketMonitor.ReadConfig()['notifications']
				email_send_text = ''
				for i in monitor_str:
					if monitor_str == 'WRONG_TIME':
						self.编辑框1.AppendText('仅支持查询十五天内的车票\n\n')
					elif monitor_str == 'QUERY_FAIL':
						self.编辑框1.AppendText('查询失败！\n\n')
					elif not monitor_str or monitor_str == 'NO_STATION':
						self.编辑框1.AppendText('未查询到车票\n\n')
					else:
						self.编辑框1.AppendText(i+''+'间隔时间:'+str(interval_time)+'min'+'\n\n')
						email_send_text = email_send_text+i+'\n'
				if email_config:
					if (not email_config['smtp_server']) or (not email_config['sender_email']) or (not email_config['sender_password']) or (not email_config['receiver_email']):
						self.编辑框1.AppendText('不推送至邮箱\n')
					else:
						e = api.EmailPush(email_config['smtp_server'],email_config['sender_email'],email_config['sender_password'],email_config['receiver_email'],email_send_text)
						if e != 'SEND_SUCCESS':
							self.编辑框1.AppendText(f"邮件发送失败: {e}\n")
						else:
							self.编辑框1.AppendText('邮件发送成功\n')
				else:
					self.编辑框1.AppendText('不推送至邮箱\n')
				time.sleep(interval_time * 60)
			else:
				continue



