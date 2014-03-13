#!/usr/bin/env python
#coding=utf-8
import argparse
import redis
from scpfile import scp
import pexpect
import time

class flyer():
    id = 0
    channels = {}
    redisIp = ""
    redisPort = 0
    redisPassword = ""
    totalProcessNum = 0
    def __init__(self, redisIp="127.0.0.1", redisPort=6379, redisPassword="", redisDb=10, totalProcessNum = 2 ):
        """get redis instance and check if it can be used"""
        self.redisIp = redisIp
        self.redisPort = redisPort
        self.redisPassword = redisPassword
        self.redisDb = redisDb
        self.totalProcessNum = totalProcessNum
        r = self.getRedis()
        if r.ping():
            ps = r.pubsub()
            ps.subscribe("rootChannel")  #订阅两个频道，分别是count_alarm ip_alarm
            self.channels["rootChannel"] = ps
            print "init ok"

    def getRedis(self):
        pool = redis.ConnectionPool(host=self.redisIp, port=self.redisPort, password=self.redisPassword, db=self.redisDb)
        return redis.Redis(connection_pool=pool)

    def getPubsub(self):
        r = self.getRedis()
        return r.pubsub()

    def start(self):
        """get the process id in the cluster"""
        r = self.getRedis()
        while 1:
            if r.setnx("flyerLock", 1):
                self.id = r.incr("flyerId")
                print self.id,"get lock"
                if self.id != 1:
                    r.delete("flyerLock")
                    print "id",self.id,"watiing"
                    print self.id,"release lock"
                    self.recieveAll()
                    print "id",self.id,"starting"
                elif self.id == 1:
                    self.clean()
                    print "id:",self.id
                    r.delete("flyerLock")
                    print self.id, "release lock"
                    retryNum = 10
                    count = 0
                    while 1:
                        if r.get("registedNum") == self.totalProcessNum:
                            self.sendAll("start")
                            break
                        else:
                            time.sleep(1)
                        count += 1
                        if count>= retryNum:
                            print "start time out"
                            break
            else:
                time.sleep(0.2)
        return self.id

    def stop(self):
        """send to all process to exit"""
        r = self.getRedis()
        r.set("flyerStop", 1)
        exit(0)

    def send(self, channelName, message):
        """send message to chanel (if you want sent to specific process you can use
        difference chanel name in different process)"""
        r = self.getRedis()
        return r.publish(channelName, message)

    def recieve(self, channelName):
        """recieve num messages from chanel"""
        ps = self.getPubsub()
        ps.subscribe(channelName)
        for item in ps.listen():
            if item['type'] == 'message':
                    return item["data"]

    def sendAll(self, message):
        """send message to each process"""
        r = self.getRedis()
        r.publish("rootChannel", message)

    def recieveAll(self):
        """recieve message from all"""
        ps = self.channels["rootChannel"]
        for item in ps.listen():
            if item['type'] == 'message':
                    return item["data"]
    def clean(self):
        r = self.getRedis()
        r.set("flyerStop", 0)
        r.set("flyerId", 0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Flyer--An easy MPI-like distributed\
            tool for python, to ran applications in clusters.')
    parser.add_argument('--h', action="store", default="host.list", dest="hostList")
    parser.add_argument('--e', action="store", dest="exeFile")
    parser.add_argument('--r', action="store", default="/tmp", dest="rpath")
    results = parser.parse_args()
    exeInfo = scp(results.hostList, results.rpath, results.exeFile)
    if not exeInfo:
        print "error: no file", results.exeFile
        exit()

    flyerTest = flyer()
    flyerTest.clean()



