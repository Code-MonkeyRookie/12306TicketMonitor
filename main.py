# @作者：CodeW
# @功能：

import StationInfomation
import TicketMonitor
import datetime
import os
import re
import time
from colorama import Back,Fore,Style,init
def TicketMonitorPage():
      #余票监控选择页面
      while 1:
            print(Fore.LIGHTWHITE_EX+'1.查询车次并配置监控\n2.查看现有配置\n3.编辑现有配置\n4.直接启动监控\n5.退出程序\n')
            choice = int(input('请输入对应序号：'))
            os.system('cls')

            if choice == 1:

                  seat_code = ['business_seat','first_seat','second_seat','soft_sleeper','hard_sleeper','hard_seat','no_seat']
                  seat = []
                  interval_time = 0
                  from_station = input(Fore.LIGHTBLUE_EX + '请输入出发地：')
                  to_station = input(Fore.LIGHTBLUE_EX + '请输入目的地：')
                  if StationInfo.GetStationCode(from_station, to_station) == 'NoStation':
                        print('请重新输入正确的出发地或目的地!')
                        exit()
                  date = input(Fore.LIGHTBLUE_EX + '请输入出发日期(格式：YYYY-MM-DD)：')
                  if not re.match(r'\d{4}-[0-1][0-9]-[0-3][0-9]', date):
                        print('请正确输入时间格式!')
                        exit()
                  print(Fore.LIGHTMAGENTA_EX + '查询ing.....')
                  from_station_code, to_station_code = StationInfo.GetStationCode(from_station, to_station)
                  ticket_info_sum = StationInfo.TicketQuery(from_station_code, to_station_code, date)
                  if ticket_info_sum == 'WrongTime':
                        print('查询时间在十五天内，请重新输入')
                        exit()
                  time.sleep(1)
                  os.system('cls')
                  TicketInfoPage(ticket_info_sum)


                  train_code = input(Fore.LIGHTMAGENTA_EX+'请输入要监控的车次：').upper()
                  print('\n1.商务座\n2.一等座\n3.二等座\n4.软卧\n5.硬卧\n6.硬座\n7.无座')
                  seat_temp = str(input(Fore.LIGHTMAGENTA_EX+'请输入席别对应的序号(若要多选请用逗号,分隔数字)：')).split(sep=',')
                  for i in seat_temp:
                        if int(i) < 1 or int(i) > 7:
                              print('\n请重新输入1-4内的数字！')
                              exit()
                        else:
                              seat.append(seat_code[int(i)-1])
                  # 检查配置文件是否存在
                  if os.path.exists(TicketMonitor.config):
                        print('配置文件已存在，将自动追加待监控车次')
                        return_code = TicketMonitor.LoadTicketConfig(train_code,seat,date,True,ticket_info_sum,StationInfo.station_info)
                        if return_code == 'AddSuccess':print('追加监控车次成功')
                  else:
                        interval_time = input('\n请输入监控程序查询间隔时间(min)：')
                        return_code = TicketMonitor.LoadTicketConfig(train_code, seat, date, False,ticket_info_sum,StationInfo.station_info,interval_time=interval_time)
                        if return_code == 'CreateSuccess':print('创建配置文件成功')
                  time.sleep(1)
                  os.system('cls')


            elif choice == 2:
                  config_temp = TicketMonitor.ReadMonitorConfig()
                  if config_temp == 'NoneConfig':
                        print('配置文件不存在!')
                  else:
                        print('监控查询间隔时间：'+str(config_temp['interval_time'])+'min')
                        print('----------------------------------------------')
                        print('| 车次 | 始发站 | 终点站 | 出发地 | 目的地 | 车票日期 |  席别  | 查询全程票')
                        for con_temp in config_temp['monitor_tic_info']:
                              print('|'+con_temp['train']+' | '+con_temp['start_station']+' | '+con_temp['end_station']+' | '+con_temp['from_station']+' | '+con_temp['to_station']+' | '+con_temp['date']+' | '+','.join(con_temp['seat'])+' | '+str(con_temp['check_round_trip']))
                  input('\n按回车键返回.....')
                  os.system('cls')

            elif choice == 3:
                  ConfigEditPage()
                  time.sleep(1)
                  os.system('cls')
            elif choice == 4:
                  print('余票监控程序启动中.......')
                  time.sleep(1)
                  os.system('cls')
                  TicketMonitor.StartMonitor()
            elif choice == 5:
                  break
            else:
                  print('请重新输入1-5内的数字！')


def ConfigEditPage():
      #配置文件编辑界面
      print(Fore.LIGHTWHITE_EX + '1.删除车次配置\n2.更改配置文件\n3.返回上一页\n')
      choice = int(input('请输入对应序号：'))
      os.system('cls')
      if choice == 1:
            config_temp = TicketMonitor.ReadMonitorConfig()
            if config_temp == 'NoneConfig':
                  print('配置文件不存在!')
            else:
                  print('----------------------------------------------')
                  print('| 车次 | 始发站 | 终点站 | 出发地 | 目的地 | 车票日期 |  席别  | 查询全程票')
                  for con_temp in config_temp['monitor_tic_info']:
                        print('|' + con_temp['train'] + ' | ' + con_temp['start_station'] + ' | ' + con_temp[
                              'end_station'] + ' | ' + con_temp['from_station'] + ' | ' + con_temp['to_station'] + ' | ' +
                              con_temp['date'] + ' | ' + ','.join(con_temp['seat']) + ' | ' + str(con_temp['check_round_trip']))
                  train_temp = input('\n请输入要删除的车次：').upper()
                  TicketMonitor.DelMonitorConfig(train_temp)
                  print('删除成功!')


      elif choice == 2:
            print('暂时只支持监控查询间隔时间!')
            interval_time = input('\n请输入监控程序查询间隔时间(min)：')
            TicketMonitor.ChangeMonitorConfig(interval_time)

      elif choice == 3:
            os.system('cls')
      else:
            print('请重新输入1-3内的数字！')




def TicketInfoPage(ticket_info):
      # 车票信息展示页面

      print(Fore.LIGHTBLUE_EX + '-------------------------------------------------------------------------------------------------------------g')
      print(Fore.LIGHTBLUE_EX + ' 车次 | 出发站 | 到达站 | 出发时间 | 到达时间 | 历时 | 何时到达 | 商务座 | 一等座 | 二等座 | 软卧 | 硬卧 | 硬座 | 无座 |')
      for tic_info in ticket_info.values():
            # 判断几日到达
            start_time = tic_info['start_time'].split(':')
            time_consuming = tic_info['time_consuming'].split(':')
            arrive_temp = ''
            hour = int(start_time[0]) + int(time_consuming[0])
            minute = int(start_time[1]) + int(time_consuming[1])
            if minute >= 60:
                  hour += 1
            if hour >= 24 and hour < 48:
                  arrive_temp = '次日到达'
            elif hour >= 48 and hour < 72:
                  arrive_temp = '两日到达'
            elif hour >= 72:
                  arrive_temp = '三日到达'
            else:
                  arrive_temp = '当日到达'

            print(Fore.LIGHTWHITE_EX+' ' + tic_info['train_code'] + ' | ' + StationInfo.station_info['station_name'][
                  StationInfo.station_info['station_code'].index(tic_info['from_station_code'])] + ' | ' +
                  StationInfo.station_info['station_name'][
                        StationInfo.station_info['station_code'].index(tic_info['to_station_code'])] + ' | ' +
                  tic_info['start_time'] + ' | ' + tic_info['arrive_time'] + ' | ' + tic_info[
                        'time_consuming'] + ' | ' + arrive_temp + ' | ' + (
                        tic_info['special_seat'] if tic_info['business_seat'] == '--' else tic_info[
                              'business_seat'])  + ' | ' +  tic_info['first_seat'] +' | ' + tic_info[
                        'second_seat'] + ' | ' + tic_info['soft_sleeper'] + ' | ' + tic_info[
                        'hard_sleeper'] +  ' | ' + tic_info['hard_seat'] + ' | ' + tic_info[
                        'no_seat'] + ' | ' )




from_station_code = ''
to_station_code = ''
# 初始化：Windows 系统必须调用，自动处理终端兼容问题
# autoreset=True：自动重置样式（后续文本不受当前样式影响）
init(autoreset=True)
StationInfo = StationInfomation.StationInfo() #初始化
TicketMonitor = TicketMonitor.TicketMonitor()
print(Fore.LIGHTRED_EX+'---------------------------------------------------\n'
'                 12306余票监控系统                   \n'
'---------------------------------------------------')

input('\n按回车键继续....')
os.system('cls')
TicketMonitorPage()




