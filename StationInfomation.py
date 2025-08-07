# @作者：CodeW
# @功能：获取车票信息
import requests
import fake_useragent
import re
import json
import datetime
class StationInfo(): #括号内可以继承其他对象属性
    def __init__(self):
        self.headers = {
            'User-Agent':fake_useragent.UserAgent(platforms='pc').random
        }
        self.station_info = {
            'station_name': [],
            'station_code': []
        }
        self.ticket_info_sum = {}    #车票信息汇总
    def GetStationCode(self,from_station,to_station):
        self.station_info = {
            'station_name': [],
            'station_code': []
        }
        #获取车站代码
        url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
        station_name_original = requests.get(url=url,headers=self.headers)
        #分割每个站点的代码

        for i in re.finditer(r'@[^@]+',station_name_original.text):
            temp_info = re.findall(r'\|[^|]+',i.group())    #分割单个车站的各种代码
            temp_info[0] = temp_info[0].replace('|','')
            temp_info[1] = temp_info[1].replace('|','')
            self.station_info['station_name'].append(temp_info[0])
            self.station_info['station_code'].append(temp_info[1])
        if from_station not in self.station_info['station_name'] or to_station not in self.station_info['station_name']: return 'NoStation'
        return self.station_info['station_code'][self.station_info['station_name'].index(from_station)],self.station_info['station_code'][self.station_info['station_name'].index(to_station)]
    def TicketQuery(self,from_station_code,to_station_code,date): #date: YYYY-MM-DD
        #车票信息查询
        trips_count = 0   #车次趟数
        ticket_info = {   #车票信息
                'train_code' : '',#车次信息
                'start_station_code':'',#始发站代码
                'end_station_code':'',#终点站代码
                'from_station_code':'',#出发地站代码
                'to_station_code':'',#目的地站代码
                'start_time':'',#出发时间
                'arrive_time':'',#到达时间
                'time_consuming':'',#历时
                'prefer_first_seat' : 0, #优选一等座
                'senior_soft_sleeper':0,#高级软卧
                'other':0 ,#其他
                'soft_sleeper':0,#软卧
                'soft_seat':0,#软座
                'special_seat':0,#特等座
                'no_seat':0,#无座
                'one_person_soft':0,#一人软包
                'hard_sleeper':0,#硬卧
                'hard_seat':0,#硬座
                'second_seat':0,#二等座
                'first_seat':0,#一等座
                'business_seat':0,#商务座
                'three_person_soft':0,#三人软包
        }
        url = 'https://kyfw.12306.cn/otn/leftTicket/queryU?leftTicketDTO.train_date='+ date + '&leftTicketDTO.from_station=' + from_station_code + '&leftTicketDTO.to_station=' + to_station_code +'&purpose_codes=ADULT'
        cookies = {
            'JSESSIONID':''
        }
        real_time = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        allow_time = datetime.date.today() + datetime.timedelta(days=15)
        if(real_time > allow_time or real_time < allow_time - datetime.timedelta(days=15)):
            return 'WrongTime'#限制查询时间为十五天内
        ticket_text = json.loads(requests.get(url,headers=self.headers,cookies=cookies).text)
        if not ticket_text['status']:
            return 'QueryFail'    #获取余票失败
        for i in ticket_text['data']['result']:
            j = i.split(sep='|')
            ticket_info['train_code'] = j[3]
            ticket_info['start_station_code'] = j[4]
            ticket_info['end_station_code'] = j[5]
            ticket_info['from_station_code'] = j[6]
            ticket_info['to_station_code'] = j[7]
            ticket_info['start_time'] = j[8]
            ticket_info['arrive_time'] = j[9]
            ticket_info['time_consuming'] = j[10]
            ticket_info['prefer_first_seat'] = j[20] if j[20] else '--'
            ticket_info['senior_soft_sleeper'] = j[21] if j[21] else '--'
            ticket_info['other'] = j[22] if j[22] else '--'
            ticket_info['soft_sleeper'] = j[23] if j[23] else '--'
            ticket_info['soft_seat'] = j[24] if j[24] else '--'
            ticket_info['special_seat'] = j[25] if j[25] else '--'
            ticket_info['no_seat'] = j[26] if j[26] else '--'
            ticket_info['one_person_soft'] = j[27] if j[27] else '--'
            ticket_info['hard_sleeper'] = j[28] if j[28] else '--'
            ticket_info['hard_seat'] = j[29] if j[29] else '--'
            ticket_info['second_seat'] = j[30] if j[30] else '--'
            ticket_info['first_seat'] = j[31] if j[31] else '--'
            ticket_info['business_seat'] = j[32] if j[32] else '--'
            ticket_info['three_person_soft'] = j[33] if j[33] else '--'
            self.ticket_info_sum[trips_count] = ticket_info.copy()
            trips_count += 1
        return self.ticket_info_sum
