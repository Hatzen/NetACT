# NetACT

NetACT is a Programm which should make it easier to test network applications interacting with each other with different roles.

Currently stalled developement

# Use case

i started to develope this program for making automated tests for EasyPeasyVPN. 
You create different configurations for NetACT on different devices. The main server is started from the current developing device it will 
send the current version of the programm to all given devices and start them. As the main program may need some time for setup it can
send commands to other instances of NetACT which can interact with standard I/O and so start specific program parts.
After the program finished the output and error stream will be redirected to the developing machine and the developer can analysed whether 
everything worked as expected.
