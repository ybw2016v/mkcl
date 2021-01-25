import psycopg2
import redis

import datetime
import pytz
from notes import DogNotes, DelDog
from users import DogUser


class DogR(object):
    """
    使用redis来数据库缓存查询
    """

    def __init__(self, dogdb, dogr):
        """
        初始化
        """
        self.dogdb = dogdb
        self.r = dogr

    def get_info(self, dogid):
        """
        docstring
        """
        doginfo = self.r.hget('dogs', dogid)
        if doginfo is not None:
            # print('命中缓存:{}-{}'.format(dogid,doginfo))
            if doginfo == 'True':
                return True
            else:
                return False
        else:
            udog = DogUser(self.dogdb, dogid)
            # print('未命中缓存:{}'.format(dogid))
            if udog.IsLocalDog or udog.IsVipDog:
                self.r.hset('dogs', dogid, 'True')
                return True
            else:
                self.r.hset('dogs', dogid, 'False')
                return False
    pass


def dogclean(dogdbi, dogri, dogs, doge):
    r = redis.Redis(host=dogri[0], port=dogri[1], db=dogri[3], password=dogri[2], decode_responses=True)
    pgdog = psycopg2.connect(
        database=dogdbi[2], user=dogdbi[3], password=dogdbi[4], host=dogdbi[0], port=dogdbi[1])
    stdog = datetime.datetime.strptime(
        dogs, '%Y-%m-%d').replace(tzinfo=pytz.timezone('UTC'))
    endog = datetime.datetime.strptime(
        doge, '%Y-%m-%d').replace(tzinfo=pytz.timezone('UTC'))
    idog = DogNotes(pgdog)
    sdf = idog.get_dognotes_list(stdog, endog)
    for sdi in sdf:
        if not idog.is_dognote_pin(sdi):
            r.sadd('doglist', sdi)
    dogn = r.srandmember('doglist')
    while dogn is not None:
        sdfp = str(dogn)
        sli = idog.get_alldog_notes([sdfp])
        dogf = False
        dog_id_lib = []
        dog_file_id = []
        dog_users_id = []
        for dogin, dogc in sli.items():
            dog_id_lib.append(dogin)
            dog_users_id.append(dogc[0])
            dog_file_id = dog_file_id+dogc[6]
            if dogc[7] or dogc[8]:
                dogf = dogf or True
            if dogc[5] > endog:
                dogf = dogf or True
                # print('超时:{}'.format(dogc))
                pass
        for udog in dog_users_id:
            dog_info = Dogr.get_info(udog)
            dogf = dogf or dog_info
        if not dogf:
            for sse in dog_id_lib:
                r.sadd('doglist2', sse)
                pass
            for ffd in dog_file_id:
                r.sadd('dogfile', ffd)
                pass
            pass
        for dogi in dog_id_lib:
            r.srem('doglist', dogi)
            pass
        dogn = r.srandmember('doglist')

    pass


r = redis.Redis(host='192.168.0.112', port=6379, db=3,
                password='', decode_responses=True)

pgdog = psycopg2.connect(database='misskey', user='misskey',
                         password='dogdogdog', host='192.168.0.112', port=20489)


idog = DogNotes(pgdog)
END_DATE = '2020-10-2'
START_DATE = '2020-09-20'

stdog = datetime.datetime.strptime(
    START_DATE, '%Y-%m-%d').replace(tzinfo=pytz.timezone('UTC'))
endog = datetime.datetime.strptime(
    END_DATE, '%Y-%m-%d').replace(tzinfo=pytz.timezone('UTC'))

# sdf = idog.get_dognotes_list('2020-10-1', '2020-10-2')
# for sdi in sdf:
#     print(idog.get_alldog_notes([sdi]))
# ossd = input()
# pass
# sd = DogUser(pgdog, '89fhzj179y')
# print(sd.dogres)
# print(sd.IsVipDog)
# print(sd.IsLocalDog)
# idog.get_alldog_notes(['8ctudkwg45'])

# qf=DogNotes(pgdog)
# qfs=qf.is_dognote_pin('8ct3s3rkma')
# print(qfs)

# idog = DogNotes(pgdog)
# sdf = idog.get_dognotes_list('2020-10-1', '2020-10-2')
# for sdi in sdf:
#     if not idog.is_dognote_pin(sdi):
#         r.sadd('doglist',sdi)
#     pass


dogn = r.srandmember('doglist')


Dogr = DogR(pgdog, r)


while dogn is not None:
    sdfp = str(dogn)
    # print(sdfp)
    sli = idog.get_alldog_notes([sdfp])
    dogf = False
    # print(sli)
    dog_id_lib = []
    dog_file_id = []
    dog_users_id = []
    for dogin, dogc in sli.items():
        dog_id_lib.append(dogin)
        dog_users_id.append(dogc[0])
        dog_file_id = dog_file_id+dogc[6]
        if dogc[7] or dogc[8]:
            dogf = dogf or True
            # print(dogc)
        if dogc[5] > endog:
            dogf = dogf or True
            print('超时:{}'.format(dogc))
            pass
    for udog in dog_users_id:
        # dog_info = DogUser(pgdog, udog)
        dog_info = Dogr.get_info(udog)
        # if dog_info.IsLocalDog or dog_info.IsVipDog:
        dogf = dogf or dog_info
    if not dogf:
        # print(dog_id_lib)
        for sse in dog_id_lib:
            r.sadd('doglist2', sse)
            pass
        for ffd in dog_file_id:
            r.sadd('dogfile', ffd)
            pass
        # print('以上应该删除')
        pass
    # sdp = input()
    for dogi in dog_id_lib:
        r.srem('doglist', dogi)
        pass
    dogn = r.srandmember('doglist')

    # pass
# sdpp=DogR(pgdog,r)
# print(sdpp.get_info('8cu3eul8uu'))

# deldog=DelDog(pgdog)
# deldog.del_dog_note('8ctcfdqweq')
# deldog.del_dog_file('8be5rgvftl')
