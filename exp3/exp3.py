from nest.topology import *  # Importing necessary modules from nest
from nest.experiment import *

#  Simulate the different types of Internet traffic such as FTP a TELNET over a network and
# analyze the throughput.

##########################################################
#                   Network Topology                     #
#                                                        #
#                                                        #
#   h1 -------------------- r1 -------------------- h2   #
#       <-- 5mbit, 2ms -->      <-- 5mbit, 2ms -->       #
#                                                        #
##########################################################

h1 = Node("h1")  # Creating a node named "h1"
h2 = Node("h2")  # Creating a node named "h2"
r1 = Router("r1")  # Creating a router named "r1"


# Connecting node h1 to router r1 and assigning the interfaces to eth1 and etr1a
eth1, etr1a = connect(h1, r1)
# Connecting node h2 to router r1 and assigning the interfaces to etr1b and eth2
etr1b, eth2 = connect(h2, r1)


eth1.set_address("10.0.0.1/24")  # Setting IP address and subnet mask for eth1
# Setting IP address and subnet mask for etr1a
etr1a.set_address("10.0.0.2/24")

# Setting IP address and subnet mask for etr1b
etr1b.set_address("10.0.1.1/24")
eth2.set_address("10.0.1.2/24")  # Setting IP address and subnet mask for eth2


h1.add_route("DEFAULT", eth1)  # Adding a default route to node h1 via eth1
h2.add_route("DEFAULT", etr1b)  # Adding a default route to node h2 via etr1b

# configuring the queue size.
# applying Packet Limited queue in this scenario.
qdisc = "pfifo"
pfifo_parameter = {"limit": "20"}  # set the queue capacity to 20 packets


eth1.set_attributes("5mbit", "2ms")  # Setting bandwidth and delay for eth1
etr1a.set_attributes("5mbit", "2ms")  # Setting bandwidth and delay for etr1a

# Setting bandwidth, delay, queuing discipline, and applying the queue discipline previously configured .
# Setting bandwidth and delay for etr1b
etr1b.set_attributes("5mbit", "2ms", qdisc, **pfifo_parameter)
eth2.set_attributes("5mbit", "2ms", qdisc, **pfifo_parameter)


# Creating a new experiment named "ftp-and-telnet"
exp = Experiment("ftp-and-telnet")


# Creating a TCP flow from node h1 to node h2 for 10 seconds
flow1 = Flow(h1, h2, etr1b.get_address(), 0, 10, 1)
exp.add_tcp_flow(flow1)  # Adding the TCP flow to the experiment

# Creating a UDP flow from node h2 to node h1 for 10 seconds
flow2 = Flow(h2, h1, eth1.get_address(), 0, 10, 1)

exp.add_udp_flow(flow2)  # Adding the UDP flow to the experiment

# Specifying that we want to collect queuing discipline statistics for eth2
exp.require_qdisc_stats(eth2)

exp.run()  # Running the experiment
