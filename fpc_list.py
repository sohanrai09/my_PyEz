# Script to extract the list of FPCs installed in the router
# Equivalent of CLI command 'show chassis hardware clei-models' but formatted into a tabular format
# Script uses RPC instead of screen scrapping.


from jnpr.junos import Device
from tabulate import tabulate

# List of devices
host_ip_list = ['x.x.x.x']


# Function to fetch the FPCs and build a table for display
def fetch_fn(host_ip):
    dev = Device(host=host_ip, user='user', password='password')
    dev.open()
    hostname = dev.facts['hostname']

    # RPC equivalent of 'show chassis hardware'
    hardware_rpc = dev.rpc.get_chassis_inventory()
    fpc_list = hardware_rpc.findall(".//chassis-module/description")
    slot_list = hardware_rpc.findall(".//chassis-module/name")

    out_dict = dict(zip(slot_list, fpc_list))
    out_list = []

    # Iterate over the extracted details to only fetch FPCs. Other details include REs,SCBs,PEMs which can also be retrieved
    for slot, fpc in out_dict.items():
        fpc_name = fpc.text
        slot_name = slot.text

        if "FPC" in slot_name:
            out_list.append([slot_name, fpc_name])

    print("\n")
    print(f"FPCs installed on Device {hostname} are listed below")
    print(tabulate(out_list, tablefmt='fancy_grid'))
    print("\n")
    dev.close()


for host_ip in host_ip_list:
    fetch_fn(host_ip)