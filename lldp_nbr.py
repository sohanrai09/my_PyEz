# Script to display LLDP Neighbor info for a given interface on a device
# Script uses one of the predefined PyEz Tables named LLDPNeighborTable

from jnpr.junos import Device
from jnpr.junos.op.lldp import LLDPNeighborTable
from rich.console import Console
from rich.table import Table

console = Console()

dev = Device(host='x.x.x.x', user='user', password='password')
dev.open()

interface = 'xe-0/1/1'

# Using the predefined table for LLDP neighbors in PyEz
lldp_table = LLDPNeighborTable(dev)
lldp_table.get()

# Filtering out only the info relevant for the interface, if not done, all the neighbors' info will be retrieved
lldp_nbr = lldp_table[interface]

# Define Rich table to display output to terminal
table = Table(title=f"[bold blue] LLDP neighbor info for {interface}", show_lines=True)
table.add_column("Local Intf", style="cyan")
table.add_column("Local Parent Intf", style="cyan")
table.add_column("Remote Chassis ID", style="cyan")
table.add_column("Remote Intf description", style="cyan")
table.add_column("Remote Intf", style="cyan")
table.add_column("Remote System name", style="cyan")


try:
    table.add_row(lldp_nbr.local_int, lldp_nbr.local_parent, lldp_nbr.remote_chassis_id, lldp_nbr.remote_port_desc,
                  lldp_nbr.remote_port_id, lldp_nbr.remote_sysname)
    console.print(table)

# Catch the exception when no LLDP neighbor info is found for the given interface
except AttributeError:
    console.print(f"[bold red] LLDP Neighbor info not found for {interface}")

dev.close()
