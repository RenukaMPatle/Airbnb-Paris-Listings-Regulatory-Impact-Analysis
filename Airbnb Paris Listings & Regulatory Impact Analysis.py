#!/usr/bin/env python
# coding: utf-8

# # Airbnb Paris Listings & Regulatory Impact Analysis

# In[51]:


import numpy as np
import pandas as pd 


# In[52]:


reviews_dict = pd.read_csv("C:/Users/piyus/Downloads/Reviews_data_dictionary.csv")


# In[53]:


listings_dict = pd.read_csv("C:/Users/piyus/Downloads/Listings_data_dictionary.csv")


# In[54]:


reviews_dict


# In[55]:


listings_dict


# In[56]:


reviews = pd.read_csv("C:/Users/piyus/AppData/Local/Temp/Rar$DIa2664.41333/Reviews.csv")


# In[57]:


reviews.head()


# In[58]:


listings_dict = pd.read_csv("C:/Users/piyus/Downloads/Listings_data_dictionary.csv")


# In[59]:


import warnings
warnings.filterwarnings("ignore")


# In[60]:


listings_dict


# # Loading and Checking the Dataset

# In[61]:


listings = pd.read_csv("C:/Users/piyus/AppData/Local/Temp/Rar$DIa12156.1865/Listings.csv",encoding = "ISO-8859-1",low_memory=False)


# In[62]:


listings.head()


# In[63]:


listings.info()


# In[64]:


listings["city"]


# In[65]:


listings["city"].value_counts()


# In[66]:


#Columns and Rows Filtering
paris_listings = listings.query("city=='Paris'")


# In[67]:


paris_listings.info()


# In[68]:


paris_listings = listings.query("city=='Paris'").loc[:,["host_since","neighbourhood","city","accommodates","price"]]


# In[69]:


paris_listings.head()


# In[70]:


paris_listings.info()


# In[71]:


#Checking if there are Missing Values in the Dataset
paris_listings.isna().sum()


# In[72]:


paris_listings.dropna(how = "any",inplace = True)


# In[73]:


paris_listings.info()


# In[74]:


paris_listings.describe()


# In[75]:


paris_listings.describe(include="object")


# In[76]:


paris_listings[paris_listings["accommodates"]==0].count(axis = 0)


# In[77]:


paris_listings[paris_listings["price"]==0].count(axis = 0)


# In[78]:


paris_listings[(paris_listings["price"]==0) & (paris_listings["accommodates"]!=0)]
paris_listings = paris_listings[paris_listings["price"]!=0]
paris_listings.info()


# In[79]:


paris_listings.head()


# In[80]:


#Finding Average Price of AirBnB in Paris As Per Localities
paris_listings_neighbourhood = paris_listings.groupby("neighbourhood").agg({"price":"mean"}).sort_values("price",ascending=False).round(2)
paris_listings_neighbourhood


# In[82]:


paris_Elysee_accommodates = paris_listings.query("neighbourhood=='Elysee'").groupby("accommodates").agg({"price":"mean"}).sort_values("price",ascending=False).round(2)


# In[83]:


paris_Elysee_accommodates


# In[ ]:


# The AirBnB with 14 people accommodates is the expensive, even more expensive the 16 accommodates
# the same trend is spotted for 11 and 12 accommodates. Every other accommodation looks reasonable.
### Possible reasons for this trend
1. Owners of properties with 16 people might face occupancy issues due to less number of large groups.
2. The ones with 14 people might be a sweet spot for a group having two families travelling.
3. There is possibility that more than 16 and 12 occupancy properties are away from hotspots in Elysee.
4. There might be potential outliers in 11 and 14 occupancy properties which are skewing the trend.


# In[84]:


paris_listings["host_since"].nunique()


# # Finding Popularity of AirBnB Over Time

# In[90]:


df=paris_listings
df.host_since = pd.to_datetime(df.host_since)
paris_listings_over_time = paris_listings.set_index("host_since").resample("Y").agg({"neighbourhood":"count","price":"mean"})


# In[91]:


paris_listings_over_time


# In[92]:


import matplotlib.pyplot as plt
import seaborn as sns


# In[93]:


paris_listings_neighbourhood


# In[94]:


plt.figure(figsize = (12,8))
sns.barplot(data = paris_listings_neighbourhood,
           x = "price",
           y = paris_listings_neighbourhood.index,
           color = "#E5989B")
plt.title("Neighbourhoods in Paris (Premium Localities at the Top!)")
plt.xlabel("How Expensive? (Euros)")
plt.ylabel("Prominent Places with AirBnBs")
plt.show()


# In[ ]:


# Inside of Paris, the price of AirBnBs is directly impacted by the popularity of the tourist place or 
# the view of Eiffel tower. We need to further see if the prices are increasing when the regulations are imposed.


# In[95]:


paris_Elysee_accommodates


# In[96]:


plt.figure(figsize = (12,8))
sns.barplot(data = paris_Elysee_accommodates,
           x = "price",
           y = paris_Elysee_accommodates.index,
           color = "green",
           orient = "h",
           order = paris_Elysee_accommodates.index)
plt.title("Average Price of AirBnB in Elysee -- vs -- Number of People that can stay")
plt.xlabel("Average Price (Euros)")
plt.ylabel("Number of People that can stay")
plt.show()


# In[ ]:


# The AirBnBs with 14 people accomodation is the costliest, even costlier than 16 accomodates. 
# the same trend is spotted for 11 and 12 accomodates. Every other accomodation looks reasonable.


# In[97]:


paris_listings_over_time


# In[98]:


plt.figure(figsize = (12,8))
sns.lineplot(data = paris_listings_over_time["neighbourhood"],color = "pink")
plt.xlabel("Years")
plt.ylabel("Number of AirBnBs and Localities")
plt.title("Popularity of AirBnBs over time")
plt.grid(True)
plt.show()


# In[99]:


plt.figure(figsize = (12,8))
sns.lineplot(data = paris_listings_over_time["price"],color = "green")
plt.xlabel("Years")
plt.ylabel("Average Price")
plt.title("Average Price of AirBnBs over time")
plt.grid(True)
plt.show()


# In[ ]:


#Finding Effects of Regulations on AirBnB Business


# In[100]:


fig , ax = plt.subplots()

ax.plot(paris_listings_over_time.index,paris_listings_over_time["neighbourhood"], label = "New Hosts", c = "pink")

ax.set_ylabel("New Hosts")

ax2 = ax.twinx()

ax2.plot(paris_listings_over_time.index,paris_listings_over_time["price"], label = "Average Price")

ax2.set_ylim(0)

ax2.set_ylabel("Average Price")

ax.set_title("Regulations Lead to Fewer New Hosts and Higher Prices")

plt.show()


# # Final Insights

# In[ ]:


1.The Number of AirBnBs kept on increasing since the launch and prices kept on increasing too, due to initial traction and early adopters.
2.After the startup is known to everyone and becomes a common utility, AirBnBs start increasing in numbers and prices also kept on decreasing.
3.After regulation was announced around 2015 there was under confidence in the business, number of AirBnBs started decreasing and prices started increasing.
4.Once the regulation is the new normal, during the year 2019 the number of AirBnBs have increased in number and prices kept decreasing due to more supply of them.


# # Recommendation for AirBnB

# In[ ]:


1.Regulations in long term rentals can impact the business adversely, there might be customer and hosts churn due to uncertainty.Such regulations might add to AirBnBs losses which might be difficult to recover later.
2.If the customer experience is going to get impacted due to this, it would lead to incorrect brand perception.
3.It is recommended to watch out for any such regulations at other places and be prepared for it.
4.AirBnB can replicate such regulations at other places.
5.They can keep strict rules to onboard and release the hosts.
6.They can limit the number of AirBnBs in a locality to ensure the public has enough rental options and the government doesn't step in.


# In[ ]:





# In[ ]:





# In[ ]:




