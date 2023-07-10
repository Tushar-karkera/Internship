from nest.topology import *
from nest.experiment import *

# Simulate a three nodes point-to-point network with duplex links between them. Set the queue
# size vary the bandwidth and find the number of packets dropped.

####################################################
#               Network Topology                   #
#                                                  #
#                                                  #
#                                                  #
#  h1------------------r1---------------------- h2 #
#         <------ 5mbit, 2ms ------>               #
#                                                  #
####################################################

# Created 2 Nodes and a router.
h1 = Node("h1")
h2 = Node("h2")
r1 = Router("r1")

# Connect the nodes to router r1.
(eth1, etr1a) = connect(h1, r1)
(eth2, etr1b) = connect(h2, r1)

# Assigning IP Address to the node and router interfaces.
eth1.set_address("10.0.0.1/24")
etr1a.set_address("10.0.0.2/24")

etr1b.set_address("10.0.1.2/24")
eth2.set_address("10.0.1.2/24")

# Add a default route for the router as its gateway.
h1.add_route("DEFAULT", eth1)
h2.add_route("DEFAULT", eth2)

# configuring the queue size.
# applying Packet Limited queue in this scenario.
qdisc = "pfifo"
pfifo_parameters = {
    "limit": "20",  # set the queue capacity to 20 packets
}

# Setting the bandwidth and the delay between the nodes as 5mbit
# and 2ms respectively.
# also applying the queue discipline previously configured on the etr1b interface.
eth1.set_attributes("5mbit", "2ms")
eth2.set_attributes("5mbit", "2ms")

etr1a.set_attributes("5mbit", "2ms")
etr1b.set_attributes("5mbit", "2ms", qdisc, **pfifo_parameters)

# Creating an new experiment
exp = Experiment("three-node-point-to-point")

# creating a new Flow from `h1` to `h2` for 10 seconds.
flow1 = Flow(h1, h2, eth2.get_address(), 0, 10, 1)

# Use `flow1` as a UDP flow with target bandwidth of 50mbit.
# Using higher bandwidth on the UDP flow to bottleneck the network and lead to packet drops.
exp.add_udp_flow(flow1, target_bandwidth="50mbit")

# Enable statistics on the etr1b interface of the router.
# Temporarily disabled queue statistics due to unresolved errors.
# exp.require_qdisc_stats(etr1b)

# Run the experiment
exp.run()
