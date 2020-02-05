
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import datetime
from datetime import timedelta
import datetime as dt
from numpy import mean
import math
from no_PII_Storage_folder import *
import matplotlib.pyplot as plt


# In[2]:


user_data_org = pd.read_json('NewData/clickstream/sample_mitx_6002x_7_1t2017_log_data_500000.json',  lines = True)

user_data = user_data_org
user_data['username'] = hash_column(user_data_org['username'])
# user_data.loc[0:3,]  #### get bunch of each row data

print(user_data['username'])
# type(user_data['username'])
# username = user_data['username']


# print("Username Only\n",)
#print(username)
# username.value_counts(sort=True, ascending=True)


# In[3]:


#Searches for mobile users and adds them to new data frame with ONLY mobile users

### Divide 'Mobile User' and 'Non Mobile User' // 'mobile_data'   ,  'Non_mobile_data'

keyword = "Mobi"

total_mobile = 0
total_non_mobile = 0

mobile_data = pd.DataFrame()
Non_mobile_data = pd.DataFrame()

for count in range(len(user_data)):
    if keyword in user_data['agent'][count]:
        mobile_data[total_mobile] = user_data.loc[count]
        total_mobile += 1
    else:
        Non_mobile_data[total_non_mobile] = user_data.loc[count]
        total_non_mobile += 1
        
print("\nThere are " + str(total_mobile) + " user-agents that contain:  " + keyword )  
print("\nThere are " + str(total_non_mobile) + " user-agents that not contain:  " + keyword)  

mobile_data = mobile_data.T
Non_mobile_data = Non_mobile_data.T

#print(Non_mobile_data)



# Mobi ref : https://delib.zendesk.com/hc/en-us/articles/203431259-Browser-device-identification-how-to-find-out-which-browser-and-device-have-been-used-to-submit-a-response


# In[4]:


Mobile_name_time_data = mobile_data[['username', 'time']]
Non_Mobile_name_time_data = Non_mobile_data[['username', 'time']]

#### We have to erase if there is '' and 'NaN' in the information 

Extract_Mobile_Dataframe = pd.DataFrame()
Extract_Non_Mobile_Dataframe = pd.DataFrame()


Total_Extract_Mobile = 0
Count_For_Mobile = 0

Total_Extract_Non_Mobile =0
Count_For_Non_Mobile = 0





for Count_For_Mobile in range(total_mobile):
    if( (Mobile_name_time_data['username'][Count_For_Mobile] != '' and Mobile_name_time_data['username'][Count_For_Mobile] != 'NA')):
        if((Mobile_name_time_data['time'][Count_For_Mobile] !='' and Mobile_name_time_data['time'][Count_For_Mobile] !='NA')):
            Extract_Mobile_Dataframe[Total_Extract_Mobile] = Mobile_name_time_data.loc[Count_For_Mobile]
            Total_Extract_Mobile = Total_Extract_Mobile + 1 
            
print(Extract_Mobile_Dataframe) 

for Count_For_Non_Mobile in range(total_non_mobile):
    if( (Non_Mobile_name_time_data['username'][Count_For_Non_Mobile] != '' and Non_Mobile_name_time_data['username'][Count_For_Non_Mobile] != 'NA')):
        if((Non_Mobile_name_time_data['time'][Count_For_Non_Mobile] !='' and Non_Mobile_name_time_data['time'][Count_For_Non_Mobile] !='NA')):
            Extract_Non_Mobile_Dataframe[Total_Extract_Non_Mobile] = Non_Mobile_name_time_data.loc[Count_For_Non_Mobile]
            Total_Extract_Non_Mobile = Total_Extract_Non_Mobile + 1 
#     if(Count_For_Non_Mobile==9912):
#         break

print("Extract_Non_Mobile_Dataframe\n")
print(Extract_Non_Mobile_Dataframe)

Extract_Mobile_Dataframe = Extract_Mobile_Dataframe.T
Extract_Non_Mobile_Dataframe = Extract_Non_Mobile_Dataframe.T

print("Transpose_Extract_Mobile_Dataframe\n")
print(Extract_Mobile_Dataframe)

print("Transpose_Extract_Non_Mobile_Dataframe\n")
print(Extract_Non_Mobile_Dataframe)

# Extract_Mobile_Dataframe.value_counts(sort=True, ascending=True)
# Extract_Non_Mobile_Dataframe.value_counts(sort=True, ascending=True)


# In[5]:


##### Here part is for groupby ####

Extract_Mobile_Dataframe = Extract_Mobile_Dataframe.sort_values(['time'], ascending=True)  ## Sorting time before group by
Grouped_Mobile_Dataframe = Extract_Mobile_Dataframe.groupby('username')

for key, group in Grouped_Mobile_Dataframe:
    print(" key: ", key)
    print(" count: ", len(group))
    print(group.head())
    print("\n")

List_Mobile_Keys = list(Grouped_Mobile_Dataframe.groups.keys())
print("List_Mobile_Keys\n")
print(List_Mobile_Keys)
print(len(List_Mobile_Keys))  ### There are ... unique keys in here == There are 12 unique users for Mobile Users

print("Print Here\n")

Mobile_Group0 = Grouped_Mobile_Dataframe.get_group(List_Mobile_Keys[0])

print("Mobile_Group0\n")
print(Mobile_Group0)
print("Can I print out the len of the Group0?\n")
print(len(Mobile_Group0))   ### We can get the number of click


print("Type of it!\n")
print(type(Mobile_Group0))  #### <class 'pandas.core.frame.DataFrame'>

print(Mobile_Group0['time'].iloc[0])
print(Mobile_Group0['time'].iloc[1])


##### Just want to see how may   --> We can just ignore it

Grouped_Mobile_Dataframe_count = Grouped_Mobile_Dataframe.count()
print(Grouped_Mobile_Dataframe_count)    ##### It will show how many times does each user click it. Left: usernaem  Right: how many times do they click for it
type(Grouped_Mobile_Dataframe_count)  ### It was Dataframe 

print(Grouped_Mobile_Dataframe_count.iloc[0][0])   #### We can get only the click number of first user : 
print(Grouped_Mobile_Dataframe_count.iloc[1][0])   #### We can get only the click number of second user : 

print("Only the click time\n")
click_time_Mobile = Grouped_Mobile_Dataframe_count.iloc[:,0]
print(click_time_Mobile[0]) # We can get only the click number of first user : 
print(type(click_time_Mobile))  # <class 'pandas.core.series.Series'>
print(type(click_time_Mobile[0]))  # <class 'numpy.int64'>
#### Actually there are ... unique users for Mobile users.


############################################################### Okay Let's get it!!!##########################

#### I did it depend on "List_Mobile_Keys" sequence. This sequence is the order of group name(=user)
datetimeFormat = '%Y-%m-%d %H:%M:%S.%f %Z'

Full_time_diff_Mobile_List = []
time_diff_Mobile_List = []
Plot_time_diff_Mobile_List = []   #### Use this list when we are plot a histogram

for i in range(len(List_Mobile_Keys)):  ### Loop for how many groups (= how many unique users)
    time_diff_Mobile_List = []
    Mobile_Group = Grouped_Mobile_Dataframe.get_group(List_Mobile_Keys[i])  ## i th Group
    for j in range(len(Mobile_Group)-1):  ### Loop for how many click times for each i th Group  // It is the time difference so we need to do -1
        time_diff_Mobile = datetime.datetime.strptime(Mobile_Group['time'].iloc[j+1], datetimeFormat)-datetime.datetime.strptime(Mobile_Group['time'].iloc[j],datetimeFormat)
        #time_diff_Mobile_List.append(time_diff_Mobile)
        time_diff_Mobile_List.append(time_diff_Mobile.total_seconds())
        Plot_time_diff_Mobile_List.append(time_diff_Mobile.total_seconds())
        
    print("This is for Group : ", i)
    print(time_diff_Mobile_List)
    print("The length of the click_diff time for this Group is :")
    print(len(time_diff_Mobile_List))
#    Full_time_diff_Mobile_List.append(time_diff_Mobile_List)
    Full_time_diff_Mobile_List.append(round(np.mean(time_diff_Mobile_List),2))

print("This is for the full time difference for Mobile User\n")
print(Full_time_diff_Mobile_List)

print("The number of Group is \n")
print(len(Full_time_diff_Mobile_List))  #

print("The average of Full_time_diff_Mobile_List\n")
print(np.mean(Full_time_diff_Mobile_List))

print("This is the list for plot\n")
print(Plot_time_diff_Mobile_List)

print("The length of the list for plot is : ")
print(len(Plot_time_diff_Mobile_List))    ####  

print("What is the max time_diff in Mobile User?\n")
print(max(Plot_time_diff_Mobile_List))   #### 
print(min(Plot_time_diff_Mobile_List))      #### 
print(np.mean(Plot_time_diff_Mobile_List))   ####  

#print(type(Full_time_diff_Mobile_List[0][0]))    #  <class 'float'>





# In[6]:


##### Here is for the Non_Mobile_User  ######


Extract_Non_Mobile_Dataframe = Extract_Non_Mobile_Dataframe.sort_values(['time'], ascending=True)    
Grouped_Non_Mobile_Dataframe = Extract_Non_Mobile_Dataframe.groupby('username')

for key_n, group_n in Grouped_Non_Mobile_Dataframe:
    print(" key: ", key_n)
    print(" count: ", len(group_n))
    print(group_n.head())
    print("\n")

######## Copy from the Mobile Things ######

List_Non_Mobile_Keys = list(Grouped_Non_Mobile_Dataframe.groups.keys())
print("List__Non_Mobile_Keys\n")
print(List_Non_Mobile_Keys)
print(len(List_Non_Mobile_Keys))  ### There are ...unique keys in here == There are ... unique users for Non Mobile Users

print("Print Here\n")

Mobile_Non_Group0 = Grouped_Non_Mobile_Dataframe.get_group(List_Non_Mobile_Keys[0])

print("Mobile_Non_Group0\n")
print(Mobile_Non_Group0)
print("Can I print out the len of the Group0?\n")
print(len(Mobile_Non_Group0))   ### We can get the number of click


print("Type of it!\n")
print(type(Mobile_Non_Group0))  #### <class 'pandas.core.frame.DataFrame'>



##### Just want to see how may   --> We can just ignore it

Grouped_Non_Mobile_Dataframe_count = Grouped_Non_Mobile_Dataframe.count()
print(Grouped_Non_Mobile_Dataframe_count)    ##### It will show how many times does each user click it. Left: usernaem  Right: how many times do they click for it
type(Grouped_Non_Mobile_Dataframe_count)  ### It was Dataframe 


print("Only the click time\n")
click_time_Non_Mobile = Grouped_Non_Mobile_Dataframe_count.iloc[:,0]
print(click_time_Non_Mobile[0]) # We can get only the click number of first user 
print(type(click_time_Non_Mobile))  # <class 'pandas.core.series.Series'>
print(type(click_time_Non_Mobile[0]))  # <class 'numpy.int64'>
#### Actually there are ... unique users for Non Mobile users.


############################################################### Okay Let's get it!!!##########################

#### I did it depend on "List_Non_Mobile_Keys" sequence. This sequence is the order of group name(=user)
datetimeFormat = '%Y-%m-%d %H:%M:%S.%f %Z'

Full_time_diff_Non_Mobile_List = []
time_diff_Non_Mobile_List = []
Plot_time_diff_Non_Mobile_List = []   #### Use this list when we are plot a histogram
count_Nan = 0

for i in range(len(List_Non_Mobile_Keys)):  ### Loop for how many groups (= how many unique users)
    time_diff_Non_Mobile_List = []
    Non_Mobile_Group = Grouped_Non_Mobile_Dataframe.get_group(List_Non_Mobile_Keys[i])  ## i th Group
    
    if(len(Non_Mobile_Group)!=1):
        for j in range(len(Non_Mobile_Group)-1):  ### Loop for how many click times for each i th Group  // It is the time difference so we need to do -1
            time_diff_Non_Mobile = datetime.datetime.strptime(Non_Mobile_Group['time'].iloc[j+1], datetimeFormat)-datetime.datetime.strptime(Non_Mobile_Group['time'].iloc[j],datetimeFormat)
            #time_diff_Mobile_List.append(time_diff_Mobile)
            time_diff_Non_Mobile_List.append(time_diff_Non_Mobile.total_seconds())
            Plot_time_diff_Non_Mobile_List.append(time_diff_Non_Mobile.total_seconds())
            
        print("This is for Group : ", i)
        print(time_diff_Non_Mobile_List)
        print("The length of the click_diff time for this Group is :")
        print(len(time_diff_Non_Mobile_List))

        Full_time_diff_Non_Mobile_List.append(round(np.mean(time_diff_Non_Mobile_List),2))

print("This is for the full time difference for Non Mobile User\n")
print(Full_time_diff_Non_Mobile_List)

print("The number of Group is \n")
print(len(Full_time_diff_Non_Mobile_List))  

print("Count Nan!\n")
print(count_Nan)

print("The average of Full_time_Non_diff_Mobile_List\n")
print(np.mean(Full_time_diff_Non_Mobile_List))

print("This is the list for plot\n")
print(Plot_time_diff_Non_Mobile_List)

print("The length of the list for plot is : ")
print(len(Plot_time_diff_Non_Mobile_List))  #### 

print(max(Plot_time_diff_Non_Mobile_List))   ####   
print(min(Plot_time_diff_Non_Mobile_List))   #### 
print(np.mean(Plot_time_diff_Non_Mobile_List))   #### 


# In[7]:


### Plot for Mobile Users ###

def round_up(n, decimals=0):
    
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier


print("This is the list for plot\n")
print(Plot_time_diff_Mobile_List)

print("The length of the list for plot is : ")
print(len(Plot_time_diff_Mobile_List))

print("What is the max time_diff in Mobile User?\n")
print(max(Plot_time_diff_Mobile_List))   ####   
print(min(Plot_time_diff_Mobile_List))   #### 
print(np.mean(Plot_time_diff_Mobile_List))   #### 

print(" The length of the digit of the max \n")

digit_count = 0
max_num = max(Plot_time_diff_Mobile_List)
while max_num >=10:
    digit_count = digit_count +1
    max_num = max_num/10

print(" To test the round_up\n")
range_variable = round_up(max(Plot_time_diff_Mobile_List), -(digit_count))
print(range_variable)
min_range_variable = min(range_variable, 10000.0)    #### 86400 sec is 24 hours
print("min_range_varbiable: ", min_range_variable)
range_values = (0,min_range_variable)
print("range_values\n")
print(range_values)

bins = 20

## Plotting a histogram

plt.hist(Plot_time_diff_Mobile_List, bins, range=range_values, color = 'green', histtype = 'bar', rwidth = 0.8)

# x-axis label
plt.xlabel('Time_Interval_sec')
# frequency label
plt.ylabel('No. of click')
# plot title
plt.title('Mobile Users')

# function to show the plot
plt.show()

### The threshold is 2000 sec #### --> We have to get rid of data which is more than 2000 sec
print(" The type of Plot_time_diff_Mobile_List\n")
print(type(Plot_time_diff_Mobile_List))   ### List

print(max(Plot_time_diff_Mobile_List))

### Make a New array ###
Th_Plot_time_diff_Mobile_List = []

for i,e in enumerate(Plot_time_diff_Mobile_List):
    if(e<=2000):  #### I'll just make the time_diff more than 2000 sec -> 0 sec
#         print(type(e))
#         print(e)
        Th_Plot_time_diff_Mobile_List.append(e)
        
print(len(Th_Plot_time_diff_Mobile_List))  ###   clicks (threshold was applied)
print(np.mean(Th_Plot_time_diff_Mobile_List))  ####  is the average time_diff for Mobile Users
        


# In[18]:


Mobile_interval_plot = min_range_variable / bins
bins2 = np.arange(0,min_range_variable,Mobile_interval_plot)    #### The range is up to 10000, but there are 20 bins, so 10000/20 = 500
hist2, bin2_edges = np.histogram(Plot_time_diff_Mobile_List, bins2)
print(hist2)
type(hist2) ### array
###If, interval is 2000,
Mobile_sample_included = 0
for i in range(int(2000/Mobile_interval_plot)):
    Mobile_sample_included = Mobile_sample_included + hist2[i]

print(Mobile_sample_included)
Mobile_total_click = 0

for j in range(len(hist2)):
    Mobile_total_click = Mobile_total_click + hist2[j]
    
Mobile_sample_included_Percent = Mobile_sample_included / Mobile_total_click

print(Mobile_sample_included_Percent)


# In[19]:


### Plot for Non-Mobile users ###

def round_up(n, decimals=0):
    
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier


# print("This is the list for plot\n")
# print(Plot_time_diff_Non_Mobile_List)

print("The length of the list for plot is : ")
print(len(Plot_time_diff_Non_Mobile_List))

print("What is the max time_diff in Mobile User?\n")
print(max(Plot_time_diff_Non_Mobile_List))   ####   
print(min(Plot_time_diff_Non_Mobile_List))   #### 
print(np.mean(Plot_time_diff_Non_Mobile_List))   #### 

print(" The length of the digit of the max \n")

Non_digit_count = 0
Non_max_num = max(Plot_time_diff_Non_Mobile_List)
while Non_max_num >=10:
    Non_digit_count = Non_digit_count +1
    Non_max_num = Non_max_num/10

print(" To test the round_up\n")
Non_range_variable = round_up(max(Plot_time_diff_Non_Mobile_List), -(Non_digit_count))
print(Non_range_variable)
Non_min_range_variable = min(Non_range_variable, 10000.0)
print("min_range_variable: ", Non_min_range_variable)
Non_range_values = (0,Non_min_range_variable)
print("range_values\n")
print(Non_range_values)

bins = 20

## Plotting a histogram

plt.hist(Plot_time_diff_Non_Mobile_List, bins, range=Non_range_values, color = 'green', histtype = 'bar', rwidth = 0.8)

# x-axis label
plt.xlabel('Time_Interval_sec')
# frequency label
plt.ylabel('No. of click')
# plot title
plt.title('Non-Mobile Users')

# function to show the plot
plt.show()

### The threshold is 2000 sec #### --> We have to get rid of data which is more than 2000 sec

### Make a New array ###
Th_Plot_time_diff_Non_Mobile_List = []

for i,e in enumerate(Plot_time_diff_Non_Mobile_List):
    if(e<=2000):  #### I'll just make the time_diff more than 2000 sec -> 0 sec
#         print(type(e))
#         print(e)
        Th_Plot_time_diff_Non_Mobile_List.append(e)
        
print(len(Th_Plot_time_diff_Non_Mobile_List))  ###  clicks (threshold was applied)
print(np.mean(Th_Plot_time_diff_Non_Mobile_List))  ####  is the average time_diff for Mobile Users



########### Overall Results ############
# 1. Without threshold(=2000 sec) 
#    1) Mobile Users : Average time_diff -> ...sec
#    2) Non-Mobile Users : Average time_diff ->  ...sec  

# 2. With threshold(=2000 sec)
#    1) Mobile users : Average time_diff -> ...sec
#    2) Non-Mobile Users : Average time_diff -> ...sec   


# In[20]:


bins3 = np.arange(0,min_range_variable,500)
hist3, bin3_edges = np.histogram(Plot_time_diff_Non_Mobile_List, bins3)
print(hist3)


Non_Mobile_interval_plot = Non_min_range_variable / bins
bins3 = np.arange(0,Non_min_range_variable,Non_Mobile_interval_plot)    #### The range is up to 10000, but there are 20 bins, so 10000/20 = 500
hist3, bin3_edges = np.histogram(Plot_time_diff_Non_Mobile_List, bins3)
print(hist3)
type(hist3) ### array
###If, interval is 2000,
Non_Mobile_sample_included = 0
for i in range(int(2000/Non_Mobile_interval_plot)):
    Non_Mobile_sample_included = Non_Mobile_sample_included + hist3[i]

print(Non_Mobile_sample_included)
Non_Mobile_total_click = 0

for j in range(len(hist3)):
    Non_Mobile_total_click = Non_Mobile_total_click + hist3[j]
    
Non_Mobile_sample_included_Percent = Non_Mobile_sample_included / Non_Mobile_total_click

print(Non_Mobile_sample_included_Percent)

