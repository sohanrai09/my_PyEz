# Script to fetch the BGP details for a Peer address
# Details include, peer & local address, peer AS, peer type, peer state, advertised & received prefixes

from jnpr.junos import Device
from rich.console import Console
from rich.table import Table


dev = Device(host='x.x.x.x', user='user', password='password')
dev.open()

peer = '30.1.1.11'

# CLI equivalent of 'show bgp neighbor <peer>'
bgp_result = dev.rpc.get_bgp_neighbor_information(neighbor_address=peer)

local_addr = bgp_result.findtext(".//local-address").split('+')[0]
peer_addr = bgp_result.findtext(".//peer-address").split('+')[0]
peer_as = bgp_result.findtext(".//peer-as")
peer_type = bgp_result.findtext(".//peer-type")
peer_state = bgp_result.findtext(".//peer-state")

if peer_state == 'Established':
    adv_prefix = bgp_result.findtext(".//bgp-rib/advertised-prefix-count")
    rcvd_prefix = bgp_result.findtext(".//bgp-rib/received-prefix-count")
else:
    adv_prefix = 'NA'
    rcvd_prefix = 'NA'

# Rich table for terminal display of output
table = Table(title=f"[bold blue] BGP details for peer {peer}", show_lines=True)
table.add_column("Peer Address", style="cyan")
table.add_column("Local Address", style="cyan")
table.add_column("Peer AS", style="cyan")
table.add_column("Peer Type", style="cyan")
table.add_column("Peer State", style="green")
table.add_column("Advertised Prefixes", style="cyan")
table.add_column("Rcvd Prefixes", style="cyan")

table.add_row(local_addr, peer_addr, peer_as, peer_type, peer_state, adv_prefix, rcvd_prefix)

console = Console()
console.print(table)

dev.close()
