import xml.dom.minidom as mini
from pprint import pprint
import json
import xmltodict
from ncclient import manager
import webex as webex

host = '192.168.56.101'
port = '830'
user = 'netconf'
password = 'netconf'


def get_capablities():
    router = {
        'host': host,
        'port': port,
        'username': user,
        'password': password,
        'hostkey_verify': False
    }
    try:
        with manager.connect(**router) as connection:
            for capability in connection.server_capabilities:
                print(capability)
    except Exception as e:
        print(e)
        # raise "Connection Failed"


def get_running_config():
    try:
        with manager.connect(
                host=host,
                port=port,
                username=user,
                password=password,
                hostkey_verify=False
        ) as connection:
            response = connection.get_config("running")
            running_config = xmltodict.parse(response.xml)
            print(mini.parseString(response.xml).toprettyxml())
            # print(json.dumps(running_config, indent=2, sort_keys=True))
            return running_config
    except Exception as e:
        print(e)


def get_users():
    try:
        with manager.connect(
                host=host,
                port=port,
                username=user,
                password=password,
                hostkey_verify=False
        ) as connection:
            netconf_filter = '''
            <filter>
                <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                    <username>
                    </username>
                </native>
            </filter>
            '''
            response = connection.get(netconf_filter)
            # print(mini.parseString(response.xml).toprettyxml())
            usernames = xmltodict.parse(response.xml)
            print(json.dumps(usernames, indent=2, sort_keys=True))
    except Exception as e:
        print(e)


def edit_user(u, p, pl):
    try:
        with manager.connect(
                host=host,
                port=port,
                username=user,
                password=password,
                hostkey_verify=False
        ) as connection:
            config_template = '''
            <config>
                <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                    <username>
                        <name>{user}</name>
                            <privilege>{privilege_level}</privilege>
                            <password>
                                    <encryption>0</encryption>
                                    <password>{pw}</password>
                            </password>
                    </username>
                </native>
            </config>
            '''
            netconf_config = config_template.format(
                user=u, privilege_level=pl, pw=p
            )
            response = connection.edit_config(netconf_config, target="running")
    except Exception as e:
        print(e)


def delete_user(u, p, pl):
    try:
        with manager.connect(
                host=host,
                port=port,
                username=user,
                password=password,
                hostkey_verify=False
        ) as connection:
            config_template = '''
            <config>
                <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                    <username operation="delete">
                        <name>{user}</name>
                            <privilege>{privilege_level}</privilege>
                            <password>
                                    <encryption>0</encryption>
                                    <password>{pw}</password>
                            </password>
                    </username>
                </native>
            </config>
            '''
            netconf_config = config_template.format(
                user=u, privilege_level=pl, pw=p
            )
            response = connection.edit_config(netconf_config, target="running")
    except Exception as e:
        print(e)


def edit_hostname(hostname):
    try:
        with manager.connect(
                host=host,
                port=port,
                username=user,
                password=password,
                hostkey_verify=False
        ) as connection:
            CONFIGURATION = f'''
            <config>
                <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                    <hostname>{hostname}</hostname>
                </native>
            </config>
            '''
            netconf_config = CONFIGURATION.format(
                hostname=hostname
            )
            response = connection.edit_config(netconf_config, target="running")
    except Exception as e:
        print(e)


# function to edit given interface


def add_loopback():
    try:
        with manager.connect(
                host=host,
                port=port,
                username=user,
                password=password,
                hostkey_verify=False
        ) as connection:
            netconf_loopback = """
            <config>
                <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                    <interface>
                        <Loopback>
                            <name>1</name>
                            <description>My first Loopback</description>
                            <ip>
                                <address>
                                    <primary>
                                        <address>10.1.1.1</address>
                                        <mask>255.255.255.0</mask>
                                    </primary>
                                </address>
                            </ip>
                        </Loopback>
                    </interface>
                </native>
            </config>
                """

            netconf_reply = connection.edit_config(target="running", config=netconf_loopback)
    except Exception as e:
        print(e)


# edit gigabitethernet interface
def edit_gigabitethernet(int_name, int_desc, ip_addr, ip_mask):
    try:
        with manager.connect(
                host=host,
                port=port,
                username=user,
                password=password,
                hostkey_verify=False
        ) as connection:
            config_template = '''

	<config>
		<interfaces
			xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
			<interface>
				<name>GigabitEthernet1</name>
				<description>VBox</description>
				<type
					xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd
				</type>
				<enabled>true</enabled>
				<ipv4
					xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"/>
					<ipv6
						xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"/>
					</interface>
				</interfaces>
			</config>

                '''

            netconf_config = config_template.format(
                int_name=int_name, int_desc=int_desc, ip_addr=ip_addr, ip_mask=ip_mask
            )
            response = connection.edit_config(netconf_config, target="running")
    except Exception as e:
        print(e)


get_running_config()
#edit_hostname("Switch1")
#webex.webexSend("Network Configuration has been updated")