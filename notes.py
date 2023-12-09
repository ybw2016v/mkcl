from aix import genid
import time

class DogNotes(object):
    """
    类与对象
    """

    def __init__(self, dogdbc):
        """
        数据库游标卡尺初始化
        """
        self.dogdb = dogdbc.cursor()

    def get_dognotes_list(self, startdog, enddog):
        """
        获取在一段时间内所有的帖子id列表
        """
        stid = genid(int(startdog.timestamp()*1000))
        edid = genid(int(enddog.timestamp()*1000)) #enddog.
        self.dogdb.execute(
            """select id from note where "id" < %s and "id" > %s;""", [edid, stid])
        dogres = self.dogdb.fetchall()
        pdogres = list(map(lambda x: x[0], dogres))
        return pdogres

    def get_dognote_info(self, dogid):
        """
        获取单个帖子的相关信息
        """
        dogfleg=False
        self.dogdb.execute("""select "userId","userHost",mentions,"renoteId","replyId","fileIds","hasPoll" from note where "id" = %s""", [dogid])
        ooui=self.dogdb.fetchall()
        if len(ooui)==0:
            return 'error'
        else:
            dogres = {"id":dogid,"userId":ooui[0][0],"host":ooui[0][1],"mentions":ooui[0][2],"renoteId":ooui[0][3],"replyId":ooui[0][4],"fileIds":ooui[0][5],"hasPoll":ooui[0][6]}

            self.dogdb.execute(
                """select id from note_reaction where "noteId" = %s""", [dogid])
            dogres2a = self.dogdb.fetchall()
            if len(dogres2a)!=0:
                dogfleg=True
            self.dogdb.execute(
                """select id from note_favorite where "noteId" = %s""", [dogid])
            dogres2a = self.dogdb.fetchall()
            if len(dogres2a)!=0:
                dogfleg=True
            self.dogdb.execute(
                """select id from clip_note where "noteId" = %s""", [dogid])
            dogres2a = self.dogdb.fetchall()
            if len(dogres2a)!=0:
                dogfleg=True
            
            self.dogdb.execute(
                """select id from note_unread where "noteId" = %s""", [dogid])
            dogres2a = self.dogdb.fetchall()
            if len(dogres2a)!=0:
                dogfleg=True
            self.dogdb.execute(
                """select id from note_watching where "noteId" = %s""", [dogid])
            dogres2a = self.dogdb.fetchall()
            if len(dogres2a)!=0:
                dogfleg=True
            self.dogdb.execute(
                """select id from note_reaction where "noteId" = %s""", [dogid])
            dogres2a = self.dogdb.fetchall()
            if len(dogres2a)!=0:
                dogfleg=True
            dogres["dogfleg"]=dogfleg
            return dogres

    def get_dognote_beinfo(self, dogid):
        """
        获得被引用的列表
        """
        self.dogdb.execute(
            """select id from note where "renoteId" = %s or "replyId" = %s """, [dogid, dogid])
        dogres = self.dogdb.fetchall()
        sdog = map(lambda x: x[0], dogres)
        return list(sdog)

    def is_dognote_pin(self, dogid):
        """
        查询帖子是否被置顶
        """
        self.dogdb.execute(
            """select id from user_note_pining where "noteId" = %s """, [dogid])
        dogres = self.dogdb.fetchall()
        if len(dogres) == 0:
            return False
        else:
            return True

    def get_alldog_notes(self, idlist, hudog=[], ndog=0):
        """
        一个递归函数
        """
        skidog = {}
        # sxhdog = []
        zhidog = []
        for did in idlist:
            # if did in hudog:
                # print('error {}重复'.format(did))
            # else:
            lindog = self.get_dognote_info(did)
            if lindog=='error':
                print('出现错误 id {}'.format(did))
            else:
                skidog[did] = lindog
                if lindog["renoteId"] is not None:
                    zhidog.append(lindog["renoteId"])
                if lindog["replyId"] is not None:
                    zhidog.append(lindog["replyId"])
            beidog = self.get_dognote_beinfo(did)
            zhidog = zhidog+beidog
        # print('循环完成')
        zhidog = list(set(zhidog))
        # print('zhidog:{}'.format(zhidog))
        # print(hudog)
        zhidog2=[]
        for idog in zhidog:
            if idog not in hudog:
                # print('重复 {}'.format(idog))
                zhidog2.append(idog)
        # print(idlist)
        ppodog = hudog+idlist
        ppodog = list(set(ppodog))
        # print(ppodog)
        # print('zhidog:{}'.format(zhidog))
        # print('***********')
        # dfg=input()
        if zhidog2 == []:
            skiidog = {}
        else:
            skiidog = self.get_alldog_notes(zhidog2, ppodog, ndog)
        resdog = dict(skidog, **skiidog)
        return resdog
    pass


class DelDog(object):
    """
    删除类
    """
    def __init__(self,dogdb):
        """
        初始化
        """
        self.dogdb=dogdb
        self.dogcr=dogdb.cursor()

    def del_dog_note(self,dogid):
        """
        进行删除操作
        """
        self.dogcr.execute(
            """DELETE  from note where  "id" = %s """, [dogid])
        self.dogdb.commit()
    def del_dog_file(self,dogid):
        """
        进行删除操作
        """
        self.dogcr.execute(
            """DELETE  from drive_file where  "id" = %s """, [dogid])
        self.dogdb.commit()
    pass
