import meraki
from prettytable import PrettyTable

def firmware(id,api):

    dashboard = meraki.DashboardAPI(api, output_log=False, print_console=False)

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

    """Print the available applicances versions"""
    #print(availableAppl)
    #print(availableSw)
    #print(availableWireless)
    #print(listDevices)


    """ Searching device string in current devices list and add the available version """
    search_appliance = "wired"
    search_switch = "switch"
    search_wireless = "wireless"
    search_notConfigVersion = "Not"


    for i in range(len(listDevices)):
        for j in range(len(listDevices[i])):
            if search_wireless in listDevices[i][j]:
                listDevices[i].append(availableWireless)
            elif search_switch in listDevices[i][j]:
                listDevices[i].append(availableSw)
            elif search_appliance in listDevices[i][j]:
                listDevices[i].append(availableAppl)
            #Fix the "Not running current verion" in the devices list
            elif search_notConfigVersion in listDevices[i][j]:
                data = str(deviceModel)
                if data.startswith("MR"):
                    listDevices[i].append(availableWireless)
                elif data.startswith("MX"):
                    listDevices[i].append(availableAppl)
                elif data.startswith("MS"):
                    listDevices[i].append(availableSw)

    #Check responses
    print(response)
    print(responseDevices)
    print(listDevices)

    """Put the info into a Pretty Table """
    table = PrettyTable()
    table.title = "Firmware"
    table.field_names=["Name", "Serial", "Model",  "Current Version", "Available Version"]
    for row in listDevices:
        table.add_row(row)
    print()
    print(table)
    print()
    # Create a CSV file fom the meraki organization policy objects
    with open("Meraki_Firwmare.csv", "w", newline="") as file_output:
        file_output.write(table.get_csv_string())






