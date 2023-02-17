import requests,json
import pandas as pd
from datetime import datetime

def uplinkBW(id,api):

    url = "https://api.meraki.com/api/v1/networks/"+id+"/appliance/trafficShaping/uplinkBandwidth"

    payload = None

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Cisco-Meraki-API-Key": api
    }

    response = requests.request('GET', url, headers=headers, data = payload)

    bwlimits = json.loads(response.text)

    #to get rid of nested dictionary
    bwlimits=bwlimits['bandwidthLimits']

    df = pd.DataFrame(bwlimits)
    print("Bandwith Limits:")
    print(df)
    csvNetVar = datetime.now().strftime("%m-%d-%Y-%Hh%Mm.csv")
    df.to_csv(csvNetVar, index=False)
    print()
    print(" It is best practice to set the throughput bandwidth to the highest possible\n "
          "amount based on your bandwidth set by your provider as to avoid potentially\n "
          "saturating the connection. ")
    print()
    return df

    #print(response.text.encode('utf8'))


