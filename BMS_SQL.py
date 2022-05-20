import pymysql
import pandas as pd

class connection():
    def __init__(self):
        f=open("./sql_config.conf",'r',encoding='UTF8')
        self.log=""
        self.wvbms_db = pymysql.connect(
            user=f.readline().strip(), 
            passwd=f.readline().strip(), 
            host=f.readline().strip(),
            port=3306,
            db=f.readline().strip(), 
            charset='utf8'
    )
    def print_log(self): #로그출력
        print(self.log)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def fee_upsert(self, room_num, date, period_start, period_end, rent_fee, water_fee, unpaid_fee, total_fee, pay_limit): #월세 SQL 업데이트
        try:
            self.sql="INSERT INTO WV_BMS.Rental_Fee (room_num, date, period_start, period_end, rent_fee, water_fee, unpaid_fee, total_fee, pay_limit) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}') ON DUPLICATE KEY UPDATE period_start='{2}', period_end='{3}', rent_fee='{4}', water_fee='{5}', unpaid_fee='{6}', total_fee='{7}', pay_limit='{8}'".format(room_num, date, period_start, period_end, rent_fee, water_fee, unpaid_fee, total_fee, pay_limit).replace("''","NULL")
            self.log = self.sql+"\t\t"
            self.cursor = self.wvbms_db.cursor(pymysql.cursors.DictCursor)
            self.cursor.execute(self.sql)
            self.wvbms_db.commit()
            self.log+="SUCCESS"
            self.print_log()

        except pymysql.err.DataError:
            self.log+="**DataError**"
            self.print_log()

        except pymysql.err.IntegrityError: 
            self.log+="IntegrityError"
            self.print_log()

        except KeyError:
            self.log+="**DuplicationError**"
            self.print_log()

        except pymysql.err.ProgrammingError:
            self.log+="**ProgrammingError**"
            self.print_log()
        
        except pymysql.err.OperationalError:
            self.log+="**OperationalError**"
            self.print_log()
    
    def fee_water_upsert(self, room_num, date, water_fee): #수도료 SQL 업데이트
        try:
            self.sql="INSERT INTO WV_BMS.Rental_Fee (room_num, date, water_fee) VALUES ('{0}', '{1}', '{2}') ON DUPLICATE KEY UPDATE water_fee='{2}'".format(room_num, date, water_fee).replace("''","NULL")
            self.log = self.sql+"\t\t"
            self.cursor = self.wvbms_db.cursor(pymysql.cursors.DictCursor)
            self.cursor.execute(self.sql)
            self.wvbms_db.commit()
            self.log+="SUCCESS"
            self.print_log()

        except pymysql.err.DataError:
            self.log+="**DataError**"
            self.print_log()

        except pymysql.err.IntegrityError: 
            self.log+="IntegrityError"
            self.print_log()

        except KeyError:
            self.log+="**DuplicationError**"
            self.print_log()

        except pymysql.err.ProgrammingError:
            self.log+="**ProgrammingError**"
            self.print_log()
        
        except pymysql.err.OperationalError:
            self.log+="**OperationalError**"
            self.print_log()

    def fee_delete(self, room_num, date):
        try:
            self.sql="DELETE FROM `WV_BMS`.`Rental_Fee` WHERE (`room_num` = '{0}') and (`date` = '{1}')".format(room_num, date).replace("''","NULL")
            self.log = self.sql+"\t\t"
            self.cursor = self.wvbms_db.cursor(pymysql.cursors.DictCursor)
            self.cursor.execute(self.sql)
            self.wvbms_db.commit()
            self.log+="SUCCESS"
            self.print_log()

        except pymysql.err.DataError:
            self.log+="**DataError**"
            self.print_log()

        except pymysql.err.IntegrityError: 
            self.log+="IntegrityError"
            self.print_log()

        except KeyError:
            self.log+="**DuplicationError**"
            self.print_log()

        except pymysql.err.ProgrammingError:
            self.log+="**ProgrammingError**"
            self.print_log()
        
        except pymysql.err.OperationalError:
            self.log+="**OperationalError**"
            self.print_log()
    

    def pay_update(self, room_num, date, paid_fee, paid_date, paid_method, paid_memo):
        try:
            self.sql="UPDATE WV_BMS.Rental_Fee SET paid_fee='{2}', paid_date='{3}', paid_method='{4}', paid_memo='{5}' WHERE room_num='{0}' AND date='{1}'".format(room_num, date, paid_fee, paid_date, paid_method, paid_memo).replace("''","NULL")
            self.log = self.sql+"\t\t"
            self.cursor = self.wvbms_db.cursor(pymysql.cursors.DictCursor)
            self.cursor.execute(self.sql)
            self.wvbms_db.commit()
            self.log+="SUCCESS"
            self.print_log()

 
        except pymysql.err.DataError:
            self.log+="**DataError**"
            self.print_log()

        except pymysql.err.IntegrityError: 
            self.log+="IntegrityError"
            self.print_log()

        except KeyError:
            self.log+="**DuplicationError**"
            self.print_log()

        except pymysql.err.ProgrammingError:
            self.log+="**ProgrammingError**"
            self.print_log()
        
        except pymysql.err.OperationalError:
            self.log+="**OperationalError**"
            self.print_log()
    
    def memo_update(self, room_num, date, memo):
        try:
            self.sql="UPDATE WV_BMS.Rental_Fee SET memo='{2}' WHERE room_num='{0}' AND date='{1}'".format(room_num, date, memo).replace("''","NULL")
            self.log = self.sql+"\t\t"
            self.cursor = self.wvbms_db.cursor(pymysql.cursors.DictCursor)
            self.cursor.execute(self.sql)
            self.wvbms_db.commit()
            self.log+="SUCCESS"
            self.print_log()

 
        except pymysql.err.DataError:
            self.log+="**DataError**"
            self.print_log()

        except pymysql.err.IntegrityError: 
            self.log+="IntegrityError"
            self.print_log()

        except KeyError:
            self.log+="**DuplicationError**"
            self.print_log()

        except pymysql.err.ProgrammingError:
            self.log+="**ProgrammingError**"
            self.print_log()

    def fee_select(self, room_num, date):   #월세 SQL 가져오기
        try:
            self.cursor = self.wvbms_db.cursor(pymysql.cursors.DictCursor)
            self.sql = "SELECT * FROM WV_BMS.Rental_Fee WHERE (room_num LIKE '%%%s%%' and date LIKE '%%%s%%')"%(room_num,date)
            self.log = self.sql+"\t\t"
            self.cursor.execute(self.sql)
            df=pd.DataFrame(self.cursor.fetchall()).fillna("")
            self.log+=("SUCCESS")
            self.print_log()
            print(df)
            return df
        except:
            self.log+="**Get Data Error**"
            self.print_log()
        
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def room_update(self, room_num, cont_date, name, phone, deposit, rent_fee, empty, lang):
        try:
            self.sql="UPDATE WV_BMS.ROOM_info SET cont_date='{1}', name='{2}', phone='{3}', deposit={4}, rent_fee={5}, empty={6}, language={7} WHERE room_num='{0}'".format(room_num, cont_date, name, phone, deposit, rent_fee, empty, lang).replace("''","NULL")
            self.log = self.sql+"\t\t"
            self.cursor = self.wvbms_db.cursor(pymysql.cursors.DictCursor)
            self.cursor.execute(self.sql)
            self.wvbms_db.commit()
            self.log+="SUCCESS"
            self.print_log()

 
        except pymysql.err.DataError:
            self.log+="**DataError**"
            self.print_log()

        except pymysql.err.IntegrityError: 
            self.log+="IntegrityError"
            self.print_log()

        except KeyError:
            self.log+="**DuplicationError**"
            self.print_log()

        except pymysql.err.ProgrammingError:
            self.log+="**ProgrammingError**"
            self.print_log()

    def room_select(self, room_num):
        try:
            self.cursor = self.wvbms_db.cursor(pymysql.cursors.DictCursor)
            self.sql = "SELECT * FROM WV_BMS.ROOM_info WHERE room_num LIKE '%s%%'"%(room_num)
            self.log = self.sql+"\t\t"
            self.cursor.execute(self.sql)
            df=pd.DataFrame(self.cursor.fetchall()).fillna("")
            self.log+="SUCCESS"
            self.print_log()
            print(df)
            return df
        except:
            self.log+="**Get Data Error**"
            self.print_log()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def water_room_upsert(self, date, room, water): #수도사용량 호실별 SQL 업데이트
        try:
            self.sql="INSERT INTO WV_BMS.Water_Fee (meas_date, r{1}) VALUES ('{0}', '{2}') ON DUPLICATE KEY UPDATE r{1}='{2}'".format(date, room, water).replace("''","NULL")
            self.log = self.sql+"\t\t"
            self.cursor = self.wvbms_db.cursor(pymysql.cursors.DictCursor)
            self.cursor.execute(self.sql)
            self.wvbms_db.commit()
            self.log+="SUCCESS"
            self.print_log()

        except pymysql.err.DataError:
            self.log+="**DataError**"
            self.print_log()

        except pymysql.err.IntegrityError: 
            self.log+="IntegrityError"
            self.print_log()

        except KeyError:
            self.log+="**DuplicationError**"
            self.print_log()

        except pymysql.err.ProgrammingError:
            self.log+="**ProgrammingError**"
            self.print_log()
        
        except pymysql.err.OperationalError:
            self.log+="**OperationalError**"
            self.print_log()

    def water_total_upsert(self, date, fee): #전체 수도사용량 SQL 업데이트
        try:
            self.sql="INSERT INTO WV_BMS.Water_Fee (meas_date, total_fee) VALUES ('{0}', '{1}') ON DUPLICATE KEY UPDATE total_fee='{1}'".format(date, fee).replace("''","NULL")
            self.log = self.sql+"\t\t"
            self.cursor = self.wvbms_db.cursor(pymysql.cursors.DictCursor)
            self.cursor.execute(self.sql)
            self.wvbms_db.commit()
            self.log+="SUCCESS"
            self.print_log()

        except pymysql.err.DataError:
            self.log+="**DataError**"
            self.print_log()

        except pymysql.err.IntegrityError: 
            self.log+="IntegrityError"
            self.print_log()

        except KeyError:
            self.log+="**DuplicationError**"
            self.print_log()

        except pymysql.err.ProgrammingError:
            self.log+="**ProgrammingError**"
            self.print_log()
        
        except pymysql.err.OperationalError:
            self.log+="**OperationalError**"
            self.print_log()

    def water_delete(self, date):
        try:
            self.sql="DELETE FROM `WV_BMS`.`Water_Fee` WHERE (`meas_date` = '{0}')".format(date).replace("''","NULL")
            self.log = self.sql+"\t\t"
            self.cursor = self.wvbms_db.cursor(pymysql.cursors.DictCursor)
            self.cursor.execute(self.sql)
            self.wvbms_db.commit()
            self.log+="SUCCESS"
            self.print_log()

        except pymysql.err.DataError:
            self.log+="**DataError**"
            self.print_log()

        except pymysql.err.IntegrityError: 
            self.log+="IntegrityError"
            self.print_log()

        except KeyError:
            self.log+="**DuplicationError**"
            self.print_log()

        except pymysql.err.ProgrammingError:
            self.log+="**ProgrammingError**"
            self.print_log()
        
        except pymysql.err.OperationalError:
            self.log+="**OperationalError**"
            self.print_log()

    def water_select(self, date):
        try:
            self.cursor = self.wvbms_db.cursor(pymysql.cursors.DictCursor)
            self.sql = "SELECT * FROM WV_BMS.Water_Fee WHERE meas_date = '%s'"%(date)
            self.log = self.sql+"\t\t"
            self.cursor.execute(self.sql)
            df=pd.DataFrame(self.cursor.fetchall()).fillna("")
            self.log+="SUCCESS"
            self.print_log()
            print(df)
            return df
        except:
            self.log+="**Get Data Error**"
            self.print_log()
    
    def water_select_thismonth(self, date): #이번 달중 가장 빠른 수도데이터
        try:
            self.cursor = self.wvbms_db.cursor(pymysql.cursors.DictCursor)
            self.sql = "SELECT * FROM WV_BMS.Water_Fee WHERE meas_date BETWEEN date_format(LAST_DAY('{0}'), '%Y-%m-01') and LAST_DAY('{0}') ORDER BY meas_date desc LIMIT 1".format(date)
            self.log = self.sql+"\t\t"
            self.cursor.execute(self.sql)
            df=pd.DataFrame(self.cursor.fetchall()).fillna("")
            self.log+="SUCCESS"
            self.print_log()
            print(df)
            return df
        except:
            self.log+="**Get Data Error**"
            self.print_log()


    def water_select_lastmonth(self, date): #지난 달중 가장 빠른 수도데이터
        try:
            self.cursor = self.wvbms_db.cursor(pymysql.cursors.DictCursor)
            self.sql = "SELECT * FROM WV_BMS.Water_Fee WHERE meas_date <= LAST_DAY(date_sub('%s',INTERVAL 1 month)) ORDER BY meas_date desc LIMIT 1"%(date)
            self.log = self.sql+"\t\t"
            self.cursor.execute(self.sql)
            df=pd.DataFrame(self.cursor.fetchall()).fillna("")
            self.log+="SUCCESS"
            self.print_log()
            print(df)
            return df
        except:
            self.log+="**Get Data Error**"
            self.print_log()


"""menu=int(input("기능: "))
if menu==1:    connection().fee_upsert(input("room_num: "),input("date: "),input("period_start: "),input("period_end: "),input("rent_fee: "),input("water_fee: "),input("unpaid_fee: "),input("total_fee: "),input("pay_limit: "))
elif menu==2:  connection().fee_select(input("room_num: "),input("date: "))
elif menu==3:  connection().pay_update(input("room_num: "),input("date: "),input("paid_fee: "),input("paid_date: "),input("paid_method: "),input("paid_memo: "))
elif menu==4:  connection().memo_update(input("room_num: "),input("date: "),input("memo: "))
elif menu==5:  connection().room_update(input("room_num: "),input("cont_date: "),input("name: "),input("phone: "),input("deposit: "),input("rent_fee: "),False)
elif menu==6:  connection().room_select(input("room_num: "))
elif menu==7:  connection().water_room_upsert(input("date: "),input("room: "),input("water: "))
elif menu==8:  connection().water_delete(input("date: "))
elif menu==9:  connection().water_select(input("date: "))
elif menu==10:  connection().water_select_thismonth(input("date: "))
elif menu==11:  connection().water_select_lastmonth(input("date: "))"""