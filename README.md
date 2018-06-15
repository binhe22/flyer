# Flyer
### What is flyer?
It is a tool for python to ditributed in a cluster.

### How does it work?
It depends on gevent,pexpect and redis. It use redis to exchange information. Mostly, it is like a small mpi library for python.  

### How to use?

Make sure that each node in the cluster trust each other in ssh. Then edit the host.list to add the host. Each line in host.list means that it will start a proccess in the host. Edit file.list to add files to use by the program, flyer will help you to copy the files. 

You can run :

```
./flyer.py -e run.py -f file.list -h host.list
```
The flyer include the class the run.py has to inherit, by using redis to pass message and sync infomation.

### Waht to do?
* It is just a demo, far away from stabilization, I will go on working on it.
* Error handling is not good, I will fix it
* Use a redis cluster
* Write some examples
* Add other functions if necessary

### Example
run.py 
