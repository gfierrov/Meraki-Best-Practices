API_KEY = "2a67ac33ea4ddf9e02d495802c5aacbc50303976"
import meraki
import requests, json, time, datetime
from MerakiBW import uplinkBW
from MerakiRFProfile import rfProfile
from MerakiFirmwareCode import firmware
from prettytable import PrettyTable

geturl = "https://api.meraki.com/api/v1/organizations"
payload={}
headers = {'x-cisco-meraki-api-key': format(str(API_KEY)), 'Content-Type': 'application/json'}


response = requests.request("GET",geturl, headers=headers, data= payload)
allOrgs= json.loads(response.text)

print(response.text.encode('utf8'))
#print(allOrgs)

#prints all the available organizations for the given API Key
print("Your available organizations:")
for idx, orgs in enumerate(allOrgs):
    print(str(idx + 1) + ") " +  orgs["name"])

#method for user to choose a valid index
def ask_index(length):
    index = input("Enter a valid index: ")

    is_numeric=False
    in_range=False

    if index.isnumeric():
        is_numeric=True
        index=int(index)
        if index > 0 and index <=length:
            in_range=True

    while is_numeric==False or in_range==False:
        index = input("Enter a valid index: ")
        if index.isnumeric():
            index=int(index)
            if index>len(allOrgs):
                print("Index out of range")
            elif index>0 and index <=length:
                is_numeric=True
                in_range=True

    index=int(index)-1
    return index

index=ask_index(len(allOrgs))
id = allOrgs[index]["id"]
print(allOrgs[index]["name"])

networksURL = "https://api.meraki.com/api/v1/organizations/" + id +"/networks"
responseNetworks = requests.request("GET",networksURL, headers=headers, data= payload)
while responseNetworks.status_code==404:
    print("No API access to this network. Choose another network or provide API access")
    index = ask_index(len(allOrgs))
    id = allOrgs[index]["id"]
    print(allOrgs[index]["name"])
    print()
    networksURL = "https://api.meraki.com/api/v1/organizations/" + id + "/networks"
    responseNetworks = requests.request("GET", networksURL, headers=headers, data=payload)

allNetworks= json.loads(responseNetworks.text)

print("Networks in the selected organization:")

for idx, networks in enumerate(allNetworks):
    print(str(idx + 1) + ") " +  networks["name"])

index=ask_index(len(allNetworks))
id2 = allNetworks[index]["id"]
print(allNetworks[index]["name"])
print()
devicesURL = "https://api.meraki.com/api/v1/networks/" + id2 +"/devices"


uplinkBW(id2,API_KEY)
rfProfile(id2,API_KEY)
firmware(id2,API_KEY)


responseDevices = requests.request("GET",devicesURL, headers=headers, data= payload)
allDevices= json.loads(responseDevices.text)
#print(responseDevices.text.encode('utf8'))
print("Network Devices:")
for devices in allDevices:
    print("Model: {}\t SN: {}".format(devices["model"],devices["serial"]))












