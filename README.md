For troubleshooting Current control plane on ASA/FTD, it would be useful to see a graph of CP CPU. However since FMC does not show this graph as of writting of this article, we can use EEM to gather this data and plot the graph.

 
For the Input we used the following EEM script to gather CP CPU usage and show clock after 5 seconds intervals and write to file disk0:/CP_CPU.

 

event manager applet cpucheck
event timer watchdog time 5
action 1 cli command "sh cpu detailed"
action 2 cli command "show clock"
output file append disk0:/CP_CPU

 

Then the attached script was used to get a time value plot of the 5 seconds CP CPU usage. 

 

It outpts a graph and average of CP CPU usage.

 

RAJATSH-M-V7QW:LIST_PYTHON rajatsh$ python3 CP_CPU.py

Enter the file path: CP_CPU.txt

Average of control plane values: 57.3
