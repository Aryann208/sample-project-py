from indicators import Stochastic , SuperTrend , MADIST,ATR , SMA , nADX, SAR , Macd , Chandelier_Stop
from datetime import datetime as dt
from datetime import timedelta
import requests
import re

from bs4 import BeautifulSoup
from time import sleep

import pandas as pd
import numpy as np

def masterframe(i,day,df,df2):
    global properadx
    global properdmi
    global adxval
    adx=properadx
    dmi=properdmi
    dx=50
    #dmi=40
    #dmi=30
    global deviation
    
    if i==0:
        day="START"
    while i<48810:  
        signal="NONE"
        isExit=False 
        print(day)
        print("(********************* i val =)"+str(i))
        if day=="OVER":
            print("back 1 frame")
            i=i-1
            print("NEW DAY "+str(df["Timestamp"].iloc[i]))
            print("CHANGE AFTER DAY "+ str(day))
        print(df["Timestamp"].iloc[i])    
        while isforbiddentime(df,i)==True:
            print("Forbidden time")
            while isforbiddentime(df,i)==True:
                i=i+1
            print("DAYOVER--------------")
            day="OVER"
            break
        day="START"
        ###################BULLISH LOOP########
        if day=="OVER":
            return i , day
        if df["STX"].iloc[i]=="UP":
            print("BULLISH TREND "+str(df["Timestamp"].iloc[i]))
            #print("Value of I is "+str(i))

            #make STX vs CHECJER
            #loop1
            signal="UP"
            while df["STX"].iloc[i]=="UP"  and signal=="UP":
                count=0
                print("STX CHECK "+str(df["Timestamp"].iloc[i]))
                day="START"
                if df["STX"].iloc[i-1]=="DOWN" and df["STX"].iloc[i]=="UP" or  (isOpencandle(df,i) and df["STX"].iloc[i]=="UP")==True :
                #if i!=-1:
                    print("STX CHECK SUCCESS "+str(df["Timestamp"].iloc[i]))
                    print("SAR CHECK "+str(df["Timestamp"].iloc[i]))
                    #loop2
                    while df["STX"].iloc[i]=="UP"  and signal=="UP":
                        print(count)
                        print("CHECKING SAR VS CONDITION"+str(df["Timestamp"].iloc[i]))
                        #if (df["SAR_POS_2"].iloc[i]=="UP" and count==0)==True or (df["SAR_POS_2"].iloc[i-1]=="DOWN" and df["SAR_POS_2"].iloc[i]=="UP")==True:
                        if df["SAR_POS_2"].iloc[i]=="UP":
                            print(df["SAR_POS_2"].iloc[i])
                            print("SAR CHECK SUCCESS "+str(df["Timestamp"].iloc[i]))
                            count=count+1

                            #ADX CHECK
                            if (df["ADX"].iloc[i] <= adx and (df["DMI+"].iloc[i] >df["DMI-"].iloc[i] and df["DMI+"].iloc[i] +df["DMI-"].iloc[i] >=dmi)==True and df["ADX"].iloc[i] >= adxval )==True or meanadx(df,i,"BUY"):
                                
                                print("ADX and MACD CHECK SUCCESS "+str(df["Timestamp"].iloc[i]))
                                entryprice=df["High"].iloc[i]-deviation#+3
                                
                                print("Entry Price : "+str(entryprice))
                                signaltime.append((df["Timestamp"].iloc[i]))####
                                print(len(df2))
                                buysignal.append(1)
                                i=BUY_ITER(i,entryprice,df,df2)
                                isExit=True
                                if df["STX"].iloc[i]=="DOWN":
                                    print("Master Trend Has Changed")
                                    break
                                
                                while isforbiddentime(df,i)==True:
                                    while isforbiddentime(df,i)==True:
                                        i=i+1
                                    print("DAYOVER--------------")
                                    i=i-1
                                    day="OVER"
                                    signal="NONE"
                                    break
                                i=i+1
                                
                            ###to beak loop2
                            else :
                                print("ADX and MACD CHECK FAIL "+str(df["Timestamp"].iloc[i]))
                                i=i+1
                                
                                while isforbiddentime(df,i)==True:
                                    while isforbiddentime(df,i)==True:
                                        i=i+1
                                    print("DAYOVER--------------")
                                    i=i-1
                                    day="OVER"
                                    signal="NONE"
                                    break
                                
                                    
                                print("Wait Over"+ str(dt.now().time()))

                                isExit=False
                        else:
                            print("SAR CHECK FAIL "+str(df["Timestamp"].iloc[i]))
                            
                            i=i+1
                            while isforbiddentime(df,i)==True:
                                while isforbiddentime(df,i)==True:
                                    i=i+1
                                print("DAYOVER--------------")
                                i=i-1
                                day="OVER"
                                signal="NONE"
                                break
                            if day=="OVER":
                                print("breaking loop since day is over")
                                return i , day
                            if df["STX"].iloc[i]=="DOWN":
                                print("Trend Change")
                                #i=i-1
                                break
        
                            print("Wait Over"+ str(dt.now().time()))

                            isExit=False
                ####to break loop 1
                else:
                    print("STX CHECK FAIL "+str(df["Timestamp"].iloc[i]))
                    i=i+1
                    while isforbiddentime(df,i)==True:
                        while isforbiddentime(df,i)==True:
                            i=i+1
                        print("DAYOVER--------------")
                        i=i-1
                        day="OVER"
                        signal="NONE"
                        break
                    if day=="OVER":
                        print("breaking loop since day is over")
                        return i , day
                        
                        
###################### BEARISH LOOP###########
        if df["STX"].iloc[i]=="DOWN":
            df2=df2
            day="START"
            print("BEARISH TREND "+str(df["Timestamp"].iloc[i]))
            #print("Value of I is "+str(i))
            isExit==False
            #make STX vs CHECJER
            #loop1
            signal="DOWN"
            while df["STX"].iloc[i]=="DOWN" and signal=="DOWN":
                count=0
                print("STX CHECK "+str(df["Timestamp"].iloc[i]))

                if df["STX"].iloc[i-1]=="UP" and df["STX"].iloc[i]=="DOWN" or  (isOpencandle(df,i) and df["STX"].iloc[i]=="DOWN")==True:
                #if i!=-1:
                    print("STX CHECK SUCCESS "+str(df["Timestamp"].iloc[i]))
                    print("SAR CHECK "+str(df["Timestamp"].iloc[i]))
                    #loop2
                    while df["STX"].iloc[i]=="DOWN"  and signal=="DOWN":
                        print(count)
                        print("CHECKING SAR VS CONDITION"+str(df["Timestamp"].iloc[i]))
                        #if (df["SAR_POS_2"].iloc[i]=="DOWN" and count==0)==True or (df["SAR_POS_2"].iloc[i-1]=="UP" and df["SAR_POS_2"].iloc[i]=="DOWN")==True:
                        if df["SAR_POS_2"].iloc[i]=="DOWN":
                            print(df["SAR_POS_2"].iloc[i])
                            print("SAR CHECK SUCCESS "+str(df["Timestamp"].iloc[i]))
                            count=count+1

                            #ADX CHECK
                            if (df["ADX"].iloc[i] <= adx and (df["DMI+"].iloc[i] < df["DMI-"].iloc[i] and df["DMI+"].iloc[i] +df["DMI-"].iloc[i] >=dmi)==True and df["ADX"].iloc[i] >= adxval)==True or meanadx(df,i,"SELL") :
                            
                                print("ADX and MACD CHECK SUCCESS "+str(df["Timestamp"].iloc[i]))
                                entryprice=df["Low"].iloc[i]+deviation#-3
                                
                                signaltime.append((df["Timestamp"].iloc[i]))#### 
                                print(len(df2))
                                sellsignal.append(1)
                                i=SELL_ITER(i,entryprice,df,df2)
                                isExit=True
                                if df["STX"].iloc[i]=="UP":
                                    print("Master Trend Has Changed")
                                    break
                                while isforbiddentime(df,i)==True:
                                    while isforbiddentime(df,i)==True:
                                        i=i+1
                                    print("DAYOVER--------------")
                                    i=i-1
                                    day="OVER"
                                    signal="NONE"
                                    break
                                if day=="OVER":
                                    print("breaking loop since day is over")
                                    return i , day
                                i=i+1
                            ###to beak loop2
                            else :
                                print("ADX and MACD CHECK FAIL "+str(df["Timestamp"].iloc[i]))
                                i=i+1
                                
                                while isforbiddentime(df,i)==True:
                                    while isforbiddentime(df,i)==True:
                                        i=i+1
                                    print("DAYOVER--------------")
                                    i=i-1
                                    day="OVER"
                                    signal="NONE"
                                    break
                                if day=="OVER":
                                    print("breaking loop since day is over")
                                    return i , day
                                    
                                print("Wait Over"+ str(dt.now().time()))

                                isExit=False
                        else:
                            print("SAR CHECK FAIL "+str(df["Timestamp"].iloc[i]))
                            
                            i=i+1
                            while isforbiddentime(df,i)==True:
                                while isforbiddentime(df,i)==True:
                                    i=i+1
                                print("DAYOVER--------------")
                                i=i-1
                                day="OVER"
                                signal="NONE"
                                break
                            if day=="OVER":
                                print("breaking loop since day is over")
                                return i , day
                            if df["STX"].iloc[i]=="UP":
                                print("Trend Change")
                                #i=i-1
                                break
        
                            print("Wait Over"+ str(dt.now().time()))

                            isExit=False
                ####to break loop 1
                else:
                    print("STX CHECK FAIL "+str(df["Timestamp"].iloc[i]))
                    i=i+1
                    while isforbiddentime(df,i)==True:
                        while isforbiddentime(df,i)==True:
                            i=i+1
                        print("DAYOVER--------------")
                        i=i-1
                        day="OVER"
                        signal="NONE"
                        break
                    if day=="OVER":
                        print("breaking loop since day is over")
                        return i , day
        else:
            i=i+1
    return i , day
            

import joblib
model = joblib.load('../fyers_algo/trade_filter_model.pkl')
THRESHOLD = 0.6

# Feature names in the order used by the model
FEATURES = ['Stochastic', 'RSI', 'RSI_sl', 'momentum_3', 'momentum_5', 'vol_std_10', 'PositionType']


def should_take_trade(i: int, df: pd.DataFrame, df2: pd.DataFrame, is_buy: bool) -> bool:
    """
    Build feature vector for the potential trade at index i and decide via ML.

    Args:
      i      : index in df (10‑min) for the signal time
      df     : DataFrame with 10‑min bars, columns ['Stochastic','RSI']
      df2    : DataFrame with  2‑min bars, columns ['RSI_sl','momentum_3','momentum_5','vol_std_10']
      is_buy : True for BUY_ITER, False for SELL_ITER

    Returns:
      True if model predicts profit probability >= THRESHOLD
    """
    # extract features from df and df2 at the same timestamp
    # assume df2 index aligns or nearest after df index i
    if pause_model==True:
        return True
    ts = df.index[i]
    # find nearest index in df2 at or just before ts
    if ts in df2.index:
        j = df2.index.get_loc(ts)
    else:
        # get last index less than ts
        j = df2.index.asof(ts)
        j = df2.index.get_indexer([j])[0]

    # build feature list in correct order
    vals = []
    # Stochastic & RSI from df
    vals.append(df.at[df.index[i], 'Stochastic'])
    vals.append(df.at[df.index[i], 'RSI'])
    # RSI_sl, momentum_3, momentum_5, vol_std_10 from df2
    for col in ['RSI_sl', 'momentum_3', 'momentum_5', 'vol_std_10']:
        vals.append(df2.at[df2.index[j], col])
    # PositionType
    vals.append(0 if is_buy else 1)

    # convert to 2D array for model
    X = np.array(vals).reshape(1, -1)
    proba = model.predict_proba(X)[0][1]
    # debug print
    print(f"ML P(profit)={proba:.2f} at index={i}, {'BUY' if is_buy else 'SELL'}")
    return proba >= THRESHOLD

def BUY_ITER(i,entryprice,df,df2):
    ######print("BUY ITER LOOP")
    high = 0 
    ### to fix -5 iteration after buy initaiation check
    i=i+1
    j=0
    k=0
    position=""
    trend="UP"
    passcondn=0
    renter_buy=0
    renterprice=0
    checkrenter=0
    iterafterfail=0
    afterExit=False
    isRentertag=0
    global save
    global positiveslip
    save=0
    global day
    adxfilter=100
    global datetoday
    global datenow
    global pointstoday
    datetoday=df["Timestamp"].iloc[i].split("-")[0]
    #if len(order)==0:
    #    datenow=df["Timestamp"].iloc[0].split("-")[0]
    day="NONE"
    #print(pointstoday)
    
    ######## positive slippage includer
    #if df2["Low"].iloc[j+k+1]<entryprice-positiveslip and df2["Open"].iloc[j+k+1]<df2["High"].iloc[j+k]-positiveslip:
    #    entryprice=entryprice-positiveslip
    #else:
    #    return i
                
    while trend=="UP":
        ##1
        if df["STX"].iloc[i-1]=="UP" and df["SAR_POS_2"].iloc[i-1]=="UP" :
            
            while trend=="UP":
                if datetoday!=datenow:
                    pointstoday=0
                    datenow=datetoday
                if renterprice>0 :
                    
                    entryprice=renterprice
                    
                    ###print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                    ###print(entryprice)
                if renter_buy>0:
                    entryprice=renter_buy
                k=jfetch(df,i,k)
                ######print("ITERATING "+str(entryprice))
                
                ######print(df2["Timestamp"].iloc[j+k])
                #######print("Value of I is "+str(i))
                ######print(df2["SAR_POS_sl"].iloc[j+k])
                ######print(df2["STX_sl"].iloc[j+k])
                if ((df2["SAR_POS_sl"].iloc[j+k]=="UP" and  df2["STX_sl"].iloc[j+k]=="UP") or (df2["SAR_POS_sl"].iloc[j+k]=="UP" and renterprice>0)) :# and df["RSI"].iloc[i-1]>60 and df["CCI"].iloc[i-1]>-50)  :
                    #print(pointstoday)        
                    
                    if renter_buy>0:
                        isRentertag=1
                        signaltime.append(df2["Timestamp"].iloc[i])
                        isRenter.append("Yes")
                        entryprice=renter_buy
                        renter_buy=0
                        
                    if renterprice>0:
                        entryprice=renterprice
                        ###print("^^^^^^^^^^^^^^^^^^^^^^")
                        ###print(entryprice)
                        renterprice=0
                        ##modification
                        #j=0
                        renterprice=0
                    entryprice=entryprice 
                    ######print(i )
                    ######print(entryprice)
                    if (df2["High"].iloc[j+k] >= entryprice and position=="") and (df2["RSI_sl"].iloc[j+k-1]>-6) and should_take_trade(i, df, df2, is_buy=True):# and(df["MA"].iloc[i-1]<entryprice):#and ( df["RSI"].iloc[i-1]>-10 and df["CCI"].iloc[i-1]>0 and df2["RSI_sl"].iloc[j+k-1]>0 and df2["MADIST_sl"].iloc[j+k-1]==1)  :
                        #if (df2["High"].iloc[j+k] >= entryprice and position=="" )  :#(df2["RSI_sl"].iloc[j+k-1]>-10 and df["RSI"].iloc[i-1]>-15)
                        #df2["RSI_sl"].iloc[j+k-1]>-5 and df["RSI"].iloc[i-1]>-5 and and  df2["CCI_sl"].iloc[j+k-1]>-100 
                       #if ( df2["MADIST_sl"].iloc[j+k-1]==1 ):#and df["CCI"].iloc[i-1]>-50 ) :#df["RSI"].iloc[i-1]>-10 and df["CCI"].iloc[i-1]>0 and df2["RSI_sl"].iloc[j+k-1]>0 and 
                       #    passcondn=1
                       #else:
                       #    return i
                       #passcondn=0 
                        if datetoday!=datenow:
                            pointstoday=0
                            datenow=datetoday
                        position="open"
                        renterprice=0
                        ######print("BUY ORDER at " + str(entryprice) )
                        #place buy order code here
                        ######print("BUY ORDER PLACED"+str(df2["Timestamp"].iloc[j+k]))
                        ordertime.append((df2["Timestamp"].iloc[j+k]))
                        stochasticList.append(df["Stochastic"].iloc[i-1])
                        stochasticSlList.append(df2["Stochastic"].iloc[j+k-1])
                        
                        
                            
                        order.append(entryprice)
                        rsientry.append(df["RSI"].iloc[i-1])
                        rsi_slentry.append(df2["RSI_sl"].iloc[j+k-1])
                        m3.append(df2["momentum_3"].iloc[j+k-1])
                        m5.append(df2["momentum_5"].iloc[j+k-1])
                        vol_std.append(df2["vol_std_10"].iloc[j+k-1])
                        #rsientry.append(df["MADIST"].iloc[i-1])
                        #rsi_slentry.append(df2["MADIST_sl"].iloc[j+k-1])
                        ###print("^^^^^^^^^^^^^^^^^^^^^^")
                        if save>0:
                            entryprice=save
                            save=0
                        ###print(entryprice)
                        buysignal.append(0)
                        i,j,renter_buy=BUY_EXIT(entryprice,i,j,df,df2)
                        if datetoday==datenow:
                            pointstoday=pointstoday+points[-1]
                            print(pointstoday)
                       #global day
                        afterExit=True
                        if day=="OVER":
                            ######print("DayOver")
                            return i
                        if isforbiddentimesl(df,i)==True:
                            while isforbiddentimesl(df,i)==True:
                                i=i+1
                            ######print("DAYOVER--------------")
                            i=i-1
                            day="OVER"
                            position=""
                            trend=""
                            return i
                        
                        #buyOrder(symbol,token,entryprice)
                        
                        if isRentertag!=1:
                            isRenter.append("No")
                        isRentertag=0
                        
                        #telegram_bot_sendtext("BUY at "+str(entryprice))
                        #telegram_bot_sendtext(str(df2["Timestamp"].iloc[j+k]))
                        
                        
                        position=""
                        if renter_buy>0:
                            print(renter_buy)
                            ######print("running to check reenter condition")
                        #####modification1504
                        if df["STX"].iloc[i]=="DOWN" or df["SAR_POS_2"].iloc[i]=="DOWN":
                            return i-1
                        

                    
                    ##### use j iterator here
                    if j<=4:
                        j=j+1
                        ######print("j+ candle")
                        ######print(j)
                        #break
                    if j==5:
                        j=0
                        i=i+1
                        ######print("i candle+ after j complete5")
                        ######print(i)
              
                    if isforbiddentimesl(df,i)==True:
                        while isforbiddentimesl(df,i)==True:
                            i=i+1
                        ######print("DAYOVER--------------")
                        i=i-1
                        day="OVER"
                        position=""
                        trend=""
                        return i           
                                
                ##2
                else:
                    print(" failed recheck master")
                    #######print("Value of I is "+str(i))               
                    ######print("WAIT OVER"+str(df["Timestamp"].iloc[i]))
                    ######print("SLframe time"+str(df2["Timestamp"].iloc[j+k]))
                    ###### look maybe error here
                    renter_buy=0
                    
                    if df["SAR_POS_2"].iloc[i]=="UP" and  df["STX"].iloc[i]=="UP": 
                        ######print("SAR AND ST INTACT"+str(df["Timestamp"].iloc[i]))
                        ######print("CHECK SL FRAME ST AND SAR")
                        #modification 1104
                        
                            #break
                        #k=jfetch(df,i,k)
                        
                        #if df2["STX_sl"].iloc[j+k]=="UP" and df2["SAR_POS_sl"].iloc[j+k]=="DOWN":
                        #    #renterprice=df2["High"].iloc[j+k]
                        #    #renterprice=df2["SAR_sl"].iloc[j+k]
                        #    renterprice=df2["SAR_sl"].iloc[j+k]
                        #    ######print("got renterprice "+str(renterprice))
                        #if df["SAR_POS_2"].iloc[i]=="UP" and df2["STX_sl"].iloc[j+k]=="DOWN" and df2["SAR_POS_sl"].iloc[j+k]=="DOWN":
                        #    renterprice=df2["SAR_sl"].iloc[j+k]
                        #    ######print("got renterprice "+str(renterprice))
                        #    ##### use j iterator here                                
                        
                        if (df2["SAR_POS_sl"].iloc[j+k]=="DOWN" or df2["STX_sl"].iloc[j+k]=="DOWN") :#and (df2["SAR_POS_sl"].iloc[j+k+1]=="UP" or df2["STX_sl"].iloc[j+k+1]=="UP"):
                            #k=jfetch(df,i,k)
                            #highest ret
                            #renterprice=df2["Close"].iloc[j+k+2]
                            #renterprice=df2["Low"].iloc[j+k]
                            ###print("&&&&&&&&&&&&&&&&&&&&&&&&&")
                            if df2["SAR_POS_sl"].iloc[j+k]=="DOWN":
                                print("*************")
                                print(df2.iloc[j+k])
                                renterprice=df2["SAR_sl"].iloc[j+k-1]#+3
                            ###print(renterprice)
                            
                            #renterprice=df2["High"].iloc[j+k+1]
                            #if(df2["STX_sl"].iloc[j+k+1]=="DOWN"):
                            #    renterprice=df2["ST_sl"].iloc[j+k+1]
                            ######print("got renterprice "+str(renterprice))
                            ######print(df["Timestamp"].iloc[i])
                            ######print(df2.iloc[j+k])
                            #renterprice=df2["Low"].iloc[j+k+2]
                            
                        if j<=4:
                            j=j+1
                            ######print("j+ candle")
                            ######print(j)
                        #break
                        if j==5:
                            j=0
                            i=i+1
                            ######print("i candle+ after j complete5")
                            ######print(i)
                                
                            
                           #global day
                        if isforbiddentimesl(df,i)==True:
                            while isforbiddentimesl(df,i)==True:
                                i=i+1
                            ######print("DAYOVER--------------")
                            i=i-1
                            day="OVER"
                            position=""
                            trend=""
                            return i 
                        
                        
                            
                    else:
                        ######print("Trend Collapse"+str(df["Timestamp"].iloc[i]))
                        ##modification
                        #i=i+1
                        #######print("Value of I is "+str(i))
                        #####if trend!="":
                        #####    ordertime.append((df2["Timestamp"].iloc[i]))
                        #####    order.append("NONE")
                        #####    exittime.append((df2["Timestamp"].iloc[i]))
                        #####    exit.append("NONE")
                        #####    points.append(0)
                        #####    pnl.append("No Trade")
                        #####    if renter_buy==0:
                        #####        isRenter.append("No")
                        j=0
                        trend=""
                        return i-1
                    
                        
        ##1
        else:
            ######print("SAR or STX==DOWN")
            #i=i+1
            #####if trend!="":
            #####    ordertime.append((df2["Timestamp"].iloc[i]))
            #####    order.append("NONE")
            #####    exittime.append((df2["Timestamp"].iloc[i]))
            #####    exit.append("NONE")
            #####    points.append(0)
            #####    pnl.append("No Trade")
            #####    if renter_buy==0:
            #####        isRenter.append("No")
            ######print("Value of I is "+str(i))
            j=0
            trend=""
            return i-1
        

################################################################################
def SELL_ITER(i,entryprice,df,df2)   :
    ### to fix -5 iteration after buy initaiation check
    i=i+1
    ######print("SELL ITER LOOP")
    low=99999
    position=""
    trend="DOWN"
    renter_sell=0
    renterprice=0
    checkrenter=0
    iterafterfail=0
    afterExit=False
    isRentertag=0
    j=0
    k=0
    passcondn=0
    global day
    global save
    global positiveslip
    save  =0
    adxfilter=100
    global pointstoday
    global datetoday
    global datenow
    datetoday=df["Timestamp"].iloc[i].split("-")[0]
    #if len(order)==0:
    #    datenow=df["Timestamp"].iloc[0].split("-")[0]
    day="NONE"
    #print(pointstoday)
    
    ######### positive slippage includer
    #if df2["High"].iloc[j+k+1]>entryprice+positiveslip and df2["Open"].iloc[j+k+1]>df2["Low"].iloc[j+k]+positiveslip:
    #    entryprice=entryprice+positiveslip
    #else:
    #    return i
        
    while trend=="DOWN":
        if df["STX"].iloc[i-1]=="DOWN" and df["SAR_POS_2"].iloc[i-1]=="DOWN":
            if datetoday!=datenow:
                pointstoday=0
                datenow=datetoday
                #pointstoday=pointstoday+points[-1]
            if renterprice>0 :
                
                entryprice=renterprice
                
                ###print("^^^^^^^^^^^^^^^^^^^^^^")
                ###print(entryprice)
            if renter_sell>0:
                entryprice=renter_sell
            k=jfetch(df,i,k)        
            ######print("ITERATING "+str(entryprice))
            
            ######print(df2["Timestamp"].iloc[j+k])
            
            #######print("Value of I is "+str(i))
            ######print(df2["SAR_POS_sl"].iloc[j+k])
            ######print(df2["STX_sl"].iloc[j+k])
            
            #########
            
            ##########
            if ((df2["SAR_POS_sl"].iloc[j+k]=="DOWN" and  df2["STX_sl"].iloc[j+k]=="DOWN") or (df2["SAR_POS_sl"].iloc[j+k]=="DOWN" and renterprice>0) ) :# and df["RSI"].iloc[i-1]<40 and df["CCI"].iloc[i-1]<50):
                
                if renter_sell>0:
                    isRentertag=1
                    isRenter.append("Yes")
                    signaltime.append(df2["Timestamp"].iloc[i])
                    entryprice=renter_sell
                    renter_sell=0
                if renterprice>0:
                    entryprice=renterprice
                    ###print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                    ###print(entryprice)
                    renterprice=-1
                    ##modification
                    #j=0
                    renterprice=0
                entryprice=entryprice    
                iterafterfail=0
                ######print(i)
                ######print(entryprice)
                if (df2["Low"].iloc[j+k] <= entryprice and position=="") and (df2["RSI_sl"].iloc[j+k-1]<3) and should_take_trade(i, df, df2, is_buy=False):# and(df["MA"].iloc[i-1]>entryprice) :#and ( df["RSI"].iloc[i-1]<10 and df["CCI"].iloc[i-1]<0 and df2["RSI_sl"].iloc[j+k-1]<0 and df2["MADIST_sl"].iloc[j+k-1]==1)  :
                    if datetoday!=datenow:
                        pointstoday=0
                        datenow=datetoday
                    #position="open"
                    ##if (df2["Low"].iloc[j+k] <= entryprice and position=="") :#and (df2["RSI_sl"].iloc[j+k-1]<10 and df["RSI"].iloc[i-1]<15)
                    #and df2["RSI_sl"].iloc[j+k-1]<5 and df["RSI"].iloc[i-1]<5 and df2["CCI_sl"].iloc[j+k-1]<100 
                    #if (  df2["MADIST_sl"].iloc[j+k-1]==1  ):#and df["CCI"].iloc[i-1]<50 )  :#df["RSI"].iloc[i-1]<10 and df["CCI"].iloc[i-1]<0 and df2["RSI_sl"].iloc[j+k-1]<0 and
                    #    passcondn=1
                    #else:
                    #    return i
                    #passcondn=0
                    renterprice=-1
                    ######print("SELL ORDER at " + str(entryprice) )
                    #place buy order code here
                    #sellOrder(symbol,token,entryprice)
                    ######print("SELL ORDER PLACED"+str(df2["Timestamp"].iloc[j+k]))
                    ordertime.append((df2["Timestamp"].iloc[j+k]))
                    
                    
                    order.append(entryprice)
                    rsientry.append(df["RSI"].iloc[i-1])
                    rsi_slentry.append(df2["RSI_sl"].iloc[j+k-1])
                    stochasticList.append(df["Stochastic"].iloc[i-1])
                    stochasticSlList.append(df2["Stochastic"].iloc[j+k-1])
                    m3.append(df2["momentum_3"].iloc[j+k-1])
                    m5.append(df2["momentum_5"].iloc[j+k-1])
                    vol_std.append(df2["vol_std_10"].iloc[j+k-1])
                    #rsientry.append(df["MADIST"].iloc[i-1])
                    #rsi_slentry.append(df2["MADIST_sl"].iloc[j+k-1])
                    if isRentertag!=1:
                        isRenter.append("No")
                    isRentertag=0
                    #telegram_bot_sendtext("SELL at "+str(entryprice))
                    #telegram_bot_sendtext(str(df2["Timestamp"].iloc[j+k]))
                    ### exit function here
                    if save>0:
                        entryprice=save
                        save=0
                    ###print("^^^^^^^^^^^^^^^^^^^^^^")
                    ###print(entryprice)
                    sellsignal.append(0)
                   
                    i,j,renter_sell=SELL_EXIT(entryprice,i,j,df,df2)
                    if datetoday==datenow:
                            pointstoday=pointstoday+points[-1]
                            print(pointstoday)
                    
                   #global day
                    position=""
                    afterExit=True
                    if day=="OVER":
                        ######print("DayOver")
                        return i
                    if isforbiddentimesl(df,i)==True:
                        while isforbiddentimesl(df,i)==True:
                            i=i+1
                        ######print("DAYOVER--------------")
                        i=i-1
                        day="OVER"
                        position=""
                        trend=""
                        return i
                    
                    #buyOrder(symbol,token,entryprice)
                    
                    if isRentertag!=1:
                        isRenter.append("No")
                        isRentertag=0
                    
                    #telegram_bot_sendtext("BUY at "+str(entryprice))
                    #telegram_bot_sendtext(str(df2["Timestamp"].iloc[j+k]))
                    
                    
                position=""
                if renter_sell>0:
                    print(renter_sell)
                    ######print("running to check reenter condition")
                #####modification1504
                if df["STX"].iloc[i]=="UP" or df["SAR_POS_2"].iloc[i]=="UP":
                    return i-1
                    
                
                ##### use j iterator here
                if j<=4:
                    j=j+1
                    ######print("j+ candle")
                    ######print(j)
                #break
                if j==5:
                    j=0
                    i=i+1
                    ######print("i candle+ after j complete5")
                    ######print(i)
            
                if isforbiddentimesl(df,i)==True:
                    while isforbiddentimesl(df,i)==True:
                        i=i+1
                    ######print("DAYOVER--------------")
                    i=i-1
                    day="OVER"
                    position=""
                    trend=""
                    return i               
                                
            ##2
            else:
                print(" failed recheck master")
                #######print("Value of I is "+str(i))               
                ######print("WAIT OVER"+str(df["Timestamp"].iloc[i]))
                ######print("SLframe time"+str(df2["Timestamp"].iloc[j+k]))
                ###### look maybe error here
                renter_buy=0
                
                if df["SAR_POS_2"].iloc[i]=="DOWN" and  df["STX"].iloc[i]=="DOWN": 
                    ######print("SAR AND ST INTACT"+str(df["Timestamp"].iloc[i]))
                    ######print("CHECK SL FRAME ST AND SAR")
                    #modification 1104
                    
                        #break
                    #k=jfetch(df,i,k)
                    
                    #if df2["STX_sl"].iloc[j+k]=="UP" and df2["SAR_POS_sl"].iloc[j+k]=="DOWN":
                    #    #renterprice=df2["High"].iloc[j+k]
                    #    #renterprice=df2["SAR_sl"].iloc[j+k]
                    #    renterprice=df2["SAR_sl"].iloc[j+k]
                    #    ######print("got renterprice "+str(renterprice))
                    #if df["SAR_POS_2"].iloc[i]=="UP" and df2["STX_sl"].iloc[j+k]=="DOWN" and df2["SAR_POS_sl"].iloc[j+k]=="DOWN":
                    #    renterprice=df2["SAR_sl"].iloc[j+k]
                    #    ######print("got renterprice "+str(renterprice))
                    #    ##### use j iterator here                                
                    
                    if (df2["SAR_POS_sl"].iloc[j+k]=="UP" or df2["STX_sl"].iloc[j+k]=="UP") :#and (df2["SAR_POS_sl"].iloc[j+k+1]=="DOWN" or df2["STX_sl"].iloc[j+k+1]=="DOWN"):
                        #k=jfetch(df,i,k)
                        #highest ret
                        #renterprice=df2["Close"].iloc[j+k+2]
                        #renterprice=df2["Low"].iloc[j+k]
                        ###print("&&&&&&&&&&&&&&&&&&&&&&&&&")
                        if df2["SAR_POS_sl"].iloc[j+k]=="UP":
                            print("*************")
                            print(df2.iloc[j+k])
                            renterprice=df2["SAR_sl"].iloc[j+k-1]#+3
                        ###print(renterprice)
                        
                        #renterprice=df2["Low"].iloc[j+k+1]
                        #if(df2["STX_sl"].iloc[j+k+1]=="UP"):
                        #    renterprice=df2["ST_sl"].iloc[j+k+1]
                        ######print("got renterprice "+str(renterprice))
                        ######print(df["Timestamp"].iloc[i])
                        ######print(df2.iloc[j+k])
                        #renterprice=df2["Low"].iloc[j+k+2]
                        
                    if j<=4:
                        j=j+1
                        ######print("j+ candle")
                        ######print(j)
                    #break
                    if j==5:
                        j=0
                        i=i+1
                        ######print("i candle+ after j complete5")
                        ######print(i)
                        
                        
                       #global day
                    if isforbiddentimesl(df,i)==True:
                        while isforbiddentimesl(df,i)==True:
                            i=i+1
                        ######print("DAYOVER--------------")
                        i=i-1
                        day="OVER"
                        position=""
                        trend=""
                        return i 
                    
                        
                            
                else:
                    ######print("Trend Collapse"+str(df["Timestamp"].iloc[i]))
                    ##modification
                    #i=i+1
                    #######print("Value of I is "+str(i))
                    #####if trend!="":
                    #####    ordertime.append((df2["Timestamp"].iloc[i]))
                    #####    order.append("NONE")
                    #####    exittime.append((df2["Timestamp"].iloc[i]))
                    #####    exit.append("NONE")
                    #####    points.append(0)
                    #####    pnl.append("No Trade")
                    #####    if renter_buy==0:
                    #####        isRenter.append("No")
                    j=0
                    trend=""
                    return i-1
                    
                        
        ##1
        else:
            ######print("SAR or STX==UP")
            #i=i+1
            #####if trend!="":
            #####    ordertime.append((df2["Timestamp"].iloc[i]))
            #####    order.append("NONE")
            #####    exittime.append((df2["Timestamp"].iloc[i]))
            #####    exit.append("NONE")
            #####    points.append(0)
            #####    pnl.append("No Trade")
            #####    if renter_buy==0:
            #####        isRenter.append("No")
            ######print("Value of I is "+str(i))
            j=0
            trend=""
            return i-1
    
            
                    
multiplier2=1
multiplier3=1
atr3counter=0
b3=5
def BUY_EXIT(entryprice,i,j,df,df2):
    global b3
    entryprice=entryprice
    exititer=0
    sar=0
    global day
    global renterloopfilter
    global sldev
    renterloopfilter=0
    print("***************")
    print(entryprice)
    st=0
    ###print("BUY EXIT LOOP")
    renter_buy=0
    high=0
    position="open"
    afterExit=False
    #multiplier=1.5
    global deviation
    global multiplier
    global multiplier2
    global multiplier3
    
    
    #trial
    #multiplier=1.8
    #nf
    #multiplier=1.25
    ########## to check condition afer entry candle close 
    #j=j+1
#     buffer=entryprice-df["ATR_buffer"].iloc[i]
    k=0
    k=jfetch(df,i,k)
    ATR_sl=df["ATR"].iloc[i]*multiplier
    #buffer=(ATR_sl)*2
    #high1=df.iloc["High"].iloc[i]
    atr=entryprice-ATR_sl
    tsl=atr
    itersl=0
#     multiplier2=1
    ATR_sl2=df["ATR"].iloc[i]*multiplier2
    
    buffer=entryprice-df["ATR_buffer"].iloc[i]
    
    atr2=entryprice-ATR_sl2
    
    ATR_sl3=df2["ATR"].iloc[j+k-b3]*multiplier3
    bufferatr3=entryprice-ATR_sl3
    print(j+k)
    print("1111111111")
    #buffer=atr
    #bufferatr3=atr
    tsl=atr
    prevtsl=tsl
    global prevtslcounter
    
    global buffer3breachexit
    ###print(tsl)
    while position=="open":
        #start=timeit.default_timer()
        if position=="open":
            
            exititer=exititer+1
            ###print("EXIT ITERATING")
            k=jfetch(df,i,k)
            ##########################
            
            if df2["High"].iloc[j+k-1]>high:
                high=df2["High"].iloc[j+k-1]
                
            if breakevenSwitch and df2["High"].iloc[j+k]-entryprice>=breakevenLimit:
                print("BREAKEVEN TSL IN ACTION........................... ",high)
                #tsl=breakevenTsl
                tsl=breakevenTsl+(high-entryprice-breakevenLimit)
            #high=df2["High"].iloc[j+k-1]
            print("High= "+str(high))
            print("Actual high"+str(df2["High"].iloc[j+k-1]))
            ####print("BUFFER= "+str(buffer))
            pointsmade=0
            ### testing purpose only
            #atr=high-buffer
            
            ###print("atr"+str(atr))
            if itersl==0:
                if df2["STX_sl"].iloc[j+k]=="UP":
                    st=float(df2["ST_sl"].iloc[j+k])
                    print("st"+str(st))
                if df2["SAR_POS_sl"].iloc[j+k]=="UP":
                    sar=float(df2["SAR_sl"].iloc[j+k])
                    print("sar"+str(sar))
            else:
                if df2["STX_sl"].iloc[j+k-1]=="UP":
                    st=float(df2["ST_sl"].iloc[j+k-1])
                    print("st"+str(st))
                if df2["SAR_POS_sl"].iloc[j+k-1]=="UP":
                    sar=float(df2["SAR_sl"].iloc[j+k-1])
                    print("sar"+str(sar))
            print("SAR"+str(sar))
            print("ATR"+str(atr))
            print("ATR2"+str(atr2))
            
#             ATR_sl3=df2["ATR"].iloc[j+k]*multiplier3
#             bufferatr3=high-ATR_sl3
                
            
            #if df2["STX_sl"].iloc[j+k]=="UP" and df2["SAR_POS_sl"].iloc[j+k]=="UP":
            if sar>0 or st>0:
                    tsl1=gettsl(atr,st,sar,"BUY")
                    print(str(tsl1)+"////////////////")
            
            else:
                tsl1=atr2
                tsl=atr2
                
            if tsl1>tsl:
                tsl=tsl1
                
            ##buffer enhancement
            if tsl<buffer:
                tsl=buffer
                print("buffer????????????"+str(buffer))
            if tsl<bufferatr3:
                if(bufferatr3==0):
                    print("Pass")
                else:
                    global atr3counter
                    atr3counter=atr3counter+1
                    tsl=bufferatr3
                    print("buffer3/////////////////"+str(ATR_sl3))
                
            
            if tsl<df["Low"].iloc[i-1]      :
                tsl=df["Low"].iloc[i-1]
            print("Final TSL"+str(tsl))
            #if tsl>entryprice+buffer:
            #    tsl=entryprice+buffer
            itersl=1       
            tsl=tsl-sldev
            ####################
            #if df2["Open"].iloc[j+k]<tsl:
            #    tsl=prevtsl
            #    prevtslcounter=prevtslcounter+1
            #else:
            #    prevtsl=tsl
            print("tsl"+str(tsl))
            print(str(df2["Timestamp"].iloc[j+k])+" TRAILING SL: "+str(tsl))
            ###print(j+k)
            if tsl>entryprice and itersl==0:
                buysignal.append(3)
                print("EXITING THE POSITION because entry not valid"+str(df2["Timestamp"].iloc[j+k]))
                print("Entry was at: "+str(entryprice))
                print("Exit was at: "+str(tsl))
                pointsmade=0
                #telegram_bot_sendtext(str(pointsmade))
                points.append(pointsmade)
                exittime.append((df2["Timestamp"].iloc[j+k]))
                rsi.append(df["DMI+"].iloc[i-1]+df["DMI-"].iloc[i] )
                rsi_sl.append(df["DMI+"].iloc[i+1]+df["DMI-"].iloc[i+1] )
                exit.append(tsl)
                pnl.append("0")
                print("Points: "+str(pointsmade))
                position=""
                renter_buy=0
                ###print("Rentry price : "+ str(renter_sell))
                
                return (i,j,renter_buy) 
            if tsl>df2["Low"].iloc[j+k]:
                buysignal.append(3)
                print("EXITING THE POSITION"+str(df2["Timestamp"].iloc[j+k]))
                print("Entry was at: "+str(entryprice))
                if df2["Open"].iloc[j+k]<tsl:
                    tsl=df2["Open"].iloc[j+k]
                    
                    buffer3breachexit=buffer3breachexit+1
                
                print("Exit was at..: "+str(tsl))
                pointsmade=tsl-entryprice
                #telegram_bot_sendtext(str(pointsmade))
                points.append(pointsmade)
                exittime.append((df2["Timestamp"].iloc[j+k]))
                rsi.append(df["DMI+"].iloc[i-1]+df["DMI-"].iloc[i] )
                rsi_sl.append(df["DMI+"].iloc[i+1]+df["DMI-"].iloc[i+1] )
                exit.append(tsl)
                if pointsmade>0:
                    pnl.append("Profit")
                else:
                    pnl.append("Loss")
                ###print("Points: "+str(pointsmade))
                position=""
                #if df2["SAR_sl"].iloc[j+k]=="UP":
                #    renter_buy=getrenterprice(i,j,df,df2,"BUY")
                #else:
                #    renter_buy=0
                renter_buy=getrenterprice(i,j,df,df2,"BUY")
                print("Rentry price : "+ str(renter_buy))
                
                return(i,j,renter_buy)
            
            itersl=1
            if j<=4:
                ###print("j++ candle")
                ###print(j)
                j=j+1
            if j==5:
                j=0
                i=i+1
                #ATR_sl=df["ATR"].iloc[i]
                #mATR=(ATR_sl)*2
                #
                #if mATR>buffer:
                #    buffer=mATR
                ATR_sl=df["ATR"].iloc[i]*multiplier
                atr=high-ATR_sl
                
                ATR_sl2=df["ATR"].iloc[i]*multiplier2
                #atr2=high-ATR_sl2
                atr2=high-ATR_sl
                buffer=high-df["ATR_buffer"].iloc[i]
                ###print("i candle+ after j complete5")
                
                ##### get df2slbasedatrbuffer on completion of 10min candle only
                ATR_sl3=df2["ATR"].iloc[j+k-b3]*multiplier3
                
                print("ATRbuffer3 updateddddd !!!!!!!!!!!!!!!!!!"+str(ATR_sl3))
                bufferatr3=high-ATR_sl3
                ###print(i)
                print("buffer"+str(buffer))
                print("ATR3_buffer"+str(bufferatr3))
            if isforbiddentimesl(df,i,k)==True:
                #k=jfetch(df,i,k)
                buysignal.append(3)
                print("EXITING THE POSITION"+str(df2["Timestamp"].iloc[j+k]))
                print("Entry was at: "+str(entryprice))
                print("Exit was at: "+str(df2["Open"].iloc[j+k+5]))
                pointsmade=df2["Open"].iloc[j+k+5]-entryprice
                #telegram_bot_sendtext(str(pointsmade))
                points.append(pointsmade)
                ### j+k+5 because we are taking calculation of slframe from same point instead of 5 ahead
                exittime.append((df2["Timestamp"].iloc[j+k+5]))
                rsi.append(df["DMI+"].iloc[i-1]+df["DMI-"].iloc[i] )
                rsi_sl.append(df["DMI+"].iloc[i+1]+df["DMI-"].iloc[i+1] )
                exit.append(df2["Open"].iloc[j+k+5])
                if pointsmade>0:
                    pnl.append("Profit")
                else:
                    pnl.append("Loss")
                print("Points: "+str(pointsmade))
                position=""
                #renter_buy=getrenterprice(i,j,df,df2,"BUY")
                print("Rentry price : "+ str(renter_buy))
                if isforbiddentimesl(df,i)==True:
                    while isforbiddentimesl(df,i)==True:
                        i=i+1
                    ###print("DAYOVER--------------")
                    i=i-1
                    day="OVER"
                    position=""
                    trend=""
                    #return i
                
                day="OVER"
                return(i,j,renter_buy)
                
            
        else:
            ###print("no open position")
            position=""
            i=i+1
            return(i,j,renter_buy)
            break
    

##df["DMI+"].iloc[i-1]+df["DMI-"].iloc[i-1] df2["RSI_sl1"].iloc[j+k-1]


#######################################SELLEXIT
def SELL_EXIT(entryprice,i,j,df,df2):
    entryprice=entryprice
    global b3
    global sldev
    global multiplier
    global multiplier2
    print("***************")
    print(entryprice)
    exititer=0
    ########## to check condition afer entry candle close 
    #j=j+1
    global day
    global renterloopfilter
    renterloopfilter=0
    buffer=entryprice+df["ATR_buffer"].iloc[i]
    ###print("SELL EXIT LOOP")
    low=99999
    itersl=0
    sar=0
    st=0
    renter_sell=0
    position="open"
    afterExit=False
    global deviation
    global multiplier3
    
    #multiplier=1.5
    #trial
    #multiplier=1.8
    #nf
    #multiplier=1.25
    k=0
    k=jfetch(df,i,k)
    #buffer=(ATR_sl)*2
    #low1=df["Low"].iloc[i]
    ATR_sl=df["ATR"].iloc[i]*multiplier
    atr=ATR_sl+entryprice
    
#     multiplier2=1
    
#     buffer=entryprice+df["ATR_buffer"].iloc[i]

    ATR_sl2=df["ATR"].iloc[i]*multiplier2
    atr2=ATR_sl2+entryprice
    
    ATR_sl3=df2["ATR"].iloc[j+k-b3]*multiplier3
    
    bufferatr3=entryprice+ATR_sl3
    ###print(tsl)
    #buffer=atr
    #bufferatr3=atr
    tsl=atr
    prevtsl=tsl
    global buffer3breachexit
    global prevtslcounter
    
    while position=="open":
        
        
        if position=="open":
            
            print("+++++++++++++++++++++++++ exit loop iter")
            ####################################    
            exititer=exititer+1    
            ###print("EXIT ITERATING")
            ##########################
            k=jfetch(df,i,k)
            
            
            
            
            if df2["Low"].iloc[j+k-1]<low:
                low=df2["Low"].iloc[j+k-1]
                
            if breakevenSwitch and entryprice-df2["Low"].iloc[j+k]>=breakevenLimit:
                print("BREAKEVEN TSL IN ACTION........................... ",low)
                #tsl=breakevenTsl
                tsl=breakevenTsl+(entryprice-low-breakevenLimit)  
                
                
            #pointsmade=0
            #low=df2["Low"].iloc[j+k-1]
            print("Low= "+str(low))
            print("Actual low "+str(df2["Low"].iloc[j+k-1]))
            ####print("BUFFER= "+str(buffer))
            
            
            #atr=low+buffer
            ###print("atr"+str(atr))
            ####print("low"+str(low))
            if itersl==0:
                if df2["STX_sl"].iloc[j+k]=="DOWN":
                    st=float(df2["ST_sl"].iloc[j+k])
                    print("st"+str(st))
                if df2["SAR_POS_sl"].iloc[j+k]=="DOWN":
                    sar=float(df2["SAR_sl"].iloc[j+k])
            else:
                if df2["STX_sl"].iloc[j+k-1]=="DOWN":
                    st=float(df2["ST_sl"].iloc[j+k-1])
                    print("st"+str(st))
                if df2["SAR_POS_sl"].iloc[j+k-1]=="DOWN":
                    sar=float(df2["SAR_sl"].iloc[j+k-1])

            print("SAR"+str(sar))
            print("ATR"+str(atr))
            print("ATR2"+str(atr2))
            
#             ATR_sl3=df2["ATR"].iloc[j+k]*multiplier3
#             bufferatr3=low+ATR_sl3
            
            if sar>0 or st>0:
                tsl1=gettsl(atr,st,sar,"SELL")
                print(str(tsl1)+"////////////////")
                
            
            else:
                tsl1=atr2
                tsl=atr2
            if tsl1<tsl:
                tsl=tsl1
            
            ##buffer enhancement
            if tsl>buffer:
                tsl=buffer
                print("buffer????????????"+str(buffer))
            if tsl>bufferatr3:
                if(bufferatr3==0):
                    print("Pass")
                else:
                    global atr3counter
                    atr3counter=atr3counter+1
                    tsl=bufferatr3
                    print("buffer3/////////////////"+str(ATR_sl3))
            
            if tsl>df["High"].iloc[i-1]:
                
                tsl=df["High"].iloc[i-1] 
            print("FINL TSL"+str(tsl))
                #######
            #if tsl<entryprice-buffer:
            #    tsl=entryprice-buffer
            
                    
            
            tsl=tsl+sldev
            
            ####################
            #if df2["Open"].iloc[j+k]>tsl:
            #    tsl=prevtsl
            #    prevtslcounter=prevtslcounter+1
            #else:
            #    prevtsl=tsl
            print("TSL"+str(tsl))
            print(str(df2["Timestamp"].iloc[j+k])+" TRAILING SL: "+str(tsl))
            ###print(j+k)
            if tsl<entryprice and itersl==0:
                sellsignal.append(3)
                print("EXITING THE POSITION because entry not valid"+str(df2["Timestamp"].iloc[j+k]))
                print("Entry was at: "+str(entryprice))
                pointsmade=0
                #telegram_bot_sendtext(str(pointsmade))
                points.append(pointsmade)
                exittime.append((df2["Timestamp"].iloc[j+k]))
                rsi.append(df["DMI+"].iloc[i-1]+df["DMI-"].iloc[i] )
                rsi_sl.append(df["DMI+"].iloc[i+1]+df["DMI-"].iloc[i+1] )
                exit.append(tsl)
                pnl.append("0")
                print("Points: "+str(pointsmade))
                position=""
                renter_sell=0
                ###print("Rentry price : "+ str(renter_sell))
                
                return (i,j,renter_sell) 
                
            if tsl<df2["High"].iloc[j+k]:
                sellsignal.append(3)
                print("EXITING THE POSITION"+str(df2["Timestamp"].iloc[j+k]))
                print("Entry was at: "+str(entryprice))
                if df2["Open"].iloc[j+k]>tsl:
                    
                    
                    tsl=df2["Open"].iloc[j+k]
                    buffer3breachexit=buffer3breachexit+1
                
                print("Exit was at...: "+str(tsl))
                pointsmade=entryprice-tsl
                #telegram_bot_sendtext(str(pointsmade))
                points.append(pointsmade)
                exittime.append((df2["Timestamp"].iloc[j+k]))
                rsi.append(df["DMI+"].iloc[i-1]+df["DMI-"].iloc[i] )
                rsi_sl.append(df["DMI+"].iloc[i+1]+df["DMI-"].iloc[i+1] )
                exit.append(tsl)
                if pointsmade>0:
                    pnl.append("Profit")
                else:
                    pnl.append("Loss")
                print("Points: "+str(pointsmade))
                position=""
                #if df2["SAR_sl"].iloc[j+k]=="DOWN":
                #    renter_sell=getrenterprice(i,j,df,df2,"SELL")
                #else:
                #    renter_sell=0
                renter_sell=getrenterprice(i,j,df,df2,"SELL")
                print("Rentry price : "+ str(renter_sell))
                
                return (i,j,renter_sell)  
            itersl=1
            if j<=4:
                ###print("j++ candle")
                ###print(j)
                j=j+1
            if j==5:
                j=0
                i=i+1
                #ATR_sl=df["ATR"].iloc[i]
                #mATR=(ATR_sl)*2
                #
                #if mATR>buffer:
                #    buffer=mATR
                ATR_sl=df["ATR"].iloc[i]*multiplier
                ATR_sl2=df["ATR"].iloc[i]*multiplier2
                #atr2=low+ATR_sl
                atr=low+ATR_sl
                atr2=low+ATR_sl
                
                buffer=low+df["ATR_buffer"].iloc[i]
                
                ###print("i candle+ after j complete5")
                ##### get df2slbasedatrbuffer on completion of 10min candle only
                ATR_sl3=df2["ATR"].iloc[j+k-b3]*multiplier3
                print("ATRbuffer3 updateddddd !!!!!!!!!!!!!!!!!!"+str(ATR_sl3))
                bufferatr3=low+ATR_sl3
                print("buffer"+str(buffer))
                print("ATR3_buffer"+str(bufferatr3))
                ###print(i)
            if isforbiddentimesl(df,i,k)==True:
                sellsignal.append(3)
                #k=jfetch(df,i,k)
                print("EXITING THE POSITION"+str(df2["Timestamp"].iloc[j+k]))
                print("Entry was at: "+str(entryprice))
                print("Exit was at...: "+str(df2["Open"].iloc[j+k+5]))
                pointsmade=entryprice-df2["Open"].iloc[j+k+5]
                #telegram_bot_sendtext(str(pointsmade))
                rsi.append(df["DMI+"].iloc[i-1]+df["DMI-"].iloc[i] )
                rsi_sl.append(df["DMI+"].iloc[i+1]+df["DMI-"].iloc[i+1] )
                points.append(pointsmade)
                exittime.append((df2["Timestamp"].iloc[j+k+5]))
                exit.append(df2["Open"].iloc[j+k+5])
                if pointsmade>0:
                    pnl.append("Profit")
                else:
                    pnl.append("Loss")
                print("Points: "+str(pointsmade))
                position=""
                #renter_sell=getrenterprice(i,j,df,df2,"SELL")
                print("Rentry price : "+ str(renter_sell))
                if isforbiddentimesl(df,i)==True:
                    while isforbiddentimesl(df,i)==True:
                        i=i+1
                    ###print("DAYOVER--------------")
                    i=i-1
                    day="OVER"
                    position=""
                    trend=""
                    #return i
                
                
                
                day="OVER"
                return(i,j,renter_sell) 
            
            
            
            
        else:
            ###print("no open position")
            position=""
            i=i+1
            return(i,j,renter_sell)
            break

def isforbiddentime(df,i,j=0):
    if forbiddenKillSwitch:
        return False
    timestamp = df["Timestamp"].iloc[i]
    time_str = timestamp.split()[1][:5]  # Extract HH:MM
    #print(time_str  )
    for start, end in forbidden_time_ranges:
        start_hour, start_minute = map(int, start.split(':'))
        end_hour, end_minute = map(int, end.split(':'))
        
        if start_hour < end_hour:
            if start <= time_str < end:
                return True
        else:
            if time_str >= start or time_str < end:
                return True
    return False

 
def forbiddentime(df,i,j=0):
    
    timestamp = df["Timestamp"].iloc[i]
    time_str = timestamp.split()[1][:5]  # Extract HH:MM
    for start, end in forbidden_time_ranges:
        start_hour, start_minute = map(int, start.split(':'))
        end_hour, end_minute = map(int, end.split(':'))
        
        if start_hour < end_hour:
            if start <= time_str < end:
                i += 1
        else:
            if time_str >= start or time_str < end:
                i += 1
    return i
def isforbiddentimesl(df,i,j=0):
    if forbiddenKillSwitch:
        return False
    timestamp = df["Timestamp"].iloc[i]
    time_str = timestamp.split()[1][:5]  # Extract HH:MM
    #print(time_str  )
    for start, end in forbidden_time_ranges:
        start_hour, start_minute = map(int, start.split(':'))
        end_hour, end_minute = map(int, end.split(':'))
        
        if start_hour < end_hour:
            if start <= time_str < end:
                return True
        else:
            if time_str >= start or time_str < end:
                return True
    return False

 
def forbiddentimesl(df,i,j=0):
    
    timestamp = df["Timestamp"].iloc[i]
    time_str = timestamp.split()[1][:5]  # Extract HH:MM
    for start, end in forbidden_time_ranges:
        start_hour, start_minute = map(int, start.split(':'))
        end_hour, end_minute = map(int, end.split(':'))
        
        if start_hour < end_hour:
            if start <= time_str < end:
                i += 1
        else:
            if time_str >= start or time_str < end:
                i += 1
    return i

def gettsl(atr,st,sar,position_type="BUY"):
    #if atr>st+12:
    #    tsl=atr
    #if atr<st+12:
    #    tsl=st
    tsl2=0
    global tslbuffer
    print(sar)
    print(atr)
    print(st)
    tsl1=atr   
    tsl2=sar
    #tsl2=st
    #if sar+15>st and sar>st:
    #    tsl2=st
    #    
    #if sar+15>st and sar<st:
    #    tsl2=sar
    #
    #if sar+15<st:
    #    tsl2=st
    #if sar==0 or sar==None:
    #    tsl2=st
    #if st==0 or st==None:
    #    tsl2=sar
        
    if tsl2==0:
        tsl2=atr
        
    if position_type=="BUY":    
        if tsl1>tsl2+tslbuffer:
            print("ATR is SL")
            tsl=tsl1-tslbufferfinal
        
        else:
            print("SAR is SL")
            tsl=tsl2-tslbufferfinal
    if position_type=="SELL":    
        if tsl1<tsl2-tslbuffer:
            print("ATR is SL")
            tsl=tsl1+tslbufferfinal
        else:
            print("SAR is SL")
            tsl=tsl2+tslbufferfinal
        
            
    
    
    return tsl



def jfetch(df,i,j):

        
    df["Timestamp"].iloc[i]
    if j==0:
        j=int(i*((resolution/resolution_sl)-.08))

    while (df["Timestamp"].iloc[i]).split(" ") != (df2["Timestamp"].iloc[j]).split(" "):
        
        
        j=j+1
    
    #return j-5
    return j#+5#-5
def isOpencandle(df, i):
    if openCandleTradeSwitch==False:
        return False
    timestamp = df["Timestamp"].iloc[i]
    time_str = timestamp.split()[1][:5]  # Extract HH:MM
    
    for _, end in forbidden_time_ranges:
        if time_str == end:
            return True
    return False  

def telegram_bot_sendtext(bot_message):

    bot_token = '5126888820:AAHLj_vfUBxmlpj84CamYbjr7C6X2MWAx-o'
    bot_chatID = '910701118'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

Stochastic_dict=[]
Stochastic_Store=[]
def Stochastic_Check(df,i,direction="BUY"):
#     Stochastic_dict.append(df["Stochastic"].iloc[i])
    if direction=="BUY" and df["Stochastic"].iloc[i]>=STOCHASTIC_BUY_LIMIT:
        return True
    elif direction=="SELL" and df["Stochastic"].iloc[i]<=STOCHASTIC_SELL_LIMIT:
        return True
    else:
        return True

def meanadx(df,i,position):
    #ADX CHECK
    global dmidiff
    #dmidiff=14
    #dmidiff=10
    #adxval=45.7
    #adxval=25
    global adxval
    
    if (df["ADX"].iloc[i] >= adxval and (df["DMI+"].iloc[i] <=df["DMI-"].iloc[i] and abs((df["DMI-"].iloc[i]) -df["DMI+"].iloc[i]) >=dmidiff)==True)==True and position=="BUY" :
        print ("dmidiff= "+str(abs(abs(df["DMI-"].iloc[i]) -df["DMI+"].iloc[i])))
        return True
    if (df["ADX"].iloc[i] >= adxval and (df["DMI+"].iloc[i] >=df["DMI-"].iloc[i] and abs(df["DMI+"].iloc[i] -(df["DMI-"].iloc[i])) >=dmidiff)==True)==True and position=="SELL" :
        print ("dmidiff= "+str(abs(abs(df["DMI-"].iloc[i]) -df["DMI+"].iloc[i])))
        return True
    else: 
        return False

def getrenterprice(i,j,df,df2,position_type):
    #df=getmasterdata(resolution)
    
    global rentrytrade
    rentrytrade=1
    renterprice=0
    k=jfetch(df,i,0)
    print(df2["SAR_POS_sl"].iloc[j+k])
    print(df["SAR_POS_2"].iloc[i])
    if position_type=="BUY":
        renterprice=99999
        #df2=getslframedata(resolution_sl)
        #if df2["STX_sl"].iloc[j+k+3]=="UP" or df2["SAR_POS_sl"].iloc[j+k+3]=="UP":
        if df2["STX_sl"].iloc[j+k]=="UP" or df2["SAR_POS_sl"].iloc[j+k]=="UP":
            #renterprice=df["High"].iloc[i]
            ####highest ret
            renterprice=df2["High"].iloc[j+k-1]#+5
            #!st try
            #renterprice=df2["High"].iloc[j+k-1]
            return renterprice
        else:
            return renterprice
        if  df["SAR_POS_2"].iloc[i]=="UP" or df2["SAR_POS_sl"].iloc[j+k]=="DOWN":
            #renterprice=df["Low"].iloc[i]
            ####highest ret
            renterprice=df2["SAR_sl"].iloc[j+k-1]#-5z
            #1st try
            #renterprice=df2["Low"].iloc[j+k-1]
            return renterprice
        else:
            return renterprice
    if position_type=="SELL":
        renterprice=0
        #df2=getslframedata(resolution_sl)
        #if df2["STX_sl"].iloc[j+k+3]=="DOWN" or df2["SAR_POS_sl"].iloc[j+k+3]=="DOWN":
        if df2["STX_sl"].iloc[j+k]=="DOWN" or df2["SAR_POS_sl"].iloc[j+k]=="DOWN":
            #renterprice=df["Low"].iloc[i]
            ####highest ret
            renterprice=df2["Low"].iloc[j+k-1]#-5
            #1st try
            #renterprice=df2["Low"].iloc[j+k-1]
            return renterprice
        else:
            return renterprice
       
        if  df["SAR_POS_2"].iloc[i]=="DOWN" or df2["SAR_POS_sl"].iloc[j+k]=="UP":
            #renterprice=df["Low"].iloc[i]
            ####highest ret
            renterprice=df2["SAR_sl"].iloc[j+k-1]#-5
            #1st try
            #renterprice=df2["Low"].iloc[j+k-1]
            return renterprice
        else:
            return renterprice
    else:
        return 0
    
    
signaltime=[]
ordertime=[]
order=[]

exittime=[]
exit=[]
ordertype=[]
points=[]
pnl=[]
isRenter=[]
day=None
pip_place_val=1
csbuffer=3/pip_place_val
trend=""
resolution=5
exitfunc=0
resolution_sl=5


# signaltime=[]
m3=[]
m5=[]
vol_std=[]
buysignal=[]
sellsignal=[]
stochasticList=[]
stochasticSlList=[]
atr3counter=0
ordertime=[]
renterprice=0
renterloopfilter=0
buffer3breachexit=0
order=[]
rentrytrade=0
exittime=[]
exit=[]
ordertype=[]
points=[]
pnl=[]
isRenter=[]
exit_price_list=[]
pointstoday=0
datetoday=0
datenow=0
rsi=[]
rsientry=[]
rsi_sl=[]
rsi_slentry=[]
day=None
save=0
#### for nf 
#buffer=80
#telegram_bot_sendtext("------------------------------------------------------------------------------")
points=[]
i=0
iteration=0
save=0
positiveslip=0
deviation=0
sldev=20
adxval=0
idealADX=15
#atr_mult=0.7
dmidiff=10
## decreasing losing trades with overall number of trades
dmidiff=30
multiplier=1
multiplier=1.5
#multiplier=2.5
multiplier2=1.2
multiplier3=1.5 #.5
buffer=200
###trial 2023 period
#buffer=280
tslbuffer=12
#tslbuffer=0
properadx=90
properdmi=42
#properdmi=40
### decreasing trade number but loss as well as
#properdmi=50
tslbufferfinal=10
####do check this is working
tslbufferfinal=10
forbiddenKillSwitch=True
openCandleTradeSwitch=True
breakevenSwitch=False
breakevenLimit=300
breakevenTsl=280
forbidden_time_ranges=[('09:05', '11:00'),("15:20","23:00")]
print(forbidden_time_ranges)
ENTRY_DEVIATION=0
pause_model=False
i=2000

df=pd.read_csv("C://Users/KIIT/Desktop/MasterSetupReborn/df_2025.csv")

df2=pd.read_csv("C://Users/KIIT/Desktop/MasterSetupReborn/df2_2025.csv")
while i<5000000:
    i,day=masterframe(i,day,df,df2)
    print("break"+str(i))
    #i=i+1,
telegram_bot_sendtext("------------------------------------------------------------------------------")