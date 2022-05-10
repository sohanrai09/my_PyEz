# Script to fetch the System Alarms currently active on the device
# Output is the CLI equivalent of 'show system alarms'


from jnpr.junos import Device
from rich.console import Console
from rich.table import Table


dev = Device(host='x.x.x.x', user='user', password='password')
dev.open()
hostname = dev.facts['hostname']

# Define Rich table to display output to the terminal
table = Table(title=f"[bold green] System Alarms for {hostname}", show_lines=True)
table.add_column("Alarm Time", style="blue")
table.add_column("Class")
table.add_column("Description", style="cyan")
table.add_column("Type", style="blue")

# RPC equivalent of 'show system alarms'
rpc_result = dev.rpc.get_alarm_information()
alarms_xml = rpc_result.findall("./alarm-detail")

for alarm in alarms_xml:
    alarm_time = alarm.findtext("./alarm-time")
    alarm_class = alarm.findtext("./alarm-class")
    alarm_description = alarm.findtext("./alarm-description")
    alarm_type = alarm.findtext("./alarm-type")

    if alarm_class == 'Major':
        table.add_row(alarm_time.strip(), f"[bright_red]{alarm_class}[/bright_red]", alarm_description, alarm_type)

    else:
        table.add_row(alarm_time.strip(), f"[dark_orange]{alarm_class}[/dark_orange]", alarm_description, alarm_type)

dev.close()

console = Console()
console.print(table)
