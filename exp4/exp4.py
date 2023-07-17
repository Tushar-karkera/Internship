from nest.topology import *
from nest.experiment import *

# Simulate the transmission of ping messaged over a network topology consisting of 6 nodes
# and find the number of packets dropped due to congestion.

####################################################
#               Network Topology                   #
#                                                  #
#                 h2         h3                    #
#                  \        /                      #
#                   \      /                       #
#                    \    /                        #
#                     \  /                         #
#  h1------------------r1----------------- h4      #
#                     /  \                         #
#                    /    \                        #
#                   /      \                       #
#                  /        \                      #
#                 /          \                     #
#                h6           h5                   #
#                                                  #
#                                                  #
####################################################


# Created 6 Nodes.
h1 = Node("h1")
h2 = Node("h2")
h3 = Node("h3")
h4 = Node("h4")
h5 = Node("h5")
h6 = Node("h6")

# Created 1 router.
r1 = Router("r1")


# Connect the nodes to router r1.
# Set the address to interfaces
# adding the default route to each node
eth1, etr1a = connect(h1, r1)
eth1.set_address("10.0.1.1/24")
etr1a.set_address("10.0.1.2/24")
h1.add_route("DEFAULT", eth1)


eth2, etr1b = connect(h2, r1)
eth2.set_address("10.0.2.1/24")
etr1b.set_address("10.0.2.2/24")
h2.add_route("DEFAULT", eth2)


eth3, etr1c = connect(h3, r1)
eth3.set_address("10.0.3.1/24")
etr1c.set_address("10.0.3.2/24")
h3.add_route("DEFAULT", eth3)


eth4, etr1d = connect(h4, r1)
eth4.set_address("10.0.4.1/24")
etr1d.set_address("10.0.4.2/24")
h4.add_route("DEFAULT", eth4)


eth5, etr1e = connect(h5, r1)
eth5.set_address("10.0.5.1/24")
etr1e.set_address("10.0.5.2/24")
h5.add_route("DEFAULT", eth5)


eth6, etr1f = connect(h6, r1)
eth6.set_address("10.0.6.1/24")
etr1f.set_address("10.0.6.2/24")
h6.add_route("DEFAULT", eth6)


# configuring the queue size.
qdisc = "pfifo"
pfifo_parameters = {

    "limit": "20",  # set the queue capacity to 20 packets

}


# Setting the bandwidth and the delay between the nodes as 5mbit
# and 2ms respectively.
eth1.set_attributes("5mbit", "2ms")
etr1a.set_attributes("5mbit", "2ms")

eth2.set_attributes("5mbit", "2ms")
etr1b.set_attributes("5mbit", "2ms", qdisc, **pfifo_parameters)

eth3.set_attributes("5mbit", "2ms")
etr1c.set_attributes("5mbit", "2ms", qdisc, **pfifo_parameters)

eth4.set_attributes("5mbit", "2ms")
etr1d.set_attributes("5mbit", "2ms", qdisc, **pfifo_parameters)

eth5.set_attributes("5mbit", "2ms")
etr1e.set_attributes("5mbit", "2ms", qdisc, **pfifo_parameters)

eth6.set_attributes("5mbit", "2ms")
etr1f.set_attributes("5mbit", "2ms", qdisc, **pfifo_parameters)


# Creating an new experiment
exp = Experiment("six-nodes-start-topology")

# creating a new Flow from `h1` to `h6` for 10 seconds.
flow1 = Flow(h1, h6, eth6.get_address(), 0, 10, 1)
exp.add_flow(flow1)

# creating a new Flow from `h2` to `h5` for 5 seconds.
flow2 = Flow(h2, h5, eth5.get_address(), 0, 5, 1)
exp.add_flow(flow2)


# Enable statistics on etr1f interfaces
exp.require_qdisc_stats(etr1f)
exp.require_qdisc_stats(etr1e)

# Run the experiment
exp.run()
