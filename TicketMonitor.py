# @作者：CodeW
# @功能：余票监控
import os
import json
import time
from itertools import count

import keyboard
import StationInfomation
class TicketMonitor():
    def __init__(self):
        self.StationInfo = StationInfomation.StationInfo()
        self.config = 'config.json'
        self.ticket_monitor_sum = {
            'monitor_tic_info': [],
            'interval_time':None, #监控间隔时间(min)
            'notifications':{
                
            }
        }
    def LoadTicketConfig(self,train_code,seat,date,is_config_exist,ticket_info_sum,station_info,interval_time = None,):
        #加载监控配置
        ticket_monitor = {
            'train': train_code,
            'start_station':'',
            'end_station':'',
            'from_station':'',
            'to_station':'',
            'date':date,
            'seat':seat,
            'check_round_trip':True, #是否查询全程票

        }

        for ticket_temp in range(len(ticket_info_sum)):
            if train_code == ticket_info_sum[ticket_temp]['train_code']:
                ticket_monitor['start_station'] = station_info['station_name'][station_info['station_code'].index(ticket_info_sum[ticket_temp]['start_station_code'])]
                ticket_monitor['end_station'] = station_info['station_name'][station_info['station_code'].index(ticket_info_sum[ticket_temp]['end_station_code'])]
                ticket_monitor['from_station'] = station_info['station_name'][station_info['station_code'].index(ticket_info_sum[ticket_temp]['from_station_code'])]
                ticket_monitor['to_station'] = station_info['station_name'][station_info['station_code'].index(ticket_info_sum[ticket_temp]['to_station_code'])]
        self.ticket_monitor_sum['monitor_tic_info'].append(ticket_monitor.copy())
        if is_config_exist:
            with open(self.config,'r+',encoding='utf-8') as fp:
                json_str = json.loads(fp.read())
                json_str['monitor_tic_info'].append(ticket_monitor)
                fp.seek(0) # 将文件指针移回开头
                fp.write(json.dumps(json_str, indent=4,ensure_ascii=False))
            return 'AddSuccess'

        else:
            self.ticket_monitor_sum['interval_time'] = int(interval_time)
            with open(self.config,'w',encoding='utf-8') as fp:
                json_str = json.dumps(self.ticket_monitor_sum,indent=4,ensure_ascii=False) #增加缩进
                fp.write(json_str)
            return 'CreateSuccess'
    def ReadMonitorConfig(self):
        if os.path.exists(self.config):
            with open(self.config,'r',encoding='utf-8') as fp:
                return json.loads(fp.read())
        else:
            return 'NoneConfig'
    def DelMonitorConfig(self,train):
        count = 0
        with open(self.config, 'r', encoding='utf-8') as fp:
            json_str = json.loads(fp.read())  # 增加缩进
            for json_str_temp in json_str['monitor_tic_info']:
                if json_str_temp['train'] == train:
                    break
                count += 1
            del json_str['monitor_tic_info'][count]
        with open(self.config, 'w', encoding='utf-8') as fp:
            fp.write(json.dumps(json_str, indent=4,ensure_ascii=False))
            return 'DelSuccess'
    def ChangeMonitorConfig(self,interval_time):
        config_temp = self.ReadMonitorConfig()
        if config_temp == 'NoneConfig':
            print('配置文件不存在!')
        else:
            config_temp['interval_time'] = int(interval_time)
            with open(self.config, 'w', encoding='utf-8') as fp:
                fp.write(json.dumps(config_temp, indent=4,ensure_ascii=False))
    def StartMonitor(self):
        def Exit():
            #回调函数
            # print('监控程序将于五秒退出...')
            time.sleep(5)
            exit()
        seat_name = {'business_seat':'商务座',
                     'first_seat':'一等座',
                     'second_seat':'二等座',
                     'soft_sleeper':'软卧',
                     'hard_sleeper':'硬卧',
                     'hard_seat':'硬座',
                     'no_seat':'无座'}
        config_temp = self.ReadMonitorConfig()
        if config_temp == 'NoneConfig':
            print('配置文件不存在!')
        else:
            need_monitor_station = {
                'from_station':[],
                'to_station':[]
            }
            self.StationInfo.GetStationCode(config_temp['monitor_tic_info'][0]['from_station'], config_temp['monitor_tic_info'][0]['to_station'])
            # 创建车站代码缓存
            for con_temp in config_temp['monitor_tic_info']:
                need_monitor_station['from_station'].append(self.StationInfo.station_info['station_code'][self.StationInfo.station_info['station_name'].index(con_temp['from_station'])])
                need_monitor_station['to_station'].append(self.StationInfo.station_info['station_code'][self.StationInfo.station_info['station_name'].index(con_temp['to_station'])])
            keyboard.add_hotkey('ctrl+c', Exit) #传入函数内存地址
            while True:
                for k in range(len(need_monitor_station['from_station'])):
                    ticket_info_sum = self.StationInfo.TicketQuery(need_monitor_station['from_station'][k], need_monitor_station['to_station'][k],config_temp['monitor_tic_info'][k]['date'])
                    for i in ticket_info_sum.values():
                        if config_temp['monitor_tic_info'][k]['train'] == i['train_code']:
                            print('车次：'+config_temp['monitor_tic_info'][k]['train']+'   ',end='')
                            for j in config_temp['monitor_tic_info'][k]['seat']:
                                print(seat_name[j]+'剩余：'+i[j])
                print('等待时间：'+str(int(config_temp['interval_time']))+'min')
                print('\n按下Ctrl+C可退出监控程序\n')
                time.sleep(int(config_temp['interval_time']) * 60)








