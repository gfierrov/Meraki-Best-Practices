import meraki
from prettytable import PrettyTable

def firmware(id,api):

    dashboard = meraki.DashboardAPI(api, output_log=False, print_console=False)

    #network_id = 'L_624311498344253855'
    #network_id = 'L_624311498344247493'
    network_id = id

    """Get the available version """
    response = dashboard.networks.getNetworkFirmwareUpgrades(
        network_id
    )

    """Get the current devices version"""
    responseDevices = dashboard.networks.getNetworkDevices(
        network_id
    )



    """Get the available firmware from every single meraki devices"""

    applianceFirmware = (response["products"]["appliance"]["availableVersions"])
    for firmware in applianceFirmware:
        availableAppl = (firmware["firmware"])
    switchFirmware = (response["products"]["switch"]["availableVersions"])
    for firmware in switchFirmware:
        availableSw = (firmware["firmware"])

    wirelessFirmware = (response["products"]["wireless"]["availableVersions"])
    for firmware in wirelessFirmware:
        availableWireless = (firmware["firmware"])



    """Get meraki current devices from a network"""
    listDevices = []
    for devices in responseDevices:
        settingsToPrint = {
            "name": devices["name"] if "name" in devices else None,
            "serial": devices["serial"] if "serial" in devices else None,
            "model": devices["model"] if "model" in devices else None,
            "firmware": devices["firmware"] if "firmware" in devices else None,
        }
        deviceName = (settingsToPrint["name"])
        deviceSerial = (settingsToPrint["serial"])
        deviceModel = (settingsToPrint["model"])
        deviceFirmware = (settingsToPrint["firmware"])
        listDevicesVar = [deviceName, deviceSerial, deviceModel, deviceFirmware]
        listDevices.append(listDevicesVar)

    """Print the availanle applicances versions"""
    #print(availableAppl)
    #print(availableSw)
    #print(availableWireless)


    """ Searching device string in current devices list and add the available version """
    search_appliance = "wired"
    search_switch = "switch"
    search_wireless = "wireless"


    for i in range(len(listDevices)):
        for j in range(len(listDevices[i])):
            if search_wireless in listDevices[i][j]:
                listDevices[i].append(availableWireless)
            if search_switch in listDevices[i][j]:
                listDevices[i].append(availableSw)
            if search_appliance in listDevices[i][j]:
                listDevices[i].append(availableAppl)


    """Put the info into a Pretty Table """
    table = PrettyTable()
    table.title = "Firmware"
    table.field_names=["Name", "Serial", "Model",  "Current Version", "Available Version"]
    for row in listDevices:
        table.add_row(row)
    print()
    print(table)
    print()






