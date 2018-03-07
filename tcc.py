#!/usr/bin/env python
"""
vlanhost.py: Host subclass that uses a VLAN tag for the default interface.

Dependencies:
    This class depends on the "vlan" package
    $ sudo apt-get install vlan

Usage (example uses VLAN ID=1000):
    From the command line:
        sudo mn --custom vlanhost.py --host vlan,vlan=1000

    From a script (see exampleUsage function below):
        from functools import partial
        from vlanhost import VLANHost

        ....

        host = partial( VLANHost, vlan=1000 )
        net = Mininet( host=host, ... )

    Directly running this script:
        sudo python vlanhost.py 1000

"""
import sys
from functools import partial
from mininet.topo import Topo
from mininet.util import quietRun
from mininet.log import error, setLogLevel, info
from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController,Controller, Host
from mininet.clean import cleanup
from mininet.topolib import TreeTopo
from mininet.link import Link, TCLink, Intf
from mininet.cli import CLI


class VLANHost( Host ):
    "Host connected to VLAN interface"

    def config( self, vlan=2, **params ):
        """Configure VLANHost according to (optional) parameters:
           vlan: VLAN ID for default interface"""

        r = super( VLANHost, self ).config( **params )

        intf = self.defaultIntf()
        # remove IP from default, "physical" interface
        self.cmd( 'ifconfig %s inet 0' % intf )
        # create VLAN interface
        self.cmd( 'vconfig add %s %d' % ( intf, vlan ) )
        # assign the host's IP to the VLAN interface
        self.cmd( 'ifconfig %s.%d inet %s' % ( intf, vlan, params['ip'] ) )
        # update the intf name and host's intf map
        newName = '%s.%d' % ( intf, vlan )
        # update the (Mininet) interface to refer to VLAN interface name
        intf.name = newName
        # add VLAN interface to host's name to intf map
        self.nameToIntf[ newName ] = intf

        return r

hosts = { 'vlan': VLANHost }


def exampleAllHosts( ):
    """Simple example of how VLANHost can be used in a script"""
    # This is where the magic happens...
    #host = partial( VLANHost, vlan=vlan )
    # vlan (type: int): VLAN ID to be used by all hosts

    # Start a basic network using our VLANHost
    #topo = SingleSwitchTopo( k=2 )
    topo=VLANStarTopo(k=2, n=2) 
    net = Mininet(switch=OVSSwitch, topo=topo )

    net.addController('c1', controller=RemoteController, ip='127.0.0.1', port=6633)
    net.addController('c2', controller=RemoteController, ip='192.168.27.11', port=6633)

    net.start()
    CLI( net )
    net.stop()

# pylint: disable=arguments-differ

class VLANStarTopo( Topo ):
    """Example topology that uses host in multiple VLANs

       The topology has a single switch. There are k VLANs with
       n hosts in each, all connected to the single switch. There
       are also n hosts that are not in any VLAN, also connected to
       the switch."""

    def build( self, k=2, n=2, vlanBase=2 ):
        '''s1 = self.addSwitch( 's1' )
        for i in range( k ):
            vlan = vlanBase + i
            for j in range(n):
                name = 'h%d-%d' % ( j+1, vlan )
                h = self.addHost( name, cls=VLANHost, vlan=vlan )
                self.addLink( h, s1 )
        for j in range( n ):
            h = self.addHost( 'h%d' % (j+1) )
            self.addLink( h, s1 )'''
        s1 = self.addSwitch('s1', dpid='1c488cea1ba8a7c1', mac='8c:ea:1b:a8:a7:c1', ip='172.19.0.30/16',protocols='OpenFlow13')
        s2 = self.addSwitch('s2', dpid='1c488cea1b765e01', mac='8c:ea:1b:76:5e:01', ip='172.19.0.40/16',protocols='OpenFlow13')
        h16 = self.addHost('h16', cls=VLANHost, vlan=2, mac='fe:a7:c1:06:00:00', ip='172.19.128.3',defaultRoute='via 172.19.128.1')
        h17 = self.addHost('h17', cls=VLANHost, vlan=2, mac='fe:a7:c1:07:00:00', ip='172.19.128.4',defaultRoute='via 172.19.128.1')
        h26 = self.addHost('h26', cls=VLANHost, vlan=2, mac='fe:5e:01:06:00:00', ip='172.19.128.19',defaultRoute='via 172.19.128.1')
        h27 = self.addHost('h27', cls=VLANHost, vlan=2, mac='fe:5e:01:07:00:00', ip='172.19.128.20',defaultRoute='via 172.19.128.1')


        self.addLink(s1, s2, port1=3, port2=1)
        self.addLink(s1, h16, port1=6)
        self.addLink(s1, h17, port1=7)
        self.addLink(s2, h26, port1=6)
        self.addLink(s2, h27, port1=7)

        





def exampleCustomTags():
    """Simple example that exercises VLANStarTopo"""

    net = Mininet( topo=VLANStarTopo() )
    net.start()
    CLI( net )
    net.stop()

if __name__ == '__main__':
       

    setLogLevel( 'info' )

    if not quietRun( 'which vconfig' ):
        error( "Cannot find command 'vconfig'\nThe package",
               "'vlan' is required in Ubuntu or Debian,",
               "or 'vconfig' in Fedora\n" )
        exit()

    #if len( sys.argv ) >= 2:
    exampleAllHosts()
    #else:
    #    exampleCustomTags()
