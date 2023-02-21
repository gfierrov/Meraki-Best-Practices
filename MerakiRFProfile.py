import meraki, pandas

def rfProfile(id,api):

    dashboard = meraki.DashboardAPI(api,output_log=False,print_console=False)

    network_id = id

    response = dashboard.wireless.getNetworkWirelessRfProfiles(
        network_id
    )

    if len(response)!=0:
        profile = response[0]

        profile24=profile['twoFourGhzSettings']
        profile5 = profile['fiveGhzSettings']

        print('2.4 Ghz Profile:')
        bestPractice=True
        for idx in profile24:
            if 'minBitrate' in idx:
                print(idx, profile24[idx])
                print()
                if profile24[idx]<12:
                    bestPractice=False
        print('5 Ghz Profile:')

        for idx in profile5:
            if 'minBitrate' in idx:
                print(idx, profile5[idx])
                print()
                if profile5[idx]<12:
                    bestPractice=False

        if bestPractice:
            print("Minimum mandatory data rate 12 Mbps or above")
        else:
            print("Minimum mandatory data rate below 12 Mbps")
        print()
    else:
        print("No RF Profiles")