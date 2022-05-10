# my_PyEz
Collection of PyEz scripts for network automation of Junos devices.

PyEz is a python library to interact with Junos devices [Documentation](https://www.juniper.net/documentation/product/us/en/junos-pyez) . As I'm learning to work with PyEz, I wanted to share some simple scripts I wrote to help me along the way.

The best thing about PyEz is the interaction with devices using RPCs(Remote Procedure Calls). This is an effecient way of interacting with devices to fetch details rather than 'screen scraping'. 

For any command you wish to know the the RPC, you can find it easily from the CLI. In the below example, *get-software-information* would be the RPC equivalent for CLI command *show version*

```
show version | display xml rpc   
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/20.4R0/junos">
    <rpc>
        <get-software-information>
        </get-software-information>
    </rpc>
    <cli>
        <banner></banner>
    </cli>
```

Output of the RPC will be in XML format, and you can see the output you'd get for the RPC, using CLI (below output has been shortened).

```
show version | display xml        
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/20.4R0/junos">
    <software-information>
        <host-name>wf-york</host-name>
        <product-model>mx480</product-model>
        <product-name>mx480</product-name>
        <junos-version>20.4R3-S3.4</junos-version>
        <package-information>
            <name>os-kernel</name>
            <package-name>os-kernel-prd-x86-64-20220228.d118be0_builder_stable_11-204ab</package-name>
            <comment>JUNOS OS Kernel 64-bit  [20220228.d118be0_builder_stable_11-204ab]</comment>
        </package-information>
```

Once you know the expected output, then you can use different ways to work around the XML output to extract the relevant information. There are a ton of resources to help you get started with XML, my personal preference is [XML Tree](https://docs.python.org/3/library/xml.etree.elementtree.html#xpath-support).


Other great resources on PyEz

https://github.com/vnitinv/pyez-examples
