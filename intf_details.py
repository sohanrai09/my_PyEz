# Script to fetch the status and IP address (v4 & v6) of an Interface using PyEz.
# All the Sub Interfaces/Units' details will be captured
# Script uses RPC instead of screen scraping.

from jnpr.junos import Device
from rich.console import Console
from rich.table import Table


dev = Device(host='x.x.x.x',user='user',password='password')
dev.open()

# Interface to be checked
interface = 'et-0/3/0'

# Define Rich table to display output to termial
table = Table(title=f"[bold blue] Details for {interface}",show_lines=True)
table.add_column("Interface Name", style="yellow")
table.add_column("Admin Status", style="green")
table.add_column("Oper Status", style="green")
table.add_column("IPv4 address", style="cyan")
table.add_column("IPv6 address", style="cyan")

# Function to fetch the status and IP address (v4 & v6) of the Interface, returns Rich table for display
def intf_status_check(intf):

    rpc_result = dev.rpc.get_interface_information(terse=True, interface_name=intf)
    sub_interfaces = rpc_result.findall(".//logical-interface")

    # Find all the SubInterfaces and iterate over them to find the IP details and Status
    for sub_intf in sub_interfaces:
        ip_addr = sub_intf.findall(".//address-family")
        intf_name = sub_intf.findtext("./name")
        admin_status = sub_intf.findtext("./admin-status")
        oper_status = sub_intf.findtext("./oper-status")

        for ip in ip_addr:

            if (ip.findtext("./address-family-name")).strip() == 'inet':
                ipv4_addr = ip.findtext("./interface-address/ifa-local")

            elif (ip.findtext("./address-family-name")).strip() == 'inet6':
                ipv6_addr = ip.findtext("./interface-address/ifa-local")

        table.add_row(intf_name.strip(), admin_status.strip(), oper_status.strip(), ipv4_addr.strip(), ipv6_addr.strip())

    return table

# Invoke the function
table = intf_status_check(interface)

dev.close()

console = Console()
console.print(table)

