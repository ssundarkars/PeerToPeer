# PeerToPeer

This Application ‘peertopeer’ deals with a TCP connection made between parties/machines. We are using socket programming concepts to establish connections between machines. In order to ease the use of application it also has a GUI support implemented with the help of python.Tkinter(Tk).

In order to get started with the connection, user must ensure that, all the required files(peertopeer.py, p2p.png(logo), connectionHelpModule) are placed in the same folder or equivalent (file-path) changes are made in the peertopeer.py(main) file.  

After you execute peertopeer.py python file successfully you must see a GUI, provide the IPV4 address of the peer’s machine with a port number separated by ‘/’. Go to the help section for more info. 
Click the ‘Connect’ Button to establish connection. Now your machine is searching for machine with given address, wait for time-out if target machine is not active, as soon time-out is reached, your machine will act as a server and you can send message or files to the target machine, these messages and file will be received as soon the target machine is active on the same port.

For easier Connection follow:-

Step1:-Make machine1 as server by passing machine1 its own IPV4 address and any port from 1000-65535

Step2:-Make machine2 as client  by passing it machine1's IPv4 address and same port as given in machine1

Congrats connection successful.

Note:- All the coding has been done on the Linux platform, there might be some platform dependencies, if being used in other platforms, you need to handle them seperately. Please try to resolve them, and feel free to contact me for help/suggestions.
