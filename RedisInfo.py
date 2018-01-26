#encoding=utf-8 
import ConfigParser  
import redis
import smtplib  
from email.mime.text import MIMEText  
cf = ConfigParser.ConfigParser()
cf.read('Config.conf')
host=cf.get('database', 'host')
port=cf.get('database', 'port')
password=cf.get('database', 'password')
# r= redis.Redis(host='10.10.10.12', port=6379,password='netsdl')
r= redis.Redis(host=host, port=port,password=password)
info=r.info(section='clients')
content=''
for key in info: 
  content+=key+':'+str(info[key])+'\n'  

host = 'smtp.netsdl.com'
port = 25
sender = cf.get('mail','sender')
pwd = cf.get('mail','pwd')
receiver = cf.get('mail','receive').split(',')
msg = MIMEText(content,_subtype='plain', _charset='UTF-8')
mailTitle='clients info'
msg['subject'] = mailTitle
msg['from'] = sender
msg['to'] = ",".join(receiver)
try:
  smtp = smtplib.SMTP(host, port)  # is ssl change to  SMTP_SSL
  smtp.login(sender, pwd)
  smtp.sendmail(sender, receiver, msg.as_string())
except smtplib.SMTPException,e:  
  print e 

