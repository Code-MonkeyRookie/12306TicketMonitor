# @作者：CodeW
# @功能：主页面
import wx.adv
import wx
import api
import utlis
import time
import moitor
import os
class MainFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, title='12306余票监控系统', size=(860, 572),name='12306余票查询',style=541072960 & ~wx.RESIZE_BORDER)#禁用拖动边缘调节大小
		# 设置最大尺寸为相同值（固定大小）
		self.SetMaxSize((860, 572))
		self.启动窗口 = wx.Panel(self)
		self.Centre()
		self.出发地 = wx.TextCtrl(self.启动窗口,size=(161, 29),pos=(100, 0),value='',name='text',style=0)
		self.标签1 = wx.StaticText(self.启动窗口,size=(80, 24),pos=(1, 4),label='出发地',name='staticText',style=2321)
		标签1_字体 = wx.Font(11,74,90,400,False,'Microsoft YaHei UI',28)
		self.标签1.SetFont(标签1_字体)
		self.标签2 = wx.StaticText(self.启动窗口,size=(84, 20),pos=(282, 4),label='目的地',name='staticText',style=2321)
		标签2_字体 = wx.Font(11,74,90,400,False,'Microsoft YaHei UI',28)
		self.标签2.SetFont(标签2_字体)
		self.目的地 = wx.TextCtrl(self.启动窗口,size=(161, 29),pos=(380, 1),value='',name='text',style=0)
		self.日期框1 = wx.adv.DatePickerCtrl(self.启动窗口,size=(161, 29),pos=(636, 1),name='datectrl',style=2)
		self.标签3 = wx.StaticText(self.启动窗口,size=(64, 22),pos=(560, 4),label='日期',name='staticText',style=2321)
		标签3_字体 = wx.Font(11,74,90,400,False,'Microsoft YaHei UI',28)
		self.标签3.SetFont(标签3_字体)
		self.按钮1 = wx.Button(self.启动窗口, size=(82, 30), pos=(738, 35), label='查询', name='button')
		按钮1_字体 = wx.Font(11, 74, 90, 400, False, 'Microsoft YaHei UI', 28)
		self.按钮1.SetFont(按钮1_字体)
		self.按钮1.Bind(wx.EVT_BUTTON, self.按钮1_按钮被单击)
		self.按钮1.SetFont(按钮1_字体)
		self.车票信息 = wx.ListCtrl(self.启动窗口,size=(860, 340),pos=(0, 72),name='listCtrl',style=35)
		self.车票信息.AppendColumn('车次', 0,83)
		self.车票信息.AppendColumn('出发站', 0,70)
		self.车票信息.AppendColumn('到达站', 0,70)
		self.车票信息.AppendColumn('出发时间', 0,66)
		self.车票信息.AppendColumn('到达时间', 0,64)
		self.车票信息.AppendColumn('历时', 0,50)
		self.车票信息.AppendColumn('何时到达', 0,69)
		self.车票信息.AppendColumn('商务座', 0,55)
		self.车票信息.AppendColumn('一等座', 0,53)
		self.车票信息.AppendColumn('二等座', 0,57)
		self.车票信息.AppendColumn('软卧', 0,50)
		self.车票信息.AppendColumn('硬卧', 0,50)
		self.车票信息.AppendColumn('硬座', 0,50)
		self.车票信息.AppendColumn('无座', 0,50)
		self.车票信息.EnableCheckBoxes(True)
		车票信息_字体 = wx.Font(10,74,90,400,False,'Microsoft YaHei UI',28)
		self.车票信息.SetFont(车票信息_字体)
		self.按钮3 = wx.Button(self.启动窗口,size=(88, 34),pos=(9, 420),label='添加监控车次',name='button')
		按钮3_字体 = wx.Font(10,74,90,400,False,'Microsoft YaHei UI',28)
		self.按钮3.SetFont(按钮3_字体)
		self.按钮3.Bind(wx.EVT_BUTTON, self.按钮3_按钮被单击)
		self.余票监控按钮 = wx.Button(self.启动窗口, size=(88, 34), pos=(9, 460), label='启动余票监控', name='button')
		余票监控按钮_字体 = wx.Font(10, 74, 90, 400, False, 'Microsoft YaHei UI', 28)
		self.余票监控按钮.SetFont(余票监控按钮_字体)
		self.余票监控按钮.Bind(wx.EVT_BUTTON, self.余票监控按钮_按钮被单击)
		self.商务座 = wx.CheckBox(self.启动窗口, size=(55, 24), pos=(105, 426), name='check', label='商务座',style=16384)
		self.一等座 = wx.CheckBox(self.启动窗口, size=(55, 24), pos=(165, 426), name='check', label='一等座',style=16384)
		self.二等座 = wx.CheckBox(self.启动窗口, size=(55, 24), pos=(225, 426), name='check', label='二等座',style=16384)
		self.软卧 = wx.CheckBox(self.启动窗口, size=(55, 24), pos=(285, 426), name='check', label='软卧',style=16384)
		self.硬卧 = wx.CheckBox(self.启动窗口, size=(55, 24), pos=(345, 426), name='check', label='硬卧',style=16384)
		self.硬座 = wx.CheckBox(self.启动窗口, size=(55, 24), pos=(405, 426), name='check', label='硬座',style=16384)
		self.无座 = wx.CheckBox(self.启动窗口, size=(55, 24), pos=(465, 426), name='check', label='无座',style=16384)
		self.监控全程票 = wx.CheckBox(self.启动窗口, size=(82, 24), pos=(525, 426), name='check', label='监控全程票', style=16384)
	def 按钮1_按钮被单击(self,event):
		#查询按钮
		from_station = self.出发地.GetValue()
		to_station = self.目的地.GetValue()
		date = self.日期框1.GetValue().Format("%Y-%m-%d")	#解析为字符串格式
		if from_station and to_station:
			ticket_info = api.TicketQuery(from_station, to_station, date)
			Station = utlis.Station()
			station_info = Station.StationCode()
			if ticket_info == 'WRONG_TIME':
				wx.MessageBox('仅支持查询十五天内的车票', '提示', style=wx.OK | wx.ICON_INFORMATION)
			elif ticket_info == 'QUERY_FAIL':
				wx.MessageBox('查询失败！', '提示', style=wx.OK | wx.ICON_ERROR)
			elif not ticket_info or ticket_info == 'NO_STATION':
				wx.MessageBox('未查询到车票', '提示', style=wx.OK | wx.ICON_INFORMATION)
			else:
				ticket_info = sorted(ticket_info,key= lambda x:int(x['start_time'].replace(':','')),reverse=True)	#按时间排序
				self.车票信息.DeleteAllItems()
				for tic_temp in ticket_info:
					row_idx = self.车票信息.InsertItem(1,tic_temp['train_code']) #创建一行，并在该行第一列插入元素
					# 在该行第n列插入元素
					self.车票信息.SetItem(row_idx,1,station_info['station_name'][station_info['station_code'].index(tic_temp['from_station_code'])])
					self.车票信息.SetItem(row_idx, 2, station_info['station_name'][station_info['station_code'].index(tic_temp['to_station_code'])])
					self.车票信息.SetItem(row_idx,3,tic_temp['start_time'])
					self.车票信息.SetItem(row_idx, 4, tic_temp['arrive_time'])
					self.车票信息.SetItem(row_idx, 5, tic_temp['time_consuming'])
					self.车票信息.SetItem(row_idx,6,Station.WhenArrive(tic_temp))
					self.车票信息.SetItem(row_idx, 7, tic_temp['business_seat'])
					self.车票信息.SetItem(row_idx, 8, tic_temp['first_seat'])
					self.车票信息.SetItem(row_idx, 9, tic_temp['second_seat'])
					self.车票信息.SetItem(row_idx, 10, tic_temp['soft_sleeper'])
					self.车票信息.SetItem(row_idx, 11, tic_temp['hard_sleeper'])
					self.车票信息.SetItem(row_idx, 12, tic_temp['hard_seat'])
					self.车票信息.SetItem(row_idx, 13, tic_temp['no_seat'])
		else:
			#弹出弹窗
			wx.MessageBox('请输入车站！','提示', style=wx.OK | wx.ICON_ERROR)

	def 按钮3_按钮被单击(self, event):
		#余票监控按钮
		checked_items = []
		#返回列表项数
		item_count = self.车票信息.GetItemCount()
		#返回列表列数
		column_count = self.车票信息.GetColumnCount()
		for item in range(item_count):
			checkd_item = []
			if self.车票信息.IsItemChecked(item):
				#检测选中的项
				for column in range(column_count):
					checkd_item.append(self.车票信息.GetItemText(item,col=column))
				checked_items.append(checkd_item.copy())
		if not checked_items:
			wx.MessageBox('请选择要监控的车次！', '提示', style=wx.OK | wx.ICON_INFORMATION)
		else:
			seat = [] #需要监控的席别
			is_monitor_full_ticket = False	#是否监控全程票
			is_checked = False
			interval_time = 0
			if self.商务座.GetValue():
				seat.append('商务座')
			if self.一等座.GetValue():
				seat.append('一等座')
			if self.二等座.GetValue():
				seat.append('二等座')
			if self.软卧.GetValue():
				seat.append('软卧')
			if self.硬卧.GetValue():
				seat.append('硬卧')
			if self.硬座.GetValue():
				seat.append('硬座')
			if self.无座.GetValue():
				seat.append('无座')
			if self.监控全程票.GetValue():
				is_monitor_full_ticket = True
			if not seat:
				wx.MessageBox('请选择要监控的席别！', '提示', style=wx.OK | wx.ICON_INFORMATION)
				return 0
			if not os.path.exists('config.json'):  # 检测配置文件是否存在
				# 创建监控间隔输入对话框
				input_interval_time = wx.TextEntryDialog(self.启动窗口,'请输入监控间隔时间(min)：','输入')
				input_interval_time.ShowModal()		#显示输入框
				try:
					interval_time = int(input_interval_time.GetValue())
				except ValueError:
					wx.MessageBox('请输入数字！', '提示', style=wx.OK | wx.ICON_ERROR)
					return 0
				if interval_time <= 0:
					wx.MessageBox('请输入大于零的数字！', '提示', style=wx.OK | wx.ICON_ERROR)
					return 0
				date = self.日期框1.GetValue().Format("%Y-%m-%d")  # 解析为字符串格式
				api.MonitorConfigLoad(checked_items,seat,date,is_monitor_full_ticket,is_config_exist=False,interval_time=interval_time)
			else:
				date = self.日期框1.GetValue().Format("%Y-%m-%d")  # 解析为字符串格式
				api.MonitorConfigLoad(checked_items, seat,date, is_monitor_full_ticket, is_config_exist=True)

	def 余票监控按钮_按钮被单击(self,event):
		if os.path.exists('config.json'):  # 检测配置文件是否存在
			monitor_show = moitor.MonitorFrame(self)  # 创建子窗口实例，传入self作为父窗口
			monitor_show.Show()

		else:
			wx.MessageBox('请先添加要监控的车次！', '提示', style=wx.OK | wx.ICON_ERROR)
app = wx.App()	#创建实例
MainFrame = MainFrame() 	#创建窗口实例
MainFrame.Show()	#显示窗口
app.MainLoop()	#启动主循环