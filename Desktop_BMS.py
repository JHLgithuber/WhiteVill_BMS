from cProfile import label
from email.policy import default
from faulthandler import disable
from json import load
from optparse import Values
#import pyautogui as pg
import pandas as pd
import numpy as np
import random
import os
import tkinter.ttk
from tkinter import ttk
import tkinter as tk
from calendar import c
from distutils import command
from pickle import REDUCE
from sre_parse import State, expand_template
from tkinter import *
from tkinter import messagebox
from tkinter import Entry
import tkinter
#from tkinter.tix import *
from tkinter import filedialog
from turtle import bgcolor, color, left, right
#from typing_extensions import Self
from numpy import expand_dims, place, size
#from soupsieve import select
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import BMS_SQL as sql

room_num_list=[101,102,103,104,201,202,203,204,205,301,302,303,304,305]
language_list=["한국어","영어"]

#Making dataframe in auto----------------------------------------------------------------------------------------
def mkdf_water_autocarc(waterlastdf,waterthisdf):
    print("\n수도요금자동계산")
    print(waterlastdf)
    print(waterthisdf)

    waterdf=pd.concat([waterlastdf,waterthisdf],ignore_index=True)
    waterdf.index=['past','pre']
    waterdf.drop(['meas_date','total_fee'],axis=1,inplace=True)
    waterdf.loc['use']=waterdf.loc['pre']-waterdf.loc['past']
    waterdf['total']=waterdf.sum(axis=1)
    waterdf.loc['fee','total']=waterthisdf.iloc[0]['total_fee']
    print(waterdf)
    waterdf.loc['fee']=waterdf.loc['fee','total']/waterdf.loc['use','total']*waterdf.loc['use']
    waterdf.loc['floor']=(waterdf.loc['fee']/100).apply(np.floor)*100
    print(waterdf)
    waterdf.loc['floor','total']=None
    waterdf.loc['floor','r501']=0
    waterdf.loc['floor','total']=waterdf.loc['floor'].sum()
    print(waterdf)
    return waterdf

#수도-------------------------------------------------------------------------------------------------
class watermanage_class():  #수도계량관리
    global inquiry_date_water
    inquiry_date_water=datetime.today() + relativedelta(months=1)
    waterlist_dict={}

    class water_room():   #세대별 요금
        def __init__(self,page,room_num) -> None:
            self.page=page
            self.room_num=room_num

        def show_fee(self):
            self.frame=tkinter.Frame(self.page,relief='sunken',borderwidth=3)
            self.frame.pack(fill="both")
            self.button_room=tkinter.Button(self.frame, text=self.room_num+"호")
            self.button_room.pack(side=LEFT)
            self.label_past=tkinter.Label(self.frame, text="전월지침")
            self.label_past.pack(side=LEFT)
            self.entry_past=tkinter.Entry(self.frame, width=8, state='readonly')
            self.entry_past.pack(side=LEFT)
            self.label_pre=tkinter.Label(self.frame, text=" 당월지침")
            self.label_pre.pack(side=LEFT)
            self.entry_pre=tkinter.Entry(self.frame, width=8)
            self.entry_pre.pack(side=LEFT)
            self.label_use=tkinter.Label(self.frame, text=" 사용량")
            self.label_use.pack(side=LEFT)
            self.entry_use=tkinter.Entry(self.frame, width=8, state='readonly')
            self.entry_use.pack(side=LEFT)
            self.entry_payfee=tkinter.Entry(self.frame, width=8)
            self.entry_payfee.pack(side=RIGHT)
            self.label_payfee=tkinter.Label(self.frame, text=" 납부금액")
            self.label_payfee.pack(side=RIGHT)
            self.entry_usefee=tkinter.Entry(self.frame, width=8, state='readonly')
            self.entry_usefee.pack(side=RIGHT)
            self.label_usefee=tkinter.Label(self.frame, text="사용금액")
            self.label_usefee.pack(side=RIGHT)
    
    def watermanage_popup(self):    #수도관리
        self.watermanage=Tk()
        self.watermanage.title("수도지침관리")
        self.watermanage.geometry("650x650")
        self.select_frame=tkinter.Frame(self.watermanage)
        self.entry_year=tkinter.Entry(self.select_frame,width=6)
        self.entry_year.pack(side=LEFT)
        self.label_year=tkinter.Label(self.select_frame, text="년도 ")
        self.label_year.pack(side=LEFT)
        self.entry_month=tkinter.Entry(self.select_frame,width=4)
        self.entry_month.pack(side=LEFT)
        self.label_month=tkinter.Label(self.select_frame, text="월")
        self.label_month.pack(side=LEFT)
        self.button_inquiry=tkinter.Button(self.select_frame, text="조회", command=self.load_inquiry)
        self.button_inquiry.pack(side=LEFT)
        self.label_blank=tkinter.Label(self.select_frame,text="\t")
        self.label_blank.pack(side=LEFT)
        self.button_prev=tkinter.Button(self.select_frame, text="이전", width=10, command= self.load_prev)
        self.button_prev.pack(side=LEFT)
        self.button_next=tkinter.Button(self.select_frame, text="다음", width=10, command= self.load_next)
        self.button_next.pack(side=LEFT)
        self.button_alldel=tkinter.Button(self.select_frame, text="당월삭제", command=self.dele, bg='red')
        self.button_alldel.pack(side=RIGHT,padx=20)
        self.button_allsave=tkinter.Button(self.select_frame, text="저장", command=self.save)
        self.button_allsave.pack(side=RIGHT)
        self.button_allload=tkinter.Button(self.select_frame, text="불러오기", command=self.load)
        self.button_allload.pack(side=RIGHT)
        self.select_frame.pack(side=TOP, ipadx=30, ipady=10)

        self.label_gauge=tkinter.Label(self.watermanage,text="수도계량기 지침")
        self.label_gauge.pack(side=TOP,anchor=W)
                
        for room_num in room_num_list+[501]:
            self.waterlist_dict[room_num]=self.water_room(self.watermanage,str(room_num))
            self.waterlist_dict[room_num].show_fee()
        
        self.frame_date=tkinter.Frame(self.watermanage)
        self.label_lastdate=tkinter.Label(self.frame_date,text="전월검침일")
        self.label_lastdate.pack(side=LEFT)
        self.entry_lastdate=tkinter.Entry(self.frame_date,state='readonly',width=12)
        self.entry_lastdate.pack(side=LEFT)
        self.label_thisdate=tkinter.Label(self.frame_date,text=" 당월검침일")
        self.label_thisdate.pack(side=LEFT)
        self.entry_thisdate=tkinter.Entry(self.frame_date,width=12)
        self.entry_thisdate.pack(side=LEFT)
        self.label_totaluse=tkinter.Label(self.frame_date,text=" 전체사용량")
        self.label_totaluse.pack(side=LEFT)
        self.entry_totaluse=tkinter.Entry(self.frame_date,width=10,state='readonly')
        self.entry_totaluse.pack(side=LEFT)
        self.frame_date.pack(side=TOP,anchor=W)

        self.frame_fee=tkinter.Frame(self.watermanage)
        self.label_totalfee=tkinter.Label(self.frame_fee,text=" 건물수도료")
        self.label_totalfee.pack(side=LEFT)
        self.entry_totalfee=tkinter.Entry(self.frame_fee,width=8)
        self.entry_totalfee.pack(side=LEFT)
        self.label_totalpay=tkinter.Label(self.frame_fee,text="\t자동계산 납부수도료")
        self.label_totalpay.pack(side=LEFT)
        self.entry_totalpay=tkinter.Entry(self.frame_fee,width=8,state='readonly')
        self.entry_totalpay.pack(side=LEFT)
        self.button_carc=tkinter.Button(self.frame_fee,text="호실별 수도료 자동계산",command=self.autocarc)
        self.button_carc.pack(side=LEFT)
        self.button_apply=tkinter.Button(self.frame_fee,text="납부금액 요금적용",command=self.apply)
        self.button_apply.pack(side=LEFT)
        self.frame_fee.pack(side=TOP,anchor=E)
        self.load()

    def apply(self):    #납부금액 적용
        for room_num in room_num_list:
            sql.connection().fee_water_upsert(room_num,"%s-%s-00"%(str((inquiry_date_water + relativedelta(months=1)).year),str((inquiry_date_water + relativedelta(months=1)).month).zfill(2)),self.waterlist_dict[room_num].entry_payfee.get())
    
    def autocarc(self): #호실별 수도료 자동계산
        self.save()
        self.load()
        self.entry_totaluse.config(state='normal')
        self.entry_totalpay.config(state='normal')
        self.entry_totaluse.delete(0,'end')
        self.entry_totalpay.delete(0,'end')
        for room_num in room_num_list+[501]:
            self.waterlist_dict[room_num].entry_use.config(state='normal')
            self.waterlist_dict[room_num].entry_usefee.config(state='normal')
            self.waterlist_dict[room_num].entry_use.delete(0,'end')
            self.waterlist_dict[room_num].entry_usefee.delete(0,'end')
            self.waterlist_dict[room_num].entry_payfee.delete(0,'end')

        try:
            waterdf=mkdf_water_autocarc(sql.connection().water_select_lastmonth(inquiry_date_water-relativedelta(months=1)),sql.connection().water_select_thismonth(inquiry_date_water-relativedelta(months=1)))
            for room_num in room_num_list+[501]:
                self.waterlist_dict[room_num].entry_use.insert(0,int(waterdf.loc['use','r'+str(room_num)]))
                self.waterlist_dict[room_num].entry_usefee.insert(0,int(waterdf.loc['fee','r'+str(room_num)]))
                self.waterlist_dict[room_num].entry_payfee.insert(0,int(waterdf.loc['floor','r'+str(room_num)]))
                self.waterlist_dict[room_num].entry_use.config(state='readonly')
                self.waterlist_dict[room_num].entry_usefee.config(state='readonly')
            self.entry_totaluse.insert(0,int(waterdf.loc['use','total']))
            self.entry_totalpay.insert(0,int(waterdf.loc['floor','total']))
        except ValueError:
            pass

        self.entry_totaluse.config(state='readonly')
        self.entry_totalpay.config(state='readonly')

    def dele(self):
        sql.connection().water_delete(self.entry_thisdate.get())
        self.load()

    def load_inquiry(self): #조회
        global inquiry_date_water
        inquiry_date_water=date(int(self.entry_year.get()),int(self.entry_month.get()),1)
        print("조회: "+str(inquiry_date_water.year)+"-"+str(inquiry_date_water.month))
        self.load()

    def save(self): #저장
        global inquiry_date_water
        self.entry_year.delete(0,"end")
        self.entry_month.delete(0,"end")
        self.entry_year.insert(0,inquiry_date_water.year)
        self.entry_month.insert(0,inquiry_date_water.month)
        print("저장: "+str(inquiry_date_water.year)+"-"+str(inquiry_date_water.month))

        for room_num in room_num_list+[501]:
            sql.connection().water_room_upsert(self.entry_thisdate.get(),room_num,self.waterlist_dict[room_num].entry_pre.get())
        
        try:
            sql.connection().water_total_upsert(self.entry_thisdate.get(),self.entry_totalfee.get())
        except ValueError:
            pass
        self.load()

    def load(self): #불러오기
        global inquiry_date_water
        self.entry_year.delete(0,"end")
        self.entry_month.delete(0,"end")
        self.entry_year.insert(0,inquiry_date_water.year)
        self.entry_month.insert(0,inquiry_date_water.month)
        print("불러오기: "+str(inquiry_date_water.year)+"-"+str(inquiry_date_water.month))

        self.entry_totaluse.config(state='normal')
        self.entry_totalpay.config(state='normal')
        self.entry_totaluse.delete(0,'end')
        self.entry_totalpay.delete(0,'end')
        self.entry_totaluse.config(state='readonly')
        self.entry_totalpay.config(state='readonly')
        for room_num in room_num_list+[501]:
            self.waterlist_dict[room_num].entry_use.config(state='normal')
            self.waterlist_dict[room_num].entry_usefee.config(state='normal')
            self.waterlist_dict[room_num].entry_use.delete(0,'end')
            self.waterlist_dict[room_num].entry_usefee.delete(0,'end')
            self.waterlist_dict[room_num].entry_payfee.delete(0,'end')
            self.waterlist_dict[room_num].entry_use.config(state='readonly')
            self.waterlist_dict[room_num].entry_usefee.config(state='readonly')

        waterthisdf=sql.connection().water_select_thismonth(inquiry_date_water-relativedelta(months=1))
        waterlastdf=sql.connection().water_select_lastmonth(inquiry_date_water-relativedelta(months=1))
        for room_num in room_num_list+[501]:
            try:    #당월검침
                self.waterlist_dict[room_num].entry_pre.delete(0,'end')
                self.waterlist_dict[room_num].entry_pre.insert(0,str(waterthisdf.iloc[0]['r'+str(room_num)]))
            except IndexError:
                pass
            try:    #전월검침
                self.waterlist_dict[room_num].entry_past.config(state='normal')
                self.waterlist_dict[room_num].entry_past.delete(0,'end')
                self.waterlist_dict[room_num].entry_past.insert(0,str(waterlastdf.iloc[0]['r'+str(room_num)]))
            except IndexError:
                pass
            finally:
                self.waterlist_dict[room_num].entry_past.config(state='readonly')

        try:    #전월검침일
            self.entry_lastdate.config(state='normal')
            self.entry_lastdate.delete(0,'end')
            self.entry_lastdate.insert(0,str(waterlastdf.iloc[0]['meas_date']))
        except IndexError:
            pass
        finally:
            self.entry_lastdate.config(state='readonly')
        try:    #당월검침일
            self.entry_thisdate.delete(0,'end')
            self.entry_totalfee.delete(0,'end')
            self.entry_thisdate.insert(0,str(waterthisdf.iloc[0]['meas_date']))
            self.entry_totalfee.insert(0,str(waterthisdf.iloc[0]['total_fee']))
        except IndexError:
            pass

        for room_num in room_num_list:  #납부금액
            try:
                self.waterlist_dict[room_num].entry_payfee.delete(0,'end')
                waterfeedf=sql.connection().fee_select(room_num,"%s-%s-00"%(str((inquiry_date_water + relativedelta(months=1)).year),str((inquiry_date_water + relativedelta(months=1)).month).zfill(2)))
                self.waterlist_dict[room_num].entry_payfee.insert(0,str(waterfeedf.iloc[0]["water_fee"]))
            except IndexError:
                pass
        

    def load_prev(self):
        global inquiry_date_water
        inquiry_date_water -= relativedelta(months=1)
        self.load()

    def load_next(self):
        global inquiry_date_water
        inquiry_date_water += relativedelta(months=1)
        self.load()


#요금-------------------------------------------------------------------------------------------------
class feemanage_class():    #요금수동정산
    global inquiry_date_fee
    inquiry_date_fee=datetime.today() + relativedelta(months=1)
    feelist_dict={}

    class fee_room():   #세대별 요금
        def __init__(self,page,room_num) -> None:
            self.page=page
            self.room_num=room_num

        def show_fee(self):
            self.frame=tkinter.Frame(self.page,relief='sunken',borderwidth=3)
            self.frame.pack(fill="both")
            self.button_room=tkinter.Button(self.frame, text=self.room_num+"호")
            self.button_room.pack(side=LEFT)
            self.label_period=tkinter.Label(self.frame, text="청구기간")
            self.label_period.pack(side=LEFT)
            self.entry_start=tkinter.Entry(self.frame, width=12)
            self.entry_start.pack(side=LEFT)
            self.label_between=tkinter.Label(self.frame, text="~")
            self.label_between.pack(side=LEFT)
            self.entry_end=tkinter.Entry(self.frame, width=12)
            self.entry_end.pack(side=LEFT)
            self.label_limit=tkinter.Label(self.frame,text=" 납입시한")
            self.label_limit.pack(side=LEFT)
            self.entry_limit=tkinter.Entry(self.frame, width=12)
            self.entry_limit.pack(side=LEFT)
            self.label_rent=tkinter.Label(self.frame, text="\t임대료")
            self.label_rent.pack(side=LEFT)
            self.entry_rent=tkinter.Entry(self.frame, width=8)
            self.entry_rent.pack(side=LEFT)
            self.label_water=tkinter.Label(self.frame, text=" 수도료")
            self.label_water.pack(side=LEFT)
            self.entry_water=tkinter.Entry(self.frame, width=8)
            self.entry_water.pack(side=LEFT)
            self.label_unpaid=tkinter.Label(self.frame, text=" 전월미납")
            self.label_unpaid.pack(side=LEFT)
            self.entry_unpaid=tkinter.Entry(self.frame, width=8)
            self.entry_unpaid.pack(side=LEFT)
            self.button_total=tkinter.Label(self.frame, text=" 합계")
            self.button_total.pack(side=LEFT)
            self.entry_total=tkinter.Entry(self.frame, width=8, state='readonly')
            self.entry_total.pack(side=LEFT)
            self.button_dele=tkinter.Button(self.frame, text="삭제", width=4, bg="red", command=self.delete)
            self.button_dele.pack(side=RIGHT)
            self.button_save=tkinter.Button(self.frame, text="저장", width=8, command=self.save)
            self.button_save.pack(side=RIGHT)
            self.button_load=tkinter.Button(self.frame, text="불러오기",command=self.load)
            self.button_load.pack(side=RIGHT)
            self.button_auto=tkinter.Button(self.frame, text="자동계산")
            self.button_auto.pack(side=RIGHT)
        
        def delete(self):
            sql.connection().fee_delete(self.room_num,"%s-%s-00"%(str(inquiry_date_fee.year),str(inquiry_date_fee.month).zfill(2)))
            self.load()

        def total(self):
            self.entry_total.config(state='normal')
            self.entry_total.delete(0,"end")
            self.entry_total.insert(0,str(int(self.entry_rent.get())+int(self.entry_water.get())+int(self.entry_unpaid.get())))
            self.entry_total.config(state='readonly')
        
        def load(self):
            global inquiry_date_fee
            feedf=sql.connection().fee_select(self.room_num,"%s-%s-00"%(str(inquiry_date_fee.year),str(inquiry_date_fee.month).zfill(2)))
            self.entry_total.config(state='normal')
            self.entry_start.delete(0,"end")
            self.entry_end.delete(0,"end")
            self.entry_limit.delete(0,"end")
            self.entry_rent.delete(0,"end")
            self.entry_water.delete(0,"end")
            self.entry_unpaid.delete(0,"end")
            self.entry_total.delete(0,"end")
            try:
                self.entry_start.insert(0,str(feedf.iloc[0]["period_start"]))
                self.entry_end.insert(0,str(feedf.iloc[0]["period_end"]))
                self.entry_limit.insert(0,str(feedf.iloc[0]["pay_limit"]))
                self.entry_rent.insert(0,str(feedf.iloc[0]["rent_fee"]))
                self.entry_water.insert(0,str(feedf.iloc[0]["water_fee"]))
                self.entry_unpaid.insert(0,str(feedf.iloc[0]["unpaid_fee"]))
                self.entry_total.insert(0,str(feedf.iloc[0]["total_fee"]))
            except IndexError:
                pass
            self.entry_total.config(state='readonly')
        
        def save(self):
            self.total()
            sql.connection().fee_upsert(self.room_num,"%s-%s-00"%(str(inquiry_date_fee.year),str(inquiry_date_fee.month).zfill(2)),self.entry_start.get(),self.entry_end.get(),int(self.entry_rent.get()),int(self.entry_water.get()),int(self.entry_unpaid.get()),int(self.entry_total.get()),self.entry_limit.get())
            self.load()



    def load_inquiry(self): #조회
        global inquiry_date_fee
        inquiry_date_fee=date(int(self.entry_year.get()),int(self.entry_month.get()),1)
        print("조회: "+str(inquiry_date_fee.year)+"-"+str(inquiry_date_fee.month))
        self.load_all()
   
    def load_all(self): #전체불러오기
        global inquiry_date_fee
        self.entry_year.delete(0,"end")
        self.entry_month.delete(0,"end")
        self.entry_year.insert(0,inquiry_date_fee.year)
        self.entry_month.insert(0,inquiry_date_fee.month)
        print("전체불러오기: "+str(inquiry_date_fee.year)+"-"+str(inquiry_date_fee.month))
        for room_num in room_num_list:
            self.feelist_dict[room_num].load()
    
    def save_all(self): #전체저장
        global inquiry_date_fee
        self.entry_year.delete(0,"end")
        self.entry_month.delete(0,"end")
        self.entry_year.insert(0,inquiry_date_fee.year)
        self.entry_month.insert(0,inquiry_date_fee.month)
        print("전체저장: "+str(inquiry_date_fee.year)+"-"+str(inquiry_date_fee.month))
        for room_num in room_num_list:
            try:
                self.feelist_dict[room_num].save()
            except ValueError:
                pass
        self.load_all()

    def total_all(self): #전체합계
        for room_num in room_num_list:
            try:
                self.feelist_dict[room_num].total()
            except ValueError:
                pass

    def load_prev(self):
        global inquiry_date_fee
        inquiry_date_fee -= relativedelta(months=1)
        self.load_all()
    def load_next(self):
        global inquiry_date_fee
        inquiry_date_fee += relativedelta(months=1)
        self.load_all()

    def feemanage_popup(self):
        self.feemanage=Tk()
        self.feemanage.title("요금수동정산")
        self.feemanage.geometry("1200x550")
        self.select_frame=tkinter.Frame(self.feemanage)
        self.entry_year=tkinter.Entry(self.select_frame,width=6)
        self.entry_year.pack(side=LEFT)
        self.label_year=tkinter.Label(self.select_frame, text="년도 ")
        self.label_year.pack(side=LEFT)
        self.entry_month=tkinter.Entry(self.select_frame,width=4)
        self.entry_month.pack(side=LEFT)
        self.label_month=tkinter.Label(self.select_frame, text="월")
        self.label_month.pack(side=LEFT)
        self.button_inquiry=tkinter.Button(self.select_frame, text="조회", command=self.load_inquiry)
        self.button_inquiry.pack(side=LEFT)
        self.label_blank=tkinter.Label(self.select_frame,text="\t")
        self.label_blank.pack(side=LEFT)
        self.button_prev=tkinter.Button(self.select_frame, text="이전", width=10, command= self.load_prev)
        self.button_prev.pack(side=LEFT)
        self.button_next=tkinter.Button(self.select_frame, text="다음", width=10, command= self.load_next)
        self.button_next.pack(side=LEFT)
        self.button_allsave=tkinter.Button(self.select_frame, text="전체저장", command=self.save_all)
        self.button_allsave.pack(side=RIGHT)
        self.button_allload=tkinter.Button(self.select_frame, text="전체불러오기", command=self.load_all)
        self.button_allload.pack(side=RIGHT)
        self.button_allauto=tkinter.Button(self.select_frame, text="전체자동계산")
        self.button_allauto.pack(side=RIGHT)
        self.button_alltotal=tkinter.Button(self.select_frame, text="전체합계", command=self.total_all)
        self.button_alltotal.pack(side=RIGHT)
        self.button_waterdel=tkinter.Button(self.select_frame, text="수도료 삭제", command=self.water_del, bg='pink')
        self.button_waterdel.pack(side=RIGHT)
        self.select_frame.pack(side=TOP, ipadx=30, ipady=10)
        
        for room_num in room_num_list:
            self.feelist_dict[room_num]=self.fee_room(self.feemanage,str(room_num))
            self.feelist_dict[room_num].show_fee()
        
        self.load_all()
    
    def water_del(self):
        for room_num in room_num_list:
            self.feelist_dict[room_num].entry_water.delete(0,"end")
            self.feelist_dict[room_num].entry_water.insert(0,"0")
        self.save_all()


#납입------------------------------------------------------------------------------------------------
class paymanage_class():    #납입관리
    global inquiry_date_pay
    inquiry_date_pay=datetime.today() + relativedelta(months=1)
    paylist_dict={}

    class pay_room():   #세대별 요금
        def __init__(self,page,room_num) -> None:
            self.page=page
            self.room_num=room_num

        def show_pay(self):
            self.frame=tkinter.Frame(self.page,relief='sunken',borderwidth=3)
            self.frame.pack(fill="both")
            self.button_room=tkinter.Button(self.frame, text=self.room_num+"호")
            self.button_room.pack(side=LEFT)
            self.label_limit=tkinter.Label(self.frame,text="납입시한")
            self.label_limit.pack(side=LEFT)
            self.entry_limit=tkinter.Entry(self.frame, width=12, state='readonly')
            self.entry_limit.pack(side=LEFT)
            self.label_total=tkinter.Label(self.frame, text="당월 합계액")
            self.label_total.pack(side=LEFT)
            self.entry_total=tkinter.Entry(self.frame, width=8, state='readonly')
            self.entry_total.pack(side=LEFT)
            self.label_pay=tkinter.Label(self.frame, text=" 납입금액")
            self.label_pay.pack(side=LEFT)
            self.entry_pay=tkinter.Entry(self.frame, width=8)
            self.entry_pay.pack(side=LEFT)
            self.label_date=tkinter.Label(self.frame, text=" 납입일")
            self.label_date.pack(side=LEFT)
            self.entry_date=tkinter.Entry(self.frame, width=12)
            self.entry_date.pack(side=LEFT)
            self.label_method=tkinter.Label(self.frame, text=" 납입방법")
            self.label_method.pack(side=LEFT)
            self.entry_method=tkinter.Entry(self.frame, width=15)
            self.entry_method.pack(side=LEFT)
            self.label_memo=tkinter.Label(self.frame, text=" 비고")
            self.label_memo.pack(side=LEFT)
            self.entry_memo=tkinter.Entry(self.frame, width=15)
            self.entry_memo.pack(side=LEFT)
            self.button_save=tkinter.Button(self.frame, text="저장", width=8, command=self.save)
            self.button_save.pack(side=RIGHT)
            self.button_load=tkinter.Button(self.frame, text="불러오기",command=self.load)
            self.button_load.pack(side=RIGHT)
            self.button_auto=tkinter.Button(self.frame, text="납입취소",command=self.cancle,bg='pink')
            self.button_auto.pack(side=RIGHT)
            self.button_auto=tkinter.Button(self.frame, text="납입완료",command=self.perfect)
            self.button_auto.pack(side=RIGHT)

        

        
        def load(self):
            global inquiry_date_pay
            paydf=sql.connection().fee_select(self.room_num,"%s-%s-00"%(str(inquiry_date_pay.year),str(inquiry_date_pay.month).zfill(2)))
            self.entry_limit.config(state='normal')
            self.entry_total.config(state='normal')
            self.entry_limit.delete(0,"end")
            self.entry_total.delete(0,"end")
            self.entry_pay.delete(0,"end")
            self.entry_date.delete(0,"end")
            self.entry_method.delete(0,"end")
            self.entry_memo.delete(0,"end")

            try:
                self.entry_limit.insert(0,str(paydf.iloc[0]["pay_limit"]))
                self.entry_total.insert(0,str(paydf.iloc[0]["total_fee"]))
                self.entry_pay.insert(0,str(paydf.iloc[0]["paid_fee"]))
                self.entry_date.insert(0,str(paydf.iloc[0]["paid_date"]))
                self.entry_method.insert(0,str(paydf.iloc[0]["paid_method"]))
                self.entry_memo.insert(0,str(paydf.iloc[0]["paid_memo"]))
            except (IndexError,AttributeError):
                pass
            self.entry_limit.config(state='readonly')
            self.entry_total.config(state='readonly')
        
        def save(self):
            sql.connection().pay_update(self.room_num,"%s-%s-00"%(str(inquiry_date_pay.year),str(inquiry_date_pay.month).zfill(2)),self.entry_pay.get(),self.entry_date.get(),self.entry_method.get(),self.entry_memo.get())
            self.load()
        
        def perfect(self):
            self.entry_pay.delete(0,'end')
            self.entry_pay.insert(0,self.entry_total.get())
            self.save()
            self.load()

        def cancle(self):
            self.entry_pay.delete(0,'end')
            self.entry_pay.insert(0,'')
            self.save()
            self.load()        



    def load_inquiry(self): #조회
        global inquiry_date_pay
        inquiry_date_pay=date(int(self.entry_year.get()),int(self.entry_month.get()),1)
        print("조회: "+str(inquiry_date_pay.year)+"-"+str(inquiry_date_pay.month))
        self.load_all()
   
    def load_all(self): #전체불러오기
        global inquiry_date_pay
        self.entry_year.delete(0,"end")
        self.entry_month.delete(0,"end")
        self.entry_year.insert(0,inquiry_date_pay.year)
        self.entry_month.insert(0,inquiry_date_pay.month)
        print("전체불러오기: "+str(inquiry_date_pay.year)+"-"+str(inquiry_date_pay.month))
        for room_num in room_num_list:
            self.paylist_dict[room_num].load()
    
    def save_all(self): #전체저장
        global inquiry_date_pay
        self.entry_year.delete(0,"end")
        self.entry_month.delete(0,"end")
        self.entry_year.insert(0,inquiry_date_pay.year)
        self.entry_month.insert(0,inquiry_date_pay.month)
        print("전체저장: "+str(inquiry_date_pay.year)+"-"+str(inquiry_date_pay.month))
        for room_num in room_num_list:
            try:
                self.paylist_dict[room_num].save()
            except ValueError:
                pass

    def load_prev(self):
        global inquiry_date_pay
        inquiry_date_pay -= relativedelta(months=1)
        self.load_all()
    def load_next(self):
        global inquiry_date_pay
        inquiry_date_pay += relativedelta(months=1)
        self.load_all()

    def paymanage_popup(self):
        self.paymanage=Tk()
        self.paymanage.title("납입정보입력")
        self.paymanage.geometry("1200x550")
        self.select_frame=tkinter.Frame(self.paymanage)
        self.entry_year=tkinter.Entry(self.select_frame,width=6)
        self.entry_year.pack(side=LEFT)
        self.label_year=tkinter.Label(self.select_frame, text="년도 ")
        self.label_year.pack(side=LEFT)
        self.entry_month=tkinter.Entry(self.select_frame,width=4)
        self.entry_month.pack(side=LEFT)
        self.label_month=tkinter.Label(self.select_frame, text="월")
        self.label_month.pack(side=LEFT)
        self.button_inquiry=tkinter.Button(self.select_frame, text="조회", command=self.load_inquiry)
        self.button_inquiry.pack(side=LEFT)
        self.label_blank=tkinter.Label(self.select_frame,text="\t")
        self.label_blank.pack(side=LEFT)
        self.button_prev=tkinter.Button(self.select_frame, text="이전", width=10, command= self.load_prev)
        self.button_prev.pack(side=LEFT)
        self.button_next=tkinter.Button(self.select_frame, text="다음", width=10, command= self.load_next)
        self.button_next.pack(side=LEFT)
        self.button_allsave=tkinter.Button(self.select_frame, text="전체저장", command=self.save_all)
        self.button_allsave.pack(side=RIGHT)
        self.button_allload=tkinter.Button(self.select_frame, text="전체불러오기", command=self.load_all)
        self.button_allload.pack(side=RIGHT)
        self.select_frame.pack(side=TOP, ipadx=30, ipady=10)
        
        for room_num in room_num_list:
            self.paylist_dict[room_num]=self.pay_room(self.paymanage,str(room_num))
            self.paylist_dict[room_num].show_pay()
        
        self.load_all()


#계약---------------------------------------------------------------------------------------------
class contmanage_class():   #계약관리
    contlist_dict={}
    
    class cont_room():   #세대별 요금
        def __init__(self,page,room_num) -> None:
            self.page=page
            self.room_num=room_num

        def show_cont(self):
            self.frame=tkinter.Frame(self.page,relief='sunken',borderwidth=3)
            self.frame.pack(fill="both")
            self.button_room=tkinter.Button(self.frame, text=self.room_num+"호")
            self.button_room.pack(side=LEFT)
            self.var_empty = tkinter.BooleanVar()
            self.check_empty=tkinter.Checkbutton(self.frame, variable=self.var_empty, text="공실", bg='#a3d278', onvalue=True,offvalue=False)
            self.check_empty.pack(side=LEFT)
            self.label_cont=tkinter.Label(self.frame,text="계약일")
            self.label_cont.pack(side=LEFT)
            self.entry_cont=tkinter.Entry(self.frame, width=12)
            self.entry_cont.pack(side=LEFT)
            self.label_name=tkinter.Label(self.frame, text="계약자명")
            self.label_name.pack(side=LEFT)
            self.entry_name=tkinter.Entry(self.frame, width=6)
            self.entry_name.pack(side=LEFT)
            self.label_phone=tkinter.Label(self.frame, text=" 전화번호")
            self.label_phone.pack(side=LEFT)
            self.entry_phone=tkinter.Entry(self.frame, width=12)
            self.entry_phone.pack(side=LEFT)
            self.label_depo=tkinter.Label(self.frame, text=" 계약금")
            self.label_depo.pack(side=LEFT)
            self.entry_depo=tkinter.Entry(self.frame, width=10)
            self.entry_depo.pack(side=LEFT)
            self.label_rent=tkinter.Label(self.frame, text=" 월세")
            self.label_rent.pack(side=LEFT)
            self.entry_rent=tkinter.Entry(self.frame, width=10)
            self.entry_rent.pack(side=LEFT)
            self.label_lang=tkinter.Label(self.frame, text=" 언어")
            self.label_lang.pack(side=LEFT)
            self.combo_lang=ttk.Combobox(self.frame, values=language_list, width=7)
            self.combo_lang.current(0)
            self.combo_lang.pack(side=LEFT)

       

        
        def load(self):
            contdf=sql.connection().room_select(self.room_num)

            self.entry_cont.delete(0,'end')
            self.entry_name.delete(0,'end')
            self.entry_phone.delete(0,'end')
            self.entry_depo.delete(0,'end')
            self.entry_rent.delete(0,'end')     
            
            if contdf.iloc[0]["empty"]==1:
                self.check_empty.select()
            else:
                self.check_empty.deselect()
            self.entry_cont.insert(0,str(contdf.iloc[0]["cont_date"]))
            self.entry_name.insert(0,str(contdf.iloc[0]["name"]))
            self.entry_phone.insert(0,str(contdf.iloc[0]["phone"]))
            self.entry_depo.insert(0,str(contdf.iloc[0]["deposit"]))
            self.entry_rent.insert(0,str(contdf.iloc[0]["rent_fee"]))
            self.combo_lang.current(contdf.iloc[0]["language"])

        
        def save(self):
            print(id(self.var_empty))
            sql.connection().room_update(self.room_num, self.entry_cont.get(), self.entry_name.get(), self.entry_phone.get(), self.entry_depo.get(), self.entry_rent.get(), self.var_empty.get(), self.combo_lang.current())
            self.load()

   
    def load_all(self): #전체불러오기
        print("전체불러오기: 계약정보")
        for room_num in room_num_list:
            self.contlist_dict[room_num].load()
    
    def save_all(self): #전체저장
        print("전체저장: 계약정보")
        for room_num in room_num_list:
            try:
                self.contlist_dict[room_num].save()
            except ValueError:
                pass


    def contmanage_popup(self):
        self.contmanage=Tk()
        self.contmanage.title("계약정보관리")
        self.contmanage.geometry("850x550")
        self.select_frame=tkinter.Frame(self.contmanage)
        self.button_allsave=tkinter.Button(self.select_frame, text="저장", command=self.save_all)
        self.button_allsave.pack(side=RIGHT)
        self.button_allload=tkinter.Button(self.select_frame, text="불러오기", command=self.load_all)
        self.button_allload.pack(side=RIGHT)
        self.select_frame.pack(side=TOP, ipadx=30, ipady=10)
        
        for room_num in room_num_list:
            self.contlist_dict[room_num]=self.cont_room(self.contmanage,str(room_num))
            self.contlist_dict[room_num].show_cont()

        self.load_all()





#HOME-------------------------------------------------------------------------
root=Tk()
root.title("화이트빌 BMS")
root.geometry("1000x1000")

menubar=tk.Menu(root)

filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="파일선택")
filemenu.add_command(label="기본파일열기")
filemenu.add_command(label="새로고침")
filemenu.add_command(label="렌덤채우기")
filemenu.add_command(label="종료",command=quit)
menubar.add_cascade(label="프로그램", menu=filemenu)

feemenu = tk.Menu(menubar, tearoff=0)
feemenu.add_command(label="요금수동정산", command= lambda: feemanage_class().feemanage_popup())
menubar.add_cascade(label="요금관리", menu=feemenu)

watermenu = tk.Menu(menubar, tearoff=0)
watermenu.add_command(label="수도지침관리", command= lambda: watermanage_class().watermanage_popup())
menubar.add_cascade(label="수도관리", menu=watermenu)

paymenu = tk.Menu(menubar, tearoff=0)
paymenu.add_command(label="납입정보입력", command= lambda: paymanage_class().paymanage_popup())
menubar.add_cascade(label="납입관리", menu=paymenu)

roommenu = tk.Menu(menubar, tearoff=0)
roommenu.add_command(label="계약정보관리", command= lambda: contmanage_class().contmanage_popup())
menubar.add_cascade(label="계약관리", menu=roommenu)

statmenu = tk.Menu(menubar, tearoff=0)
statmenu.add_command(label="납입현황표")
statmenu.add_command(label="수도요금산출액")
menubar.add_cascade(label="현황", menu=statmenu)
infomenu = tk.Menu(menubar, tearoff=0)
infomenu.add_command(label="프로그램 정보")
menubar.add_cascade(label="정보", menu=infomenu)

root.config(menu=menubar)
root.mainloop()
