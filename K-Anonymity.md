# Data Protocol Privacy Engineering Certification

## K-Anonymity Living Lab

![Data Protocol Privacy Engineering Certification](./images/nishant_pe.png)

This workbook is part of the [Data Protocol Privacy Engineering Certification](https://dataprotocol.com/). Working with data and anonymizing data is a growing essential skill that has to be learned as well as applied. To fully understand and benefit from this workbook, take the [course](https://dataprotocol.com/), read the [book](https://www.manning.com/books/privacy-engineering), and get certified!

This is a Juypter Labs workbook, If you are completely new to Jupyter workbooks and want to understand how to use, please watch [this short video](https://youtu.be/A5YyoCKxEOU?t=106) to learn the basics.

## Introduction to K-Anonymity

This introduction looks at k-anonymity, a privacy model commonly applied to protect the data subjects’ privacy in data sharing scenarios, and the guarantees that k-anonymity can provide when used to anonymise data. 

Sharing data is a very important decision to take. It is impossible to get data back once shared and liabilities can be tremendously high, especially if the data being shared can be used to identify individuals and lead to a loss of privacy. You may have tried really hard to anonymize the data being released but legal organizations want to trust more than your word. K-anonymity serves that need by providing one mechanism to quantify the risk contained in any released dataset, it moves the conversation from subjective opinion to factual basis.

## Introduction to the Living Lab - Elite Cars

We are going to use the fictional case study of Elite Cars.  Read the full description on github [here](https://github.com/Data-Protocol/privacy-playground/blob/main/README.md), here is the start

"Elite cars is a new start up that launched in New York just over a month ago. It offers an elite car ride service for the rich and famous and guarantees anonymity and total discretion.  It has captured the imagination of those it was trying to attract and in the first month it has over 4000 very well known people signed up as customers that have already taken over 90,000 trips..."



## The Challenge

New York City has asked Elite Cars to provide their passenger trip records, so they can run their own analysis.  Anonymity is of paramount importance to your customers and to the core promise and identity of the company.  

A dataset has been created that has stripped out unecessary trip data such as tips and links to driver details and passenger details. But the request has asked for the home address, gender and age of the passengers using the service, where they are going from and to, and at what times.  

The challenge in this living lab is to use K-Anonymity to interrogate this dataset and understand the level of risks and concerns that may exist. We are going to do this whole process manually so we can feel what is involved and what needs consideration. In the real world, there are machine learning algorithms that will help you achieve your wanted K-Anonymity values.

But remember, datasets are like dogs - all the same but each one is different and potentially delivers a different bite in different situations.

Let's begin...

## Preparing the Lab

We are going to use python for this exercise since python has many libraries for supporting large datasets such as pandas and numpy, all packaged by [scipy.org](https://scipy.org).  We are not going to do anything advanced so we hope you can follow along and focus on the k-anonymization aspects even if you are not a regular python coder.  

It is necessary to execute each line of the code starting from the top of the workbook.  You can re-execute individual cells after changing the contained code if wanted.

We will first import the main library we will be using - pandas.  This makes working with large datasets very easy. We then load in the master trip dataset that our engineers have generated for us.


```python
import pandas as pd

# Set max line width length for output
# pd.set_option('display.width', 144)

master_df = pd.read_csv("passenger-trips.csv", dtype=str)
master_df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 97950 entries, 0 to 97949
    Data columns (total 9 columns):
     #   Column        Non-Null Count  Dtype 
    ---  ------        --------------  ----- 
     0   Pickup        97950 non-null  object
     1   Dropoff       97950 non-null  object
     2   Pickup_long   97950 non-null  object
     3   Pickup_lat    97950 non-null  object
     4   Dropoff_long  97950 non-null  object
     5   Dropoff_lat   97950 non-null  object
     6   Sex           97950 non-null  object
     7   Zip           97950 non-null  object
     8   DOB           97950 non-null  object
    dtypes: object(9)
    memory usage: 6.7+ MB


You can see there are 8 fields. We have loaded them all in as strings for simplicity.  There are no empty fields and all fields have been padded with "*" characters where necessary, to give them uniform length.


```python
print("Master Dataset size = ", len(master_df), '\n')
```

    Master Dataset size =  97950 
    


As stated by Elite Cars you can see there are 97,950 rows of data, which is all of the trip data in the company.  


```python
display(master_df.head(3))
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Pickup</th>
      <th>Dropoff</th>
      <th>Pickup_long</th>
      <th>Pickup_lat</th>
      <th>Dropoff_long</th>
      <th>Dropoff_lat</th>
      <th>Sex</th>
      <th>Zip</th>
      <th>DOB</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2015-01-15 19:05:39</td>
      <td>2015-01-15 19:23:42</td>
      <td>-73.993896484375***</td>
      <td>40.750110626220703</td>
      <td>-73.974784851074219</td>
      <td>40.750617980957031</td>
      <td>M</td>
      <td>10889</td>
      <td>1968-07-20</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2015-01-10 20:33:38</td>
      <td>2015-01-10 20:53:28</td>
      <td>-74.00164794921875*</td>
      <td>40.7242431640625**</td>
      <td>-73.994415283203125</td>
      <td>40.759109497070313</td>
      <td>F</td>
      <td>10384</td>
      <td>1980-07-08</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2015-01-10 20:33:38</td>
      <td>2015-01-10 20:43:41</td>
      <td>-73.963340759277344</td>
      <td>40.802787780761719</td>
      <td>-73.951820373535156</td>
      <td>40.824413299560547</td>
      <td>M</td>
      <td>10422</td>
      <td>1996-06-21</td>
    </tr>
  </tbody>
</table>
</div>


We have printed the top 3 rows of the data. You can see the data is incredibly detailed both from a time and location point of view.  This is a data set that looks anonymous at first glance since there is no clear Personally Identifying Information (PII) visible.  But it is exactly the opposite.  Let's use K-anonymity to quantify that statement.

## Analyse dataset for k-anonymity

To help, we will create helper functions as we introduce new techniques to study our dataset. The first analyses the dataset and prints out key k-anonymity findings.




```python
def analyse_table_k_anon(df):

    print("\n-----------------------\n")
    print("Dataset K-Anon Analysis\n")
    print("-----------------------\n")

    print("Dataset size = ", len(df))
    print("\n-----------------------\n")

    print("K-Anonymity Min to Max Values\n")
    groupings = df.value_counts(ascending=True).reset_index(name='freq')
    
    display(groupings)

    print("\n-----------------------\n")
    print(
        "\nOverall K-Anonymity Classification for dataset = ", groupings['freq'][0], "\n"
    )
    print("\n-----------------------\n")

analyse_table_k_anon(master_df)

```

    
    -----------------------
    
    Dataset K-Anon Analysis
    
    -----------------------
    
    Dataset size =  97950
    
    -----------------------
    
    K-Anonymity Min to Max Values
    



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Pickup</th>
      <th>Dropoff</th>
      <th>Pickup_long</th>
      <th>Pickup_lat</th>
      <th>Dropoff_long</th>
      <th>Dropoff_lat</th>
      <th>Sex</th>
      <th>Zip</th>
      <th>DOB</th>
      <th>freq</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2015-01-01 00:09:45</td>
      <td>2015-01-01 00:13:50</td>
      <td>-73.996726989746094</td>
      <td>40.744548797607422</td>
      <td>-74.002204895019531</td>
      <td>40.750385284423828</td>
      <td>F</td>
      <td>10565</td>
      <td>1965-03-30</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2015-01-21 14:45:34</td>
      <td>2015-01-21 15:02:48</td>
      <td>-73.9559326171875**</td>
      <td>40.763961791992188</td>
      <td>-73.988739013671875</td>
      <td>40.736881256103516</td>
      <td>F</td>
      <td>10535</td>
      <td>1979-02-02</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2015-01-21 14:45:34</td>
      <td>2015-01-21 14:59:41</td>
      <td>-73.956916809082031</td>
      <td>40.784225463867188</td>
      <td>-73.9859619140625**</td>
      <td>40.772186279296875</td>
      <td>M</td>
      <td>10220</td>
      <td>1957-01-09</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2015-01-21 14:45:34</td>
      <td>2015-01-21 14:57:34</td>
      <td>-73.972564697265625</td>
      <td>40.74951171875****</td>
      <td>-73.98388671875****</td>
      <td>40.725704193115234</td>
      <td>F</td>
      <td>10766</td>
      <td>1994-02-17</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2015-01-21 14:45:33</td>
      <td>2015-01-21 14:52:10</td>
      <td>-73.974113464355469</td>
      <td>40.783061981201172</td>
      <td>-73.968673706054688</td>
      <td>40.7696533203125**</td>
      <td>F</td>
      <td>10494</td>
      <td>1975-04-16</td>
      <td>1</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>97945</th>
      <td>2015-01-12 05:10:41</td>
      <td>2015-01-12 05:11:44</td>
      <td>-73.998161315917969</td>
      <td>40.745731353759766</td>
      <td>-73.994834899902344</td>
      <td>40.750255584716797</td>
      <td>F</td>
      <td>10713</td>
      <td>1991-11-13</td>
      <td>1</td>
    </tr>
    <tr>
      <th>97946</th>
      <td>2015-01-12 05:10:39</td>
      <td>2015-01-12 05:30:00</td>
      <td>-73.78936767578125*</td>
      <td>40.647361755371094</td>
      <td>-73.743789672851563</td>
      <td>40.595340728759766</td>
      <td>F</td>
      <td>10703</td>
      <td>1975-05-27</td>
      <td>1</td>
    </tr>
    <tr>
      <th>97947</th>
      <td>2015-01-12 05:10:38</td>
      <td>2015-01-12 05:13:24</td>
      <td>-73.950439453125***</td>
      <td>40.771511077880859</td>
      <td>-73.959632873535156</td>
      <td>40.773906707763672</td>
      <td>M</td>
      <td>10905</td>
      <td>1986-07-17</td>
      <td>1</td>
    </tr>
    <tr>
      <th>97948</th>
      <td>2015-01-12 06:29:11</td>
      <td>2015-01-12 06:35:44</td>
      <td>-74.000511169433594</td>
      <td>40.737335205078125</td>
      <td>-74.013481140136719</td>
      <td>40.715747833251953</td>
      <td>M</td>
      <td>10100</td>
      <td>1978-08-21</td>
      <td>1</td>
    </tr>
    <tr>
      <th>97949</th>
      <td>2015-01-31 23:57:12</td>
      <td>2015-02-01 00:30:09</td>
      <td>-73.983390808105469</td>
      <td>40.756019592285156</td>
      <td>-73.984382629394531</td>
      <td>40.664901733398438</td>
      <td>M</td>
      <td>10360</td>
      <td>1995-05-10</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>97950 rows × 10 columns</p>
</div>


    
    -----------------------
    
    
    Overall K-Anonymity Classification for dataset =  1 
    
    
    -----------------------
    


## Specificity

The first thing we are going to do is examine each data field type for specificity versus "needed" specificity. Anonymizing datasets is a balance between the analysis wanting to be performed versus the level of detail held within the dataset.  In this case, we do not specifically know the precise details of the reasons why the data is being requested, which can be common in the real world as well.  It is not unusual for a negotiation to take place between wanted interest of the receiver versus risk analysis from the provider.  This is why mathematical analysis of the data to score anonymity in a quantified way is such a powerful concept. There is no judgement, just decisions about risk versus need.  

In this live lab, we shall look at each different field, present possible alternatives, and in our case here, make some arbitary decisions on which we initially choose, so we can then run further mechanisms to hit the k-anonymity numbers wanted.

When looking at datasets, it is important to understand perspective and context can radically change the dangers of any dataset.  The data we are using is all located in the NY area, with very precise date, time and location information. Mapping the location data and correlating the timing with known events in the city could, for example, give a much smaller population of interest. For example, if a film festival is taking place, it can be seen who is traveling to the film festival. We have their home zip codes, sex and date of birth. We can quickly identify which journeys are those taken by famous film stars, where and when they were going to different places not correlated to the film festival, and how often.  Anonymous data has quickly changed into highly focused source of knowledge. Using a similar technique, rather than starting with the dataset let us start with the known home address of a famous film actor, and see if that location is either at the start and/or end of any journeys. You can see by using other public information, the data that we currently have in this dataset can be used to identify people very quickly.  The exact inverse of what is needed by Elite Cars.

### Pickup and Dropoff Location Data

Let us start by looking at the specificity of the location data.  



```python
location_columns  = master_df.head()[['Pickup_long', 'Pickup_lat', 'Dropoff_long', 'Dropoff_lat']]
display(location_columns)
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Pickup_long</th>
      <th>Pickup_lat</th>
      <th>Dropoff_long</th>
      <th>Dropoff_lat</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-73.993896484375***</td>
      <td>40.750110626220703</td>
      <td>-73.974784851074219</td>
      <td>40.750617980957031</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-74.00164794921875*</td>
      <td>40.7242431640625**</td>
      <td>-73.994415283203125</td>
      <td>40.759109497070313</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-73.963340759277344</td>
      <td>40.802787780761719</td>
      <td>-73.951820373535156</td>
      <td>40.824413299560547</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-74.009086608886719</td>
      <td>40.713817596435547</td>
      <td>-74.004325866699219</td>
      <td>40.719985961914063</td>
    </tr>
    <tr>
      <th>4</th>
      <td>-73.971176147460938</td>
      <td>40.762428283691406</td>
      <td>-74.004180908203125</td>
      <td>40.742652893066406</td>
    </tr>
  </tbody>
</table>
</div>


The gps coordinates have 15 decimal places.  Using acuracy information on [gis.stackexhange.com](https://gis.stackexchange.com/questions/8650/measuring-accuracy-of-latitude-and-longitude/) we see... 

- The tens digit gives a position to about 1,000 kilometers. It gives us useful information about what continent or ocean we are on.
- The units digit (one decimal degree) gives a position up to 111 kilometers (60 nautical miles, about 69 miles). It can tell us roughly what large state or country we are in.
- The first decimal place is worth up to 11.1 km: it can distinguish the position of one large city from a neighboring large city.
- The second decimal place is worth up to 1.1 km: it can separate one village from the next.
- The third decimal place is worth up to 110 m: it can identify a large agricultural field or institutional campus.
- The fourth decimal place is worth up to 11 m: it can identify a parcel of land. It is comparable to the typical accuracy of an uncorrected GPS unit with no interference.
- The fifth decimal place is worth up to 1.1 m: it distinguish trees from each other. Accuracy to this level with commercial GPS units can only be achieved with differential correction.
- The sixth decimal place is worth up to 0.11 m: you can use this for laying out structures in detail, for designing landscapes, building roads. It should be more than good enough for tracking movements of glaciers and rivers. This can be achieved by taking painstaking measures with GPS, such as differentially corrected GPS.
- The seventh decimal place is worth up to 11 mm: this is good for much surveying and is near the limit of what GPS-based techniques can achieve.
- The eighth decimal place is worth up to 1.1 mm: this is good for charting motions of tectonic plates and movements of volcanoes. Permanent, corrected, constantly-running GPS base stations might be able to achieve this level of accuracy.
- The ninth decimal place is worth up to 110 microns: we are getting into the range of microscopy. For almost any conceivable application with earth positions, this is overkill and will be more precise than the accuracy of any surveying device.
- Ten or more decimal places indicates a computer or calculator was used and that no attention was paid to the fact that the extra decimals are useless. Be careful, because unless you are the one reading these numbers off the device, this can indicate low quality processing!

We are clearly looking at data that is a result of a calculation.  We are deciding the most important fields in this dataset are ones relating to location analysis so we shall reduce all the locaation to having 2 decimal points which is approximately 1.1 km accuracy.


```python
new_df = master_df.copy()
gps_cols = ['Pickup_long', 'Pickup_lat', 'Dropoff_long', 'Dropoff_lat']
new_df[gps_cols] = new_df[gps_cols].replace(to_replace ="(^.*\.[0-9]{2}).*", value = r"\1", regex = True)
display(new_df.head())

```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Pickup</th>
      <th>Dropoff</th>
      <th>Pickup_long</th>
      <th>Pickup_lat</th>
      <th>Dropoff_long</th>
      <th>Dropoff_lat</th>
      <th>Sex</th>
      <th>Zip</th>
      <th>DOB</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2015-01-15 19:05:39</td>
      <td>2015-01-15 19:23:42</td>
      <td>-73.99</td>
      <td>40.75</td>
      <td>-73.97</td>
      <td>40.75</td>
      <td>M</td>
      <td>10889</td>
      <td>1968-07-20</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2015-01-10 20:33:38</td>
      <td>2015-01-10 20:53:28</td>
      <td>-74.00</td>
      <td>40.72</td>
      <td>-73.99</td>
      <td>40.75</td>
      <td>F</td>
      <td>10384</td>
      <td>1980-07-08</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2015-01-10 20:33:38</td>
      <td>2015-01-10 20:43:41</td>
      <td>-73.96</td>
      <td>40.80</td>
      <td>-73.95</td>
      <td>40.82</td>
      <td>M</td>
      <td>10422</td>
      <td>1996-06-21</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2015-01-10 20:33:39</td>
      <td>2015-01-10 20:35:31</td>
      <td>-74.00</td>
      <td>40.71</td>
      <td>-74.00</td>
      <td>40.71</td>
      <td>F</td>
      <td>10847</td>
      <td>1964-08-08</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2015-01-10 20:33:39</td>
      <td>2015-01-10 20:52:58</td>
      <td>-73.97</td>
      <td>40.76</td>
      <td>-74.00</td>
      <td>40.74</td>
      <td>F</td>
      <td>10631</td>
      <td>1987-05-10</td>
    </tr>
  </tbody>
</table>
</div>


### Pickup and Dropoff Times

Pickup and dropoff times are precise down to the second of pickup and dropoff.  This seems unnecessarily detailed again whatever the analysis.  We could choose to group all trips taken per minute, per hour, per day.  We could drop the date completely and just have a 0-23 bucket structure. This could be a good example of where negotiation is required, depending on what kinds of analysis the city wants to run, balanced against the granularity and specificity of the data that can be released and maintain anonymity.  If we look at the dataset we can see all trips were taken in the month of January 2015, so we already have a high density and frequency of trips over date in this dataset.  We shall choose to group trips that were started in the same hour. We shall do the same for the Dropoff time. 


```python
time_cols = ['Pickup', 'Dropoff']
new_df[time_cols] = new_df[time_cols].replace(to_replace ="(^.*?):.*", value = r"\1", regex = True)
display(new_df.head())
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Pickup</th>
      <th>Dropoff</th>
      <th>Pickup_long</th>
      <th>Pickup_lat</th>
      <th>Dropoff_long</th>
      <th>Dropoff_lat</th>
      <th>Sex</th>
      <th>Zip</th>
      <th>DOB</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2015-01-15 19</td>
      <td>2015-01-15 19</td>
      <td>-73.99</td>
      <td>40.75</td>
      <td>-73.97</td>
      <td>40.75</td>
      <td>M</td>
      <td>10889</td>
      <td>1968-07-20</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2015-01-10 20</td>
      <td>2015-01-10 20</td>
      <td>-74.00</td>
      <td>40.72</td>
      <td>-73.99</td>
      <td>40.75</td>
      <td>F</td>
      <td>10384</td>
      <td>1980-07-08</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2015-01-10 20</td>
      <td>2015-01-10 20</td>
      <td>-73.96</td>
      <td>40.80</td>
      <td>-73.95</td>
      <td>40.82</td>
      <td>M</td>
      <td>10422</td>
      <td>1996-06-21</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2015-01-10 20</td>
      <td>2015-01-10 20</td>
      <td>-74.00</td>
      <td>40.71</td>
      <td>-74.00</td>
      <td>40.71</td>
      <td>F</td>
      <td>10847</td>
      <td>1964-08-08</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2015-01-10 20</td>
      <td>2015-01-10 20</td>
      <td>-73.97</td>
      <td>40.76</td>
      <td>-74.00</td>
      <td>40.74</td>
      <td>F</td>
      <td>10631</td>
      <td>1987-05-10</td>
    </tr>
  </tbody>
</table>
</div>


The Dropoff field does not seem to be adding much value at this granularity level so let's take the decision to delete it.


```python
new_df.drop(columns=['Dropoff'], inplace=True)
display(new_df.head())
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Pickup</th>
      <th>Pickup_long</th>
      <th>Pickup_lat</th>
      <th>Dropoff_long</th>
      <th>Dropoff_lat</th>
      <th>Sex</th>
      <th>Zip</th>
      <th>DOB</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2015-01-15 19</td>
      <td>-73.99</td>
      <td>40.75</td>
      <td>-73.97</td>
      <td>40.75</td>
      <td>M</td>
      <td>10889</td>
      <td>1968-07-20</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2015-01-10 20</td>
      <td>-74.00</td>
      <td>40.72</td>
      <td>-73.99</td>
      <td>40.75</td>
      <td>F</td>
      <td>10384</td>
      <td>1980-07-08</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2015-01-10 20</td>
      <td>-73.96</td>
      <td>40.80</td>
      <td>-73.95</td>
      <td>40.82</td>
      <td>M</td>
      <td>10422</td>
      <td>1996-06-21</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2015-01-10 20</td>
      <td>-74.00</td>
      <td>40.71</td>
      <td>-74.00</td>
      <td>40.71</td>
      <td>F</td>
      <td>10847</td>
      <td>1964-08-08</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2015-01-10 20</td>
      <td>-73.97</td>
      <td>40.76</td>
      <td>-74.00</td>
      <td>40.74</td>
      <td>F</td>
      <td>10631</td>
      <td>1987-05-10</td>
    </tr>
  </tbody>
</table>
</div>


### Date of Birth

The data contains the full date of birth. We shall make a judgement call and say that such granularity is not required and perhaps they are just needing to understand passenger age.  Instead we shall reduce this datafield to just contain year of birth.


```python
dob_cols = ['DOB']
new_df[dob_cols] = new_df[dob_cols].replace(to_replace ="(^.*?)-.*", value = r"\1", regex = True)
display(new_df.head())
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Pickup</th>
      <th>Pickup_long</th>
      <th>Pickup_lat</th>
      <th>Dropoff_long</th>
      <th>Dropoff_lat</th>
      <th>Sex</th>
      <th>Zip</th>
      <th>DOB</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2015-01-15 19</td>
      <td>-73.99</td>
      <td>40.75</td>
      <td>-73.97</td>
      <td>40.75</td>
      <td>M</td>
      <td>10889</td>
      <td>1968</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2015-01-10 20</td>
      <td>-74.00</td>
      <td>40.72</td>
      <td>-73.99</td>
      <td>40.75</td>
      <td>F</td>
      <td>10384</td>
      <td>1980</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2015-01-10 20</td>
      <td>-73.96</td>
      <td>40.80</td>
      <td>-73.95</td>
      <td>40.82</td>
      <td>M</td>
      <td>10422</td>
      <td>1996</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2015-01-10 20</td>
      <td>-74.00</td>
      <td>40.71</td>
      <td>-74.00</td>
      <td>40.71</td>
      <td>F</td>
      <td>10847</td>
      <td>1964</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2015-01-10 20</td>
      <td>-73.97</td>
      <td>40.76</td>
      <td>-74.00</td>
      <td>40.74</td>
      <td>F</td>
      <td>10631</td>
      <td>1987</td>
    </tr>
  </tbody>
</table>
</div>


## Outlier Analysis

The three fields of DOB (now limited to year of birth), sex and home zip code is consistent per individual over the whole dataset.  Let us focus on just these fields and see how they are already behaving over the whole dataset.



```python
pseudo_pii = new_df[['Zip', 'DOB', 'Sex']].copy()

analyse_table_k_anon (pseudo_pii)
```

    
    -----------------------
    
    Dataset K-Anon Analysis
    
    -----------------------
    
    Dataset size =  97950
    
    -----------------------
    
    K-Anonymity Min to Max Values
    



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Zip</th>
      <th>DOB</th>
      <th>Sex</th>
      <th>freq</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>10501</td>
      <td>1997</td>
      <td>F</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>10784</td>
      <td>1994</td>
      <td>M</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>10423</td>
      <td>1970</td>
      <td>M</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>10784</td>
      <td>1996</td>
      <td>F</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>10784</td>
      <td>1996</td>
      <td>M</td>
      <td>1</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>59995</th>
      <td>10703</td>
      <td>1991</td>
      <td>F</td>
      <td>7</td>
    </tr>
    <tr>
      <th>59996</th>
      <td>10013</td>
      <td>1956</td>
      <td>F</td>
      <td>7</td>
    </tr>
    <tr>
      <th>59997</th>
      <td>10452</td>
      <td>1978</td>
      <td>F</td>
      <td>8</td>
    </tr>
    <tr>
      <th>59998</th>
      <td>10606</td>
      <td>1964</td>
      <td>F</td>
      <td>8</td>
    </tr>
    <tr>
      <th>59999</th>
      <td>10177</td>
      <td>1964</td>
      <td>M</td>
      <td>8</td>
    </tr>
  </tbody>
</table>
<p>60000 rows × 4 columns</p>
</div>


    
    -----------------------
    
    
    Overall K-Anonymity Classification for dataset =  1 
    
    
    -----------------------
    


Just looking at these three fields, it is clear that individuals are not lost in buckets but rather individually identifiable. Even if we have no other context then we know there is danger of being able to identify these individuals. We are going to make the judgement call that granularity of zipcode is more important than demographic age data. We are going to further generalize the age to being born in a specific decade.


```python
pseudo_pii['DOB'] = pseudo_pii['DOB'].str[:3] + '0\'s'
analyse_table_k_anon (pseudo_pii)
```

    
    -----------------------
    
    Dataset K-Anon Analysis
    
    -----------------------
    
    Dataset size =  97950
    
    -----------------------
    
    K-Anonymity Min to Max Values
    



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Zip</th>
      <th>DOB</th>
      <th>Sex</th>
      <th>freq</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>10198</td>
      <td>2000's</td>
      <td>M</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>10481</td>
      <td>1950's</td>
      <td>M</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>10811</td>
      <td>2000's</td>
      <td>M</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>10481</td>
      <td>2000's</td>
      <td>M</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>10810</td>
      <td>2000's</td>
      <td>M</td>
      <td>1</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>10839</th>
      <td>10254</td>
      <td>1990's</td>
      <td>M</td>
      <td>23</td>
    </tr>
    <tr>
      <th>10840</th>
      <td>10355</td>
      <td>1980's</td>
      <td>M</td>
      <td>23</td>
    </tr>
    <tr>
      <th>10841</th>
      <td>10135</td>
      <td>1980's</td>
      <td>F</td>
      <td>23</td>
    </tr>
    <tr>
      <th>10842</th>
      <td>10084</td>
      <td>1990's</td>
      <td>F</td>
      <td>24</td>
    </tr>
    <tr>
      <th>10843</th>
      <td>10573</td>
      <td>1970's</td>
      <td>F</td>
      <td>24</td>
    </tr>
  </tbody>
</table>
<p>10844 rows × 4 columns</p>
</div>


    
    -----------------------
    
    
    Overall K-Anonymity Classification for dataset =  1 
    
    
    -----------------------
    


It is clear we are going to have remove the specificity of the ZIP code.  Each character in the Zip code defines a more specific location of address. See below courtesy of [loqate.com](https://www.loqate.com/resources/blog/what-is-a-zip-code/)

<img src="./images/zip_structure.png" width="70%"/>

Let us mask off the last 2 digits of the zip code and rerun the analysis.


```python
pseudo_pii['Zip'] = pseudo_pii['Zip'].str[:3] + '**'
analyse_table_k_anon (pseudo_pii)
```

    
    -----------------------
    
    Dataset K-Anon Analysis
    
    -----------------------
    
    Dataset size =  97950
    
    -----------------------
    
    K-Anonymity Min to Max Values
    



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Zip</th>
      <th>DOB</th>
      <th>Sex</th>
      <th>freq</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>100**</td>
      <td>2000's</td>
      <td>F</td>
      <td>43</td>
    </tr>
    <tr>
      <th>1</th>
      <td>105**</td>
      <td>2000's</td>
      <td>F</td>
      <td>46</td>
    </tr>
    <tr>
      <th>2</th>
      <td>101**</td>
      <td>2000's</td>
      <td>M</td>
      <td>46</td>
    </tr>
    <tr>
      <th>3</th>
      <td>108**</td>
      <td>2000's</td>
      <td>F</td>
      <td>47</td>
    </tr>
    <tr>
      <th>4</th>
      <td>103**</td>
      <td>2000's</td>
      <td>M</td>
      <td>49</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>115</th>
      <td>108**</td>
      <td>1980's</td>
      <td>M</td>
      <td>1149</td>
    </tr>
    <tr>
      <th>116</th>
      <td>102**</td>
      <td>1990's</td>
      <td>F</td>
      <td>1153</td>
    </tr>
    <tr>
      <th>117</th>
      <td>105**</td>
      <td>1990's</td>
      <td>M</td>
      <td>1154</td>
    </tr>
    <tr>
      <th>118</th>
      <td>109**</td>
      <td>1990's</td>
      <td>M</td>
      <td>1159</td>
    </tr>
    <tr>
      <th>119</th>
      <td>109**</td>
      <td>1980's</td>
      <td>M</td>
      <td>1163</td>
    </tr>
  </tbody>
</table>
<p>120 rows × 4 columns</p>
</div>


    
    -----------------------
    
    
    Overall K-Anonymity Classification for dataset =  43 
    
    
    -----------------------
    


With this level of information, we now have k-anonymity of 43 which far exceeds the industry standard of k-anon = 5.  We are using all our trip records here. Let us investigate how this changes if we reduce the number of records we have in the dataset we use for the analysis.  We shall map this out in a bar chart with the x-axis increasing with numbers of records included and the y-axis showing the resulting k-anonymity value.


```python
import matplotlib.pyplot as plt

def k_anon_bar_chart(df):
    print("\n-----------------------\n")
    print("K-Anon Bar Chart")
    print("\n-----------------------\n")

    print("Example first row of dataset\n")
    display(df.head(1))
    print("-----------------------\n")
    
    rows = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    k_values = []
    for x in rows:
        x_dataset = df.head(x * 10000)
        matches = x_dataset.value_counts(ascending=True)
        k_values.append(matches.values[0])

    title = "K-Anon Analysis w.r.t. # of records"

    colors = []
    for value in k_values:  # keys are the names of the boys
        if value < 5:
            colors.append("r")
        else:
            colors.append("g")

    plt.bar(rows, k_values, color=colors)
    for i in rows:
        plt.text(i, k_values[i - 1], k_values[i - 1], ha="center")
    plt.title(title)
    plt.xlabel("No of rows x 10,000")
    plt.xticks(rows)
    plt.ylabel("K-Anonymity Value")
    plt.show()

k_anon_bar_chart(pseudo_pii)
```

    
    -----------------------
    
    K-Anon Bar Chart
    
    -----------------------
    
    Example first row of dataset
    



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Zip</th>
      <th>DOB</th>
      <th>Sex</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>108**</td>
      <td>1960's</td>
      <td>M</td>
    </tr>
  </tbody>
</table>
</div>


    -----------------------
    



    
![svg](output_29_3.svg)
    


We can see we can achieve k-anonymity of 6 with only 20,000 records and k-anonymity of 41 with 90,000 records. This feels like a robust privacy centric dataset at this level.  Let us move these columns into our full data set and see how it looks.


```python
new_df['Zip'] = pseudo_pii['Zip']
new_df['DOB'] = pseudo_pii['DOB']
new_df['Sex'] = pseudo_pii['Sex']

display(new_df.head(3))
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Pickup</th>
      <th>Pickup_long</th>
      <th>Pickup_lat</th>
      <th>Dropoff_long</th>
      <th>Dropoff_lat</th>
      <th>Sex</th>
      <th>Zip</th>
      <th>DOB</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2015-01-15 19</td>
      <td>-73.99</td>
      <td>40.75</td>
      <td>-73.97</td>
      <td>40.75</td>
      <td>M</td>
      <td>108**</td>
      <td>1960's</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2015-01-10 20</td>
      <td>-74.00</td>
      <td>40.72</td>
      <td>-73.99</td>
      <td>40.75</td>
      <td>F</td>
      <td>103**</td>
      <td>1980's</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2015-01-10 20</td>
      <td>-73.96</td>
      <td>40.80</td>
      <td>-73.95</td>
      <td>40.82</td>
      <td>M</td>
      <td>104**</td>
      <td>1990's</td>
    </tr>
  </tbody>
</table>
</div>


## Summary

There is nothing we can do to reduce the specificity of the traditional sex field so for now we shall leave it as is. We shall do the same for the zip code until we understand if we need to remove the granularity in later analysis.  

We have greatly reduced the specificity and risk contained in the dataset. We have also reduced the amount of storage and processing required. Let's save the new dataset and compare its size versus the original dataset.


```python
new_df.to_csv("cleaned-trips.csv", index=False)

!ls -lh passenger-trips.csv cleaned-trips.csv
```

    -rw-r--r--  1 geoffhollingworth  staff   5.1M Jul 26 13:12 cleaned-trips.csv
    -rw-r--r--@ 1 geoffhollingworth  staff    13M Jul 16 15:05 passenger-trips.csv


We can see the new file size is a third the size of the original, and much less toxic therefore less risky.  Tremendous cost and efficiency savings can be made in addition to privacy management, through disciplined data management.  

This has been a fast introduction to how to view datasets from a mathematical k-anonymity perspective, to allow you to quantify risk with others in the organisation and beyond.  

Take these skills and tools and apply them to your own datasets, and/or play around with better solutions to the one contained here.  Be a Data Protector!

