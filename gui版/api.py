# @作者：CodeW
# @功能：
import json
import datetime
import requests
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import traceback

import utlis
def TicketQuery(from_station,to_station,date):
    Station = utlis.Station()
    station_info = Station.StationCode()
    if from_station not in station_info['station_name'] or to_station not in station_info['station_name']: return 'NO_STATION'
    from_station_code = station_info['station_code'][station_info['station_name'].index(from_station)]
    to_station_code = station_info['station_code'][station_info['station_name'].index(to_station)]
    ticket_info = Station.TicketQuery(from_station_code,to_station_code,date)
    if ticket_info == 'WRONG_TIME':
        return 'WRONG_TIME'
    elif ticket_info == 'QUERY_FAIL':
        return 'QUERY_FAIL'
    else:
        return ticket_info
def MonitorConfigLoad(ticket_sum,seat,date,is_monitor_full_ticket,is_config_exist,interval_time = 0):
    '''

    ticket_sum[[车次，出发站，到达站，出发时间，到达时间，历时，何时到达，商务座，一等座，二等座，软卧，硬卧，硬座，无座],[.......],.....] 需要监控的车票信息
    seat[商务座，一等座，二等座，软卧，硬卧，硬座，无座] 需要监控的席别
    '''
    ticket_monitor = {
            'train': '',
            'start_station': '',
            'end_station': '',
            'from_station': '',
            'to_station': '',
            'date': '',
            'seat': [],
            'check_round_trip': '',  # 是否查询全程票

        }
    TicketMonitor = utlis.TicketMonitor()
    Station = utlis.Station()
    ticket_monitor_sum = []
    #整合车票信息
    for ticket in ticket_sum:
        ticket_monitor['start_station'],ticket_monitor['end_station'] = Station.TrainQuery(ticket[0],date)
        ticket_monitor['train'] = ticket[0]
        ticket_monitor['from_station'] = ticket[1]
        ticket_monitor['to_station'] = ticket[2]
        ticket_monitor['date'] = date
        ticket_monitor['seat'] = seat
        ticket_monitor['check_round_trip'] = is_monitor_full_ticket
        ticket_monitor_sum.append(ticket_monitor.copy())

    if is_config_exist:
        #增加监控车次
        config = TicketMonitor.ReadConfig()
        config['monitor_tic_info'].extend(ticket_monitor_sum)
        TicketMonitor.WriteConfig(config)
        return 'ADD_SUCCESS'
    else:
        TicketMonitor.CreatConfig(ticket_monitor_sum,interval_time)
        return 'CREATE_SUCCESS'

def Monitor():
    TicketMonitor = utlis.TicketMonitor()
    Station = utlis.Station()
    station_info = Station.StationCode()
    monitor_str = []    #存储每个车票的情况
    seat_name = {'商务座':'business_seat',
                 '一等座':'first_seat',
                 '二等座':'second_seat',
                 '软卧':'soft_sleeper',
                 '硬卧':'hard_sleeper',
                 '硬座':'hard_seat',
                 '无座':'no_seat'}
    config = TicketMonitor.ReadConfig()
    for ticket in config['monitor_tic_info']:
        time_temp = ''  #当前时间
        str_temp1 = []  #存储票的区间，全程数
        str_temp2 = ''  #即将加入monitor_str的字符串
        ticket_temp1 = Station.TicketQuery(station_info['station_code'][station_info['station_name'].index(ticket['from_station'])],station_info['station_code'][station_info['station_name'].index(ticket['to_station'])],date=ticket['date'])
        if ticket_temp1 == 'WRONG_TIME':
            monitor_str.append(ticket_temp1)
            continue
        elif ticket_temp1 == 'QUERY_FAIL':
            monitor_str.append(ticket_temp1)
            continue
        elif not ticket_temp1 or ticket_temp1 == 'NO_STATION':
            monitor_str.append('NO_STATION')
            continue
        for k in ticket_temp1:
            if k['train_code'].upper() == ticket['train'].upper():
                ticket_temp1 = k
                break
        if type(ticket_temp1) == list:
            monitor_str.append('NO_STATION')
            continue
        if ticket['check_round_trip']:
            ticket_temp2 = Station.TicketQuery(station_info['station_code'][station_info['station_name'].index(ticket['start_station'])],station_info['station_code'][station_info['station_name'].index(ticket['end_station'])],date=ticket['date'])
            if ticket_temp2 == 'WRONG_TIME':
                monitor_str.append(ticket_temp2)
                continue
            elif ticket_temp2 == 'QUERY_FAIL':
                monitor_str.append(ticket_temp2)
                continue
            elif not ticket_temp2 or ticket_temp2 == 'NO_STATION':
                monitor_str.append('NO_STATION')
                continue
            for k in ticket_temp2:
                if k['train_code'].upper() == ticket['train'].upper():
                    ticket_temp2 = k
                    break
            if type(ticket_temp2) == list:
                monitor_str.append('NO_STATION')
                continue
            time_temp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            str_temp2 = time_temp+' [Info] - '+ticket['train']+' '+ticket['from_station']+'→'+ticket['to_station']+' \n'
            for i in ticket['seat']:
                str_temp1.append(i+''+'[区间: '+ticket_temp1[seat_name[i]]+' 全程: '+ticket_temp2[seat_name[i]]+' ]\n')
            for j in str_temp1:
                str_temp2 = str_temp2+j
            monitor_str.append(str_temp2)
        else:
            time_temp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            str_temp2 = time_temp + ' [Info] - ' + ticket['train'] + ' ' + ticket['from_station'] + '→' + ticket['to_station'] + ' \n'
            for i in ticket['seat']:
                str_temp1.append(i + '' + '[区间: ' + ticket_temp1[seat_name[i]]+' ]\n')
            for j in str_temp1:
                str_temp2 = str_temp2 + j
            monitor_str.append(str_temp2)

    return monitor_str,config["interval_time"]
def EmailPush(smtp_server,sender_email,sender_password,receiver_email,text):
    '''
    邮件服务器配置（以QQ邮箱为例）
    smtp_server 'smtp.qq.com'  邮件服务器地址
    smtp_port  465  # SSL端口
    sender_email  'your_email@qq.com'  发件人邮箱
    sender_password 'your_auth_code'  邮箱授权码（非登录密码）

    收件人信息
    receiver_email  'recipient@example.com'  收件人邮箱
    subject 'Python发送邮件测试'  邮件主题
    text 发送内容
    '''
    smtp_port = 587     #STARTTLS 加密端口
    subject = '12306余票监控通知'
    message = MIMEText(text, 'plain', 'utf-8')
    message['From'] = sender_email # 发件人信息
    message['To'] = receiver_email # 收件人信息
    message['Subject'] = Header(subject, 'utf-8')  # 邮件主题
    try:
        # 连接邮件服务器并发送邮件
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # 2. 强制命令编码为utf-8，兼容非ASCII字符
            server.command_encoding = 'utf-8'
            # 3. 显式执行ehlo，确认主机名
            server.ehlo(name='localhost')
            server.starttls()  #升级为 TLS 加密
            # 5. 再次ehlo（部分服务器要求TLS后重新握手）
            #server.ehlo(name='localhost')
            server.login(sender_email, sender_password)  # 登录邮箱
            server.sendmail(sender_email, receiver_email, message.as_string())  # 发送邮件
            server.quit()   #发送 QUIT 命令，等待服务器响应后关闭会话
        return 'SEND_SUCCESS'
    except smtplib.SMTPException as e:
        traceback_str = traceback.format_exc()  # 打印异常跟踪回溯信息，有助于调试问题
        print("异常跟踪回溯信息：\n", traceback_str)
        return e