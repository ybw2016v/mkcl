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
        获取在一段时间内所有的帖子id列表
        """
        self.dogdb.execute(
            """select id from note where  %s = any("fileIds");""", [dogid])
        dogres = self.dogdb.fetchall()
        return len(dogres)



