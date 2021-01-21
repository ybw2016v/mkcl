import yaml
import argparse
import time
from core import dogclean

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', metavar='PATH',help='Path to misskey configuration file', action='store', default='.config/default.yml')
parser.add_argument('-d', '--day', metavar='DAY',help='The days between now and the date when clear script stop cleaning', action='store', default=28, type=int)
parser.add_argument('-s', '--start', metavar='DATE',help='The days between now and the date when clear script stop cleaning', action='store', default='2021-01-01')
dogc = parser.parse_args()
dogday = time.localtime(time.time()-60*60*24*dogc.day)
erydog = str(time.strftime('%Y-%m-%d', dogday))
# print(dogc.config)
# print(erydog)
# print(dogc.start)
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
dog_redis_pass=dogy['redis']['pass']
dog_redis_db=dogy['redis']['db']

dogclean([dog_db_host,dog_db_port,dog_db_db,dog_db_user,dog_db_pass],[dog_redis_host,dog_redis_port,dog_redis_pass,dog_redis_db],dogc.start,erydog)
