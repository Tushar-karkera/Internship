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

# Set the link attributes
eth1.set_attributes("100mbit", "1ms")
eth2.set_attributes("100mbit", "1ms")
eth3.set_attributes("100mbit", "1ms")
eth4.set_attributes("100mbit", "1ms")
eth5.set_attributes("100mbit", "1ms")
eth6.set_attributes("100mbit", "1ms")

# `Ping` from `h1` to `h3`, and `h4` to `h5`.
h1.ping(eth3.address)
h4.ping(eth5.address)
