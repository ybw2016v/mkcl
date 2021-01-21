
class DogUser(object):
    """
    用户相关信息
    """

    IsLocalDog = False
    IsVipDog = False

    def __init__(self, dogdb, dogid):
        dogc = dogdb.cursor()
        dogc.execute(
            """select host ,"followersCount","followingCount" from public.user where id = %s """, [dogid])
        dogres = dogc.fetchall()[0]
        if dogres[0] is None:
            self.IsLocalDog = True
        if (dogres[1]+dogres[2]) > 0:
            self.IsVipDog = True
        self.dogres = dogres
        pass
