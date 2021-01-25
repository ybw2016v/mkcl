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
