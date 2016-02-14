from django.shortcuts import render
import urllib2
import re
import json
from pandas.io.json import json_normalize

"""
The supplied API endpoints are JS callbacks.
So, we need to clean them up so we can parse the file.
This function takes in the API endpoint URL, cleans up the JS callback, parses the JSON, and returns a normalized JSON object.
"""    
def load_data(url):
    output = urllib2.urlopen(url)
    request = output.read()

    modified_request = re.sub(re.compile(r'/\*.*\*/\n', re.DOTALL), '', request)
    modified_request = re.sub(r'^callback\(', '', modified_request)
    modified_request = re.sub(r'\);*$', '', modified_request)

    obj = json.loads(modified_request)
    return obj

def normalize_data(data):
    normalized_data = json_normalize(data,'regions',['region','instanceType'])
    return normalized_data

# Create your views here.
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

