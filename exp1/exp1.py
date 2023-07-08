from nest.topology import *

# Simulate a three nodes point-to-point network with duplex links between them. Set the queue
# size vary the bandwidth and find the number of packets dropped.

####################################################
#                          Network Topology        #
#                                                  #
#                                                  #
#                                                  #
#  N0------------------n2---------------------- N3 #
#         <------ 5mbit, 2ms ------>               #
#                                                  #
####################################################

# Created 3 Nodes
n0 = Node("n0")
n3 = Node("n3")
n2 = Switch("n2")

# Connect the nodes to switch n2
(etn0, etn2a) = connect(n0, n2)
(etn3, etn2b) = connect(n3, n2)

# Assigning IP Address to the Nodes
etn0.set_address("10.0.0.1/24")
etn3.set_address("10.0.0.2/24")

# Set the bandwidth and the delay between the nodes
etn0.set_attributes("5mbit", "2ms")
etn3.set_attributes("5mbit", "2ms")

# Ping from Node1 to Node3
n0.ping(etn3.address)
