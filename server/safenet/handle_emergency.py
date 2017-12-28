# from Hologram.HologramCloud import HologramCloud
import logging as logger

emergencySmsDest = 991
hologram_started = False
# try:
#     hologram = HologramCloud(dict(), network='cellular')
#     hologram_started = True
# except Exception, errtxt:
#     logger.error("There was an exception while trying to start Hologram: ", errtxt)


def raise_alarm(location, numOfPeople):
    logger.info("Emergency signal for location %s",location)

    msg = ("There was an alarm for location %s. There are %s of people in this location" % (location, numOfPeople))
    logger.info(msg)

    # if hologram_started :
    #     try:
    #         logger.info("About to send message %s", msg)
    #         resp = hologram.sendMessage(str(msg), topics=["ALARM"], timeout=10)
    #     except Exception, errtxt:
    #         logger.error("There was an exception while trying to send Alarm message and will attempt with SMS: ", errtxt)
    #         hologram.sendSMS(emergencySmsDest, msg)
    # else :
    #     logger.info("Hologram has not been started yet")