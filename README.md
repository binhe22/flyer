#Flyer
###What is flyer?
It is a tool for python to ditributed in a cluster.

###How does it work?
It depends on gevent,pexpect and redis. It use redis to exchange information. Mostly, it is like a small mpi library for python.  

###How to use?

Make sure that each node in the cluster trust each other in ssh. The edit the host.list to add the host. Each line in host.list means that it will start a proccess in the host. Edit file.list to add files to use by the program, flyer will help you to copy the files. 

You can run :

```
./flyer.py -e run.py -f file.list -h host.list
```
The flyer include the class the run.py has to inherit, and it also serve as the runtime environment. The run.py inherit the class and generate an instance, it can use the methods of the instance to get the proccess id, send or recieve message.

###Waht to do?
* It is just a demo, far away with stabilization, I go on working on it.
* Error handling is not good, I will fix it
* Use a redis cluster
* Write some examples
* Add other functions if necessary
