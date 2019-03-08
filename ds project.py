

import pandas as pd
import numpy as np
from datetime import datetime
from datetime import date
from datetime import time
from datetime import timedelta


users=pd.read_csv('takehome_users.csv', encoding='latin-1',index_col='object_id')
users.creation_time=pd.to_datetime(users['creation_time'])
users.last_session_creation_time=pd.to_datetime(users['last_session_creation_time'])
users['time_delta']=users.creation_time-users.last_session_creation_time
users['time_delta']=users['time_delta'].apply(lambda x: x.days)



users.index.names = ['user_id'] 
users_engage=pd.read_csv('takehome_user_engagement.csv')
users_engage['time_stamp']=users_engage['time_stamp']
    .apply(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
#users_engage['time_stamp'] = pd.to_datetime(users_engage['time_stamp'])
users_engage['date'] = users_engage['time_stamp'].apply(lambda x: x.date())
users_engage.set_index('time_stamp',inplace=True) #inplace is set to be True, so df is modified
users_engage.sort_index(inplace=True)
print(type(users_engage.index[0]))

windows=create_windows(users_engage)
userdate_list=create_userdate_list(users_engage)


# Defined functions


#creates all possible 7-days between the first and last day of user activity
def create_windows(df):
    min_date=df.date.min()
    max_date=df.date.max()
    lists=[]
    date_range=(max_date-min_date).days 
    for i in range(0,date_range-5): 
        start_date=min_date+timedelta(days=i) 
        date_list = [start_date+ timedelta(days=x) for x in range(0, 7)] 
        lists.append(date_list)
    ans=np.array(lists) #final list of all date_ranges
    return ans

#identifies which users are considered adopted
def adoption(arr):
    arr=np.unique(arr)
    if len(arr)<3:
        return 0
    for b in windows:
        c=np.isin(arr,b)
        c=[x for x in c if x==True]
        count=len(c)
        if count>=3:   
            return 1
    return 0
grouped=users_engage.groupby('user_id')
adoption_df=pd.DataFrame(grouped.date.apply(adoption))
adoption_df.columns=['Adoption']


#joins user information and adoption identification together
df=users.join(adoption_df, on='user_id', how='left')
df.Adoption.fillna(0, inplace=True)


#model with all variables
x=pd.get_dummies(df.creation_source)
x=x.drop(['GUEST_INVITE'],axis=1)
ols_df=pd.merge(x,df[['opted_in_to_mailing_list','enabled_for_marketing_drip','time_delta',
                      'org_id']],on='user_id', how='left')
ols_df.time_delta.fillna(0, inplace=True)
y=df.Adoption
ols_df = sm.add_constant(ols_df)
model = sm.OLS(y, ols_df).fit()
predictions = model.predict(ols_df)
model.summary()

#model with only creation_time variables
ols_df=pd.get_dummies(df.creation_source)
ols_df=ols_df.drop(['GUEST_INVITE'],axis=1)
y=df.Adoption
ols_df = sm.add_constant(ols_df)
model = sm.OLS(y, ols_df).fit()
predictions = model.predict(ols_df)
model.summary()

#model with only email related variables
y=df.Adoption
ols_df=df[['opted_in_to_mailing_list','enabled_for_marketing_drip']]
ols_df = sm.add_constant(ols_df)
model = sm.OLS(y, ols_df).fit()
predictions = model.predict(ols_df)
model.summary()


#Bar graphs
adopted_graph=pd.DataFrame(df[df['Adoption']==1].creation_source)
adopted_group=adopted_graph.groupby('creation_source')
adopted_group.size().plot(kind='bar',title="Creation Source-Adopted Users")

adopted_graph=pd.DataFrame(df[df['Adoption']==0].creation_source)
adopted_group=adopted_graph.groupby('creation_source')
adopted_group.size().plot(kind='bar',title="Creation Source-Non-adopted Users")



#Mosaics
mosaic(new_df,['Adoption','opted_in_to_mailing_list'])
mosaic(df,['Adoption','enabled_for_marketing_drip'])


#Mosaics
mosaic(new_df,['Adoption','opted_in_to_mailing_list'])
mosaic(df,['Adoption','enabled_for_marketing_drip'])

