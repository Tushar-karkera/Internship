from nest.topology import *
from nest.experiment import *

# Simulate a three nodes point-to-point network with duplex links between them. Set the queue
# size vary the bandwidth and find the number of packets dropped.

####################################################
#                          Network Topology        #
#                                                  #
#                                                  #
#                                                  #
#  N1------------------n2---------------------- N3 #
#         <------ 5mbit, 2ms ------>               #
#                                                  #
####################################################

# Created 3 Nodes
n1 = Node("n1")
n3 = Node("n3")
n2 = Switch("n2")

# Connect the nodes to switch n2
(etn1, etn2a) = connect(n1, n2)
(etn3, etn2b) = connect(n3, n2)

# Assigning IP Address to the Nodes
etn1.set_address("10.0.0.1/24")
etn3.set_address("10.0.0.2/24")

# configuring the queue size
qdisc = "choke"
choke_parameters = {
    "limit": "100",  # set the queue capacity to 100 packets
    "min": "5",  # set the minimum threshold to 5 packets
    "max": "15",  # set the maximum threshold to 15 packets
}

# Setting the bandwidth and the delay between the nodes
# also setting the queue size previously configured
etn1.set_attributes("5mbit", "2ms", qdisc, **choke_parameters)
etn3.set_attributes("5mbit", "2ms", qdisc, **choke_parameters)

etn2a.set_attributes("5mbit", "2ms", qdisc, **choke_parameters)
etn2b.set_attributes("5mbit", "2ms", qdisc, **choke_parameters)

# Creating an new experiment
exp = Experiment("three-node-point-to-point")

# creating a new Flow from `n1` to `n3` for 20 seconds.
flow1 = Flow(n1, n3, etn3.get_address(), 0, 20, 1)

# Use `flow1` as a UDP flow with target bandwidth of 5mbit.
exp.add_udp_flow(flow1, target_bandwidth="5mbit")

# Run the experiment
exp.run()
