from nest.topology import *
from nest.experiment import *


#Simulate an Ethernet LAN using N-nodes(6-10), change error rate and data rate
#and compare the throughput


######################################################################
#                          Network Topology                          #
#                                                                    #
#  h1        h2        h3                  h4          h5        h6  #
#  |         |         |                    |          |          |  #
#  ----------------------------- s1 -------------------------------  #
#                    <------ 100mbit, 1ms ------>                    #
#                                                                    #
######################################################################

# Create six hosts `h1` to `h4`, and one switch `s1`
h1 = Node("h1")
h2 = Node("h2")
h3 = Node("h3")
h4 = Node("h4")
h5 = Node("h5")
h6 = Node("h6")
s1 = Switch("s1")

# Connect all the four hosts to the switch
# `eth1` to `eth4` are the interfaces at `h1` to `h4`, respectively.
# `ets1a` is the first interface at `s1` which connects it with `h1`
# `ets1b` is the second interface at `s1` which connects it with `h2`
# `ets1c` is the third interface at `s1` which connects it with `h3`
# `ets1d` is the fourth interface at `s1` which connects it with `h4`
# `ets1e` is the fifth interface at `s1` which connects it with `h5`
# `ets1f` is the sixth interface at `s1` which connects it with `h6`
(eth1, ets1a) = connect(h1, s1)
(eth2, ets1b) = connect(h2, s1)
(eth3, ets1c) = connect(h3, s1)
(eth4, ets1d) = connect(h4, s1)
(eth5, ets1e) = connect(h5, s1)
(eth6, ets1f) = connect(h6, s1)


# Assign IPv4 addresses to all the interfaces.
eth1.set_address("10.0.1.1/24")
eth2.set_address("10.0.1.2/24")
eth3.set_address("10.0.1.3/24")
eth4.set_address("10.0.1.4/24")
eth5.set_address("10.0.1.5/24")
eth6.set_address("10.0.1.6/24")


h1.add_route("DEFAULT", eth1)  # Adding a default route to node h1 via eth1
h2.add_route("DEFAULT", eth2)  # Adding a default route to node h2 via eth2
h3.add_route("DEFAULT", eth3)  # Adding a default route to node h3 via eth3
h4.add_route("DEFAULT", eth4)  # Adding a default route to node h4 via eth4
h5.add_route("DEFAULT", eth5)  # Adding a default route to node h5 via etr5
h6.add_route("DEFAULT", eth6)  # Adding a default route to node h6 via eth6

# configuring the queue size.
# applying Packet Limited queue in this scenario.
qdisc = "pfifo"
pfifo_parameter = {"limit": "20"}  # set the queue capacity to 20 packets


# Set the link attributes
eth1.set_attributes("100mbit", "1ms")
eth2.set_attributes("100mbit", "1ms")
eth3.set_attributes("100mbit", "1ms")
ets1a.set_attributes("100mbit", "1ms")
ets1b.set_attributes("100mbit", "1ms")
ets1c.set_attributes("100mbit", "1ms")

# Setting bandwidth, delay, queuing discipline, and applying the queue discipline previously configured .
# Setting bandwidth and delay for ets1d, ets1e, ets1f
eth4.set_attributes("100mbit", "1ms", qdisc, **pfifo_parameter)
eth5.set_attributes("100mbit", "1ms", qdisc, **pfifo_parameter)
eth6.set_attributes("100mbit", "1ms", qdisc, **pfifo_parameter)
ets1d.set_attributes("100mbit", "1ms", qdisc, **pfifo_parameter)
ets1e.set_attributes("100mbit", "1ms", qdisc, **pfifo_parameter)
ets1f.set_attributes("100mbit", "1ms", qdisc, **pfifo_parameter)


# Creating a new experiment named "lan"
exp = Experiment("lan")

# Creating a TCP flow from node h1 to node h4 for 10 seconds
flow1 = Flow(h1, h4, eth4.get_address(), 0, 10, 1)
exp.add_tcp_flow(flow1)  # Adding the TCP flow to the experiment

# Creating a UDP flow from node h2 to node h5 for 10 seconds
flow2 = Flow(h2, h5, eth5.get_address(), 0, 10, 1)
exp.add_udp_flow(flow2)  # Adding the UDP flow to the experiment

# Specifying that we want to collect queuing discipline statistics for eth2
exp.require_qdisc_stats(eth2)

exp.run()  # Running the experiment
