import requests,json


def uplinkLB(id,api):

    url = "https://api.meraki.com/api/v1/networks/"+id+"/appliance/trafficShaping/uplinkSelection"

    payload = None

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Cisco-Meraki-API-Key": api
    }

    response = requests.request('GET', url, headers=headers, data = payload)

    #obtain from json loadbalance
    loadbalance = json.loads(response.text)

    # to get ride of nested dictionary
    loadbalance = loadbalance['loadBalancingEnabled']

    # validate if the load balance is true or false
    if loadbalance:
        print("Load Balancing: Enabled \n")

    else:
        print("Load Balancing: Disabled \n")

        print("It is recommended to have the uplink connections be set to \n "
              "load balance the traffic if applicable. \n")

