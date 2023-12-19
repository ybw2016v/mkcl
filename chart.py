import time
import psycopg

def cleanchart(dogdbi,day):
    """
    删除指定天数前的chart数据
    """
    pgdog = psycopg.connect("dbname={} user={} password={} host={} port={}".format( dogdbi[2], dogdbi[3], dogdbi[4], dogdbi[0], dogdbi[1]))
    delchart(pgdog,day)
    pass

def delchart(db,day):
    """
    删除指定天数前的chart数据
    """
    cur = db.cursor()
    now = time.time()
    dtime = int(now - 60*60*24*day)
    # print(dtime)
    cur.execute("""DELETE  from __chart__hashtag where  "date" < %s """, [dtime])
    cur.execute("""DELETE  from __chart_day__hashtag where  "date" < %s """, [dtime])
    db.commit()
    cur.execute("""DELETE  from __chart__per_user_notes where  "date" < %s """, [dtime])
    cur.execute("""DELETE  from __chart_day__per_user_notes where  "date" < %s """, [dtime])
    db.commit()
    cur.execute("""DELETE  from __chart__instance where  "date" < %s """, [dtime])
    db.commit()
    pass

# delchart('127.0.0.1',30)