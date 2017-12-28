import time, threading
import logging as logger

# Dictionary to keep [MacAddress, chipId]
macAddrTupleDict = dict()

# Dictionary to keep [chipId, location]
nodeTuplesDict = dict()


def start_work(interval=2000):
    logger.debug("About to check for expired Mac Addresses to remove. Interval  %s, time: %s", interval, time.asctime())
    for macAddr in sorted(macAddrTupleDict):
        logger.debug('MacAddr to check: %s ' , macAddr)
        logger.debug('MacAddrTupple to check: %s' , str(macAddrTupleDict[macAddr]))

        registeredTime = time.strptime(macAddrTupleDict[macAddr][1])
        now = time.localtime()
        logger.debug('Elapsed time for the macaddr: %s' , str(time.mktime(now) - time.mktime(registeredTime)))
        if time.mktime(now) - time.mktime(registeredTime) >= interval:
            logger.debug('!!!!! Will remove %s mac addr, time %s' , macAddr, time.asctime())
            # print("\t\tNow {}, registeredTime {}".format(now, registeredTime))
            macAddrTupleDict.pop(macAddr)
            # macAddrSet.remove(macAddr)
            logger.debug('!!!!! Updated Tuple %s', str(macAddrTupleDict))
        else:
            logger.debug('Too soon to remove %s mac address, time %s' , macAddr, time.asctime())


    logger.info("!!!!! Finally %s Mac Addresses, MacAddrTupple: %s", macAddrTupleDict.__len__(), str(macAddrTupleDict))
    t = threading.Timer(interval, start_work, kwargs={'interval': interval})

    if not t.is_alive():
        t.daemon = True
        t.start()
        return t


def stop_work(t):
    logger.debug("Will STOP thread to check about rotten MacAddr to remove, time: "+time.asctime())
    if t.is_alive():
        logger.debug('thread %s is alive', str(t.ident))
        t.cancel()


def handle_mac(macAddr, chipId, location):

    if chipId not in nodeTuplesDict:
        nodeTuplesDict[chipId] = (location)
        logger.info("Added new Node with chipId %s for Location %s", chipId, location)

    if macAddr not in macAddrTupleDict:
        # macAddrSet.add(macAddr)
        macAddrTupleDict[macAddr] = (chipId, time.asctime())
        logger.info("Got new MacAddr %s", macAddr)
    else:
        logger.warning('MacAddr %s is already known, will just update, number of Mac Addresses %s',macAddr, macAddrTupleDict.__len__())
        macAddrTupleDict[macAddr] = (chipId, time.asctime())

def get_macs_for_location(location):
    try:
        chipid = nodeTuplesDict.keys()[nodeTuplesDict.values().index(location)]
        macs = 0
        for k, v in macAddrTupleDict.iteritems():
            if (chipid == v[0]):
                macs = macs +1

        logger.info("There are %s people at location %s", macs, location)
        return macs
    except Exception, errtxt:
        logger.error("Location %s is not known, error: %s", location, errtxt)
        return 0


def print_tupple():
    print('ChipID \t Time')
    for (chipId, time) in macAddrTupleDict.values():
        print('%s \t %s' % (chipId, time))

if __name__ == '__main__':
    logger.info('Main Line Starting')
    t = start_work()
