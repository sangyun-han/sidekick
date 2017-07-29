import sys
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.topolib import TreeTopo
from mininet.node import RemoteController, OVSKernelSwitch

myTree = TreeTopo(depth=3,fanout=4)

def run( controllers ):
    net = Mininet( topo=myTree, controller=None, autoSetMacs=True )
    ctrl_count = 0
    for controllerIP in controllers:
        net.addController( 'c%d' % ctrl_count, RemoteController, ip=controllerIP )
        ctrl_count += 1
    net.start()
    CLI( net )
    net.topo()


if __name__ == '__main__':
    setLogLevel( 'info' )
    if len(sys.argv ) > 1:
        controllers = sys.argv[ 1: ]
    else:
        print 'Usage: sudo python tree.py '
        exit(1)
    run(controllers)
