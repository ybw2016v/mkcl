import yaml
import argparse
import time
import datetime
from core import dogclean, dog_post

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', metavar='PATH',help='Path to misskey configuration file', action='store', default='.config/default.yml')
parser.add_argument('-d', '--day', metavar='DAY',help='The days between now and the date when clear script stop cleaning', action='store', default=28, type=int)
parser.add_argument('-s', '--start', metavar='DATE',help='The days between now and the date when clear script stop cleaning', action='store', default='2021-01-01')
parser.add_argument('-w', '--week', metavar='WEEK',help='Week Mode', action='store' ,type=int)
parser.add_argument('-m', '--month', metavar='MONTH',help='30 days Mode', action='store' ,type=int)
parser.add_argument('-n', '--nopost',help='No Post Mode', action='store_true')

dogc = parser.parse_args()

if dogc.week is not None:
    dogday = time.localtime(time.time()-60*60*24*7*dogc.week)
    erydog = str(time.strftime('%Y-%m-%d', dogday))
    startdog = time.localtime(time.time()-60*60*24*7*(dogc.week+1))
    sdog= str(time.strftime('%Y-%m-%d', startdog))
    pass

if dogc.month is not None:
    dogday = time.localtime(time.time()-60*60*24*30*dogc.month)
    erydog = str(time.strftime('%Y-%m-%d', dogday))
    startdog = time.localtime(time.time()-60*60*24*30*(dogc.week+1))
    sdog= str(time.strftime('%Y-%m-%d', startdog))
    pass
else:
    dogday = time.localtime(time.time()-60*60*24*dogc.day)
    erydog = str(time.strftime('%Y-%m-%d', dogday))
    sdog= dogc.start
dogfile=open(dogc.config)
dogy=yaml.load(dogfile)
dogfile.close()

dog_db_host=dogy['db']['host']
dog_db_port=dogy['db']['port']
dog_db_db=dogy['db']['db']
dog_db_user=dogy['db']['user']
dog_db_pass=dogy['db']['pass']

dog_redis_host=dogy['redis']['host']
dog_redis_port=dogy['redis']['port']
dog_redis_pass=dogy['redis']['pass'] if ('pass' in dogy['redis']) else None
dog_redis_db=dogy['redis']['db'] if ('db' in dogy['redis']) else None

dog_url=dogy['url']

a=datetime.datetime.now()
resdoggg=dogclean([dog_db_host,dog_db_port,dog_db_db,dog_db_user,dog_db_pass],[dog_redis_host,dog_redis_port,dog_redis_pass,dog_redis_db],sdog,erydog)
b=datetime.datetime.now()
d=b-a
strdogg='成功执行[冗余信息退出机制](https://github.com/ybw2016v/mkcl)\n清理范围:{}至{}\n{}\n用时{}s'.format(sdog,erydog,resdoggg,d.seconds)



if dogc.nopost is False:
    dog_post([dog_db_host,dog_db_port,dog_db_db,dog_db_user,dog_db_pass],dog_url,strdogg)
else:
    print(strdogg)
