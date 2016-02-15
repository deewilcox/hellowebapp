from django.shortcuts import render
import urllib2
import re
import json
import demjson
import matplotlib.pyplot as plt
import numpy as np

#import pandas
#from pandas.io.json import json_normalize

# Define functions specific to the application

"""
The supplied API endpoints are JS callbacks.
So, we need to clean them up so we can parse the file.
This function takes in the API endpoint URL, cleans up the JS callback, parses the JSON, and returns a normalized JSON object.
"""    

def clean_output(json_string):
    modified_json_string = re.sub(re.compile(r'/\*.*\*/\n', re.DOTALL), '', json_string)
    modified_json_string = re.sub(r'^callback\(', '', modified_json_string)
    modified_json_string = re.sub(r'\);*$', '', modified_json_string)
    return modified_json_string

def load_data(url,service_type):
    output = requests.get(url)
    # Not using requests.json() here because the API does not hand back clean json
    request = output.text
    modified_request = clean_output(request)

    if service_type == 'spot':
        obj = json.loads(modified_request)
    elif service_type == 'ec2':
        obj = demjson.decode(modified_request)
    else:
        obj = modified_request
    
    return obj

def prepare_instance_data(data):
    # Initialize empty chart_data dictionary. 
    chart_data = {} 
    instance_types = data[0]['instanceTypes'][0]

    # Parse through data and build spread of prices by region, instance type, size, and price
    for instance in data:
        if 'region' in instance and instance['region']:
            region = instance['region']

        for instance_type in instance['instanceTypes']:
            type_name = instance_type[u'type']
            
            for sizes in instance_type['sizes']:
                size = sizes[u'size']
                if 'valueColumns' in sizes and sizes['valueColumns']:
                    for columns in sizes['valueColumns']:
                        name = columns[u'name']
                        label_name = region + '_' + type_name + '_' + name + '_' + size
                        price = columns[u'prices'][u'USD']
                        if price:
                            chart_data[label_name]=round(float(price),2)

    return chart_data 

def chart_instance(chart_data):
    labels = []
    values = []
     
    for instance_label, price in chart_data:
        labels.insert(0, instance_label)
        values.insert(0, price)
        
    ind = np.arange(len(values))
    fig = plt.figure(figsize=(len(labels) * 1.8, 10))

    ax = fig.add_subplot(1, 1, 1)
    ax.bar(ind, values, 0.3, align='center')

    plt.ylabel('Instance Prices')
    plt.xlabel('Instance Region, Size, and Type')
    ax.set_xticks(ind + 0.3)
    ax.set_xticklabels(labels)
    plt.grid(True)
    plt.show()
    return plt

""" 
This function is not in use, but keeping to revisit at a later time.
Initially, I planned to use json_normalize and pandas to plot the data. 
However, I ran into an error getting beyond json_normalize(data,['instanceTypes',['sizes']],'region') and into the pricing data.
It will be less efficient, but I will instead iterate over the data and built the dictionary that I need.
"""

def normalize_data(data):
    normalized_data = json_normalize(data,['instanceTypes',['sizes']],'region')
    return normalized_data

# Define functions specific to loading views
def index(request):
    return render(request, 'index.html',{
        'greeting':'View Current Pricing for AWS EC2 and Spot Instances',
    })

def services(request):
    url1 = 'http://spot-price.s3.amazonaws.com/spot.js'
    url2 = 'http://a0.awsstatic.com/pricing/1/ec2/linux-od.min.js'

    spot = load_data(url1,'spot')
    data1 = spot['config']['regions']
    spot_data =  normalize_data(data1)

    #ec2 = load_data(url2,'ec2')
    #data2 = ec2['config']['regions']
    #ec2_data = normalize_data(data2)

    return render(request, 'index.html',{
        'spot_data':spot_data,
        'spot_heading':'This is a data visualization for AWS Spot instance pricing',
        'ec2_data':'',
        'ec2_heading':'This is a data visualization for AWS EC2 instance pricing'
    })

