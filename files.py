from aix import genid

class DogFiles(object):
    """
    文件相关类
    """

    def __init__(self, dogdbc):
        """
        数据库游标卡尺初始化
        """
        self.dogdb = dogdbc.cursor()

    def get_dogfiles_n(self, dogid):
        """
        媒体文件引用数量
        """
        self.dogdb.execute("""select id from note where  %s = any("fileIds");""", [dogid])
        dogres = self.dogdb.fetchall()
        return len(dogres)

    def is_dogfile_local(self, dogid):
        """
        判断是否为本地存储文件
        """
        self.dogdb.execute("""select "isLink" from drive_file where  id = %s ;""", [dogid])
        dogres = self.dogdb.fetchall()
        return dogres[0][0]

    def get_sigle_files(self,startdog, enddog):
        """
        获取在一段时间内所有的帖子id列表
        """
        stid = genid(int(startdog.timestamp()*1000))
        edid = genid(int(enddog.timestamp()*1000)) #enddog.
        self.dogdb.execute(
            '''select drive_file."id" from drive_file 
LEFT join note 
on drive_file.id = any(note."fileIds")
LEFT join public.user 
on drive_file.id = public.user."avatarId" or drive_file.id = public.user."bannerId"
where drive_file."id" < %s and drive_file."id" > %s and drive_file."isLink" is true and drive_file."userHost" is not null and note."id" is null and public.user."id" is null''', [edid, stid])
        dogres = self.dogdb.fetchall()
        pdogres = list(map(lambda x: x[0], dogres))
        return pdogres
