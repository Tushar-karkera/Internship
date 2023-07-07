from nest.topology import *

####################################################
#                          Network Topology        #
#                                                  #
#  h1               h2                          h3 #
#  |                |                           |  #
#  ----------------------------- s1 -------------  #
#         <------ 5mbit, 2ms ------>               #
#                                                  #
####################################################

# Created 3 Nodes
h1 = Node("h1")
h2 = Node("h2")
h3 = Node("h3")
s1 = Switch("s1")

# Connect the nodes to switch S1
(eth1, ets1a) = connect(h1, s1)
(eth2, ets1b) = connect(h2, s1)
(eth3, ets1c) = connect(h3, s1)

# Assigning IP Address to the Nodes
eth1.set_address("10.0.0.1/24")
eth2.set_address("10.0.0.2/24")
eth3.set_address("10.0.0.3/24")

# Set the bandwidth and the delay between the nodes
eth1.set_attributes("5mbit", "2ms")
eth2.set_attributes("5mbit", "2ms")
eth3.set_attributes("5mbit", "2ms")

# Ping from Node1 to Node3
h1.ping(eth3.address)
