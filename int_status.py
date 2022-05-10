# Script to fetch the Admin and Operational status of an Interface using PyEz.
# Script uses RPC instead of configuration scrapping.


from jnpr.junos import Device


dev = Device(host='x.x.x.x',user='user',password='password')
dev.open()


# List of interfaces to check
intf_list = ['xe-1/0/0','et-0/2/0','ge-0/0/0']


# Function to fetch the Admin and Operational status of the Interface
def intf_status_check(intf):
    rpc_result = dev.rpc.get_interface_information(terse=True, interface_name=intf)
    admin_status = rpc_result.find(".//admin-status")
    oper_status = rpc_result.find(".//oper-status")
    return admin_status.text.strip(), oper_status.text.strip()


for interface in intf_list:
    admin, oper = intf_status_check(interface)
    print("*" * 20)
    print(interface, admin, oper)

print("*" * 20)

dev.close()
