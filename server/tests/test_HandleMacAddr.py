import unittest, time
import logging
from logging.config import fileConfig
import handle_mac_addr

fileConfig('../safenet/logging_config.ini')
logger = logging.getLogger()

class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        logger.info('About to start thread to check mac addresses')
        handle_mac_addr.start_work(15).join()
        # thread.start()
        # thread.join()

        logger.info('About to add new Mac Addr')
        logger.info('1. About to insert MAC, time: %s' ,time.asctime())
        self.assertIsNone(
            handle_mac_addr.handle_mac("aa:bb:cc:dd:ee:ff:gg", "chipId1234", "192.168.1.111"))
        logger.info('2. About to check, time: %s' , time.asctime())
        self.assertEqual(1, len(handle_mac_addr.macAddrTupleDict), "Dict should have 1 mac addr")

        time.sleep(5)
        logger.info('3. About to check, time: %s', time.asctime())
        self.assertEqual(1, len(handle_mac_addr.macAddrTupleDict), "Dict should have 1 mac addr")

        time.sleep(15)
        logger.info('4. About to check, time: %s' , time.asctime())
        self.assertEqual(0, len(handle_mac_addr.macAddrTupleDict), "Dict should have 0 mac addr")

        self.assertIsNone(
            safenet.handle_mac_addr.handle_mac("aa:bb:cc:dd:ee:ff:gg", "chipId1234", "192.168.1.112"))

        time.sleep(20)
        logger.info('5. About to check, time: %s' ,time.asctime())
        self.assertEqual(1, len(handle_mac_addr.macAddrTupleDict), "Dict should have 1 mac addr")

        time.sleep(20)
        logger.info('5. About to check, time: %s' ,time.asctime())
        self.assertEqual(0, len(handle_mac_addr.macAddrTupleDict), "Dict should have 0 mac addr")

if __name__ == '__main__':
    unittest.main()

