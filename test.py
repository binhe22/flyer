import pexpect

def test():
    child=pexpect.spawn('ssh %s "%s"' %("root@115.156.219.157", "nohup ls&"))
    a = child.expect("\].*(\d)")
    print a
    child.close()

test()
