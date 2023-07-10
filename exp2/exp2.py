from nest.topology import *
from nest.experiment import *
# Simulate a four node point-to-point network, and connect the links as follows: n0-n2, n1-n2
# and n2-n3. Apply TCP agent between n0-n3 and UDP n1-n3. Apply relevant applications
# over TCP and UDP agents changing the parameter and determine the number of packets by
# TCP/UDP.
########################################
#            Network Topology          #
#                                      #
#  N0               N1                 #
#  |                |                  #
#  ---------------- N2 ------------ N3 #
#      <------ 10mbit, 1ms ------>     #
#                                      #
########################################

# Create three hosts `n0` to `n3`, and one Router `r1` representing the node `n2`.
n0 = Node("n0")
n1 = Node("n1")
n3 = Node("n3")
r1 = Router("n2")

# Connect all the three hosts to the Router.
(etn0, etr1a) = connect(n0, r1)
(etn1, etr1b) = connect(n1, r1)
(etn3, etr1c) = connect(n3, r1)

# Assign IPv4 addresses to all the interfaces.
# We assume that the IPv4 address of this network is `10.0.1.0/24`.
etn0.set_address("10.0.1.1/24")
etn1.set_address("10.0.1.2/24")
etn3.set_address("10.0.1.3/24")

# Set the link bandwidth as 10mbit with a delay of 1ms
etn0.set_attributes("10mbit", "1ms")
etn1.set_attributes("10mbit", "1ms")
etn3.set_attributes("10mbit", "1ms")

# Configuring the queue size.
# Applying Packet Limited queue in this scenario.
qdisc = "pfifo"
pfifo_parameters = {
    "limit": "20",  # set the queue capacity to 20 packets
}

# Applying the queue discipline previously configured on the etr1ba and etr1b interfaces.
etr1a.set_attributes("10mbit", "1ms", qdisc, **pfifo_parameters)
etr1b.set_attributes("10mbit", "1ms", qdisc, **pfifo_parameters)


# Created an experiment for two flows of tcp and udp each.
exp = Experiment("4-node-tcp")

# Flow1 is of tcp between `n0` and `n3` for a time duration of 10 seconds.
flow1 = Flow(n0, n3, etn3.get_address(), 0, 10, 1)

# Use `flow1` as a TCP flow.
exp.add_tcp_flow(flow1)

# Flow2 is of udp between `n1` and `n3` for a time duration 10 seconds.
flow2 = Flow(n1, n3, etn3.get_address(), 0, 10, 1)

# would send UDP packets.
exp.add_udp_flow(flow2, target_bandwidth="10mbit")

# Run the experiment
# simulation is stored in the folder `/4-node-tcp(08-07-2023-09:25:52)_dump`
exp.run()
