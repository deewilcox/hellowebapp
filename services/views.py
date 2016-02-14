from django.shortcuts import render
import urllib2
import re
import json
from pandas.io.json import json_normalize

# Define functions specific to the application

"""
The supplied API endpoints are JS callbacks.
So, we need to clean them up so we can parse the file.
This function takes in the API endpoint URL, cleans up the JS callback, parses the JSON, and returns a normalized JSON object.
"""    

define clean_output(json_string):
    modified_json_string = re.sub(re.compile(r'/\*.*\*/\n', re.DOTALL), '', json_string)
    modified_json_string = re.sub(r'^callback\(', '', modified_json_string)
    modified_json_string = re.sub(r'\);*$', '', modified_json_string)
    return modified_json_string

def load_data(url):
    output = requests.get(url)
    # Not using requests.json() here because the API does not hand back clean json
    request = output.text
    modified_request = clean_output(request)
    obj = json.loads(modified_request)
    return obj

""" 
This funciton is not in use, but keeping to revisit at a later time.
Initially, I planned to use json_normalize and pandas to plot the data. 
However, I ran into an error getting beyond json_normalize(data,['instanceTypes',['sizes']],'region') and into the pricing data.
It will be less efficient, but will need to iterate over the data and built the dictionary that I need.
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

    spot = load_data(url1)
    data1 = spot['config']['regions']
    spot_data =  normalize_data(data1)

    #ec2 = load_data(url2)
    #data2 = ec2['config']['regions']
    #ec2_data = normalize_data(data2)

    return render(request, 'index.html',{
        'spot_data':spot_data,
        'spot_heading':'This is normalized data for AWS Spot instance pricing',
        'ec2_data':'',
        'ec2_heading':'This is normalized data for AWS EC2 instance pricing'
    })

