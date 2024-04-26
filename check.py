import requests
import json
import smtplib
import time
from email.mime.text import MIMEText
import argparse
import yaml


def load_config(config_file):
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    return config


def send_email(subject, message, sender_email, recipient_email, smtp_server, smtp_port, smtp_username, smtp_password):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.sendmail(sender_email, recipient_email, msg.as_string())
    server.quit()


def main(config):
    # 发送邮件的配置
    sender_email = config['email']['sender_email']
    recipient_email = config['email']['recipient_email']
    smtp_server = config['email']['smtp_server']
    smtp_port = config['email']['smtp_port']
    smtp_username = config['email']['smtp_username']
    smtp_password = config['email']['smtp_password']

    # 接口地址
    api_url = config['api']['url']

    # 设置cookies
    cookies = config['api']['cookies']
    headers = config['api']['headers']

    # 发起请求
    response = requests.get(api_url, cookies=cookies, headers=headers)
    data = response.json()

    # 检查dreviewList字段是否发生变化
    if data['status'] != 200:
        subject = '登录失败'
        send_email(subject, "", sender_email, recipient_email, smtp_server, smtp_port, smtp_username, smtp_password)
    else:
        dreview_list = data['body']['dstudentDissertation'][0]['dreviewList']
        # if len(dreview_list) != 0:
        # 发送邮件通知
        subject = '论文盲审结果更新'
        message = f'结果如下{dreview_list}，详情请登陆网页查看'
        send_email(subject, message, sender_email, recipient_email, smtp_server, smtp_port, smtp_username, smtp_password)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--conf', help='Path to the config file')
    args = parser.parse_args()

    config_file = args.conf
    config = load_config(config_file)
    main(config)