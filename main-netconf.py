from ncclient import manager #Provides connection to NETCONF
import xml.dom.minidom #Prettifies XML using python
import webex as webex #For sending messages to Webex Teams

def getCurrentConfig(str_divider):
    #GETTING THE CURRENT RUNNING CONFIG OF CSR1kv
    current_config = m.get_config(source="running", filter=netconf_filter)
    print(str_divider)
    print(xml.dom.minidom.parseString(current_config.xml).toprettyxml())

def modifyCurrentConfig():
    #MODIFYING THE CURRENT CONFIG's HOSTNAME
    m.edit_config(target="running", config=netconf_newConfig)
    getCurrentConfig("-------------------------------------------------------THIS IS THE MODIFIED RUNNING CONFIG-------------------------------------------------------")


#MAIN METHOD
m = manager.connect(
    host = "192.168.56.104",
    port="830",
    username="cisco",
    password="cisco123!",
    hostkey_verify=False,
)

#DATAFIELDS that will be changed
newConfig = {
    "hostname": "NewHostname",
    "motd": "#Welcome_to_the_CLI_interface_of_CSR1000v",
    "GigDescription" : "Description for GigEthernet01",
    "ip": "10.1.1.1",
    "mask": "255.255.255.0"
}

#Filter is used to only retrieve the specific YANG model by cisco IOS XE 
netconf_filter = """
<filter>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native" />
</filter>
"""


#This is the new config that will change the current config
netconf_newConfig=f"""
<config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <banner>
            <motd>
                <banner>{newConfig['motd']}</banner>
            </motd>
        </banner>
        <hostname>{newConfig['hostname']}</hostname>
        <interface>
            <GigabitEthernet>
                <name>1</name>
                <description>{newConfig['GigDescription']}</description>
        </GigabitEthernet>
        <Loopback>
            <name>1</name>
            <description>Loopback1</description>
            <ip>
                <address>
                    <primary>
                        <address>{newConfig['ip']}</address>
                        <mask>{newConfig['mask']}</mask>
                    </primary>
                </address>
            </ip>
        </Loopback>
        </interface>
    </native>
</config>
"""

#METHODS
getCurrentConfig("-------------------------------------------------------THIS IS THE CURRENT RUNNING CONFIG-------------------------------------------------------")
modifyCurrentConfig()

newField = f"""
FIELDS THAT WERE CHANGED

MESSAGE OF THE DAY to: {newConfig['motd']}
HOSTNAME to: {newConfig['hostname']}
Gigabit Ethernet 1 DESCRIPTION to: {newConfig['GigDescription']}
Loopback 1 IP to: {newConfig['ip']}
Loopback 1 MASK to: {newConfig['mask']}
"""
print(newField)
webex.webexSend(newField)