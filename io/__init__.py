#!/usr/bin/env python3
#
###############################################################################
"""
==========================
IO READING for Rasperry Pi
==========================

.. codeauthor:: Alexander Schwithal

Requirements
============

This plugin has no requirements or dependencies.

Configuration
=============

plugin.conf
-----------
::

[io]
class_name = IO
class_path = plugins.io

items.conf
----------
::

[test]
[[io]]
type = bool
input_pin = 24
io_edge = rising


Methods
=======

.. autoclass:: IO()
:members:

"""

import sys
import logging
import RPi.GPIO as GPIO

logger = logging.getLogger('')


class IO():
    def __init__(self,smarthome, pin=24, edge=1):
        self.pin = pin
        self.edge = int(edge)
        self._ports = dict()
        logger.info('IO: Configured for port {0} and edge {1}'.format(self.pin, self.edge))
        self.run
        self._sh = smarthome

    
    # ISR
    def Interrupt_raise(self, channel):
        logger.debug("IO: update received")
        try:
            # assign values to items
            for key in list(self._ports.keys()):
                if int(key) == self.pin:
                    logger.debug('IO: Key {0} found'.format(int(key)))
                    self._ports[key](True, caller='io_detect')
                    logger.debug('IO: Port {0} updated via ISR'.fomrat(int(key)))
                else:
                    logger.debug('IO: Key for {0} not found'.format(int(key)))
        except IndexError as e:
            logger.error("IO: Error assigning item: %s",str(e))


    def run(self):
       GPIO.setmode(GPIO.BCM)
       # Active specific pin as input:
       #GPIO.setup(self.pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
       GPIO.setup(self.pin, GPIO.IN)
       self.alive = True
       # Add interrupt event for specific pin:
       if self.edge == 1:
           GPIO.add_event_detect(self.pin, GPIO.RISING, callback = self.Interrupt_raise, bouncetime = 600)
           logger.debug('IO: Interrupt configured for rising edge')
       else:
           GPIO.add_event_detect(self.pin, GPIO.FALLING, callback = self.Interrupt_raise, bouncetime = 600)
           logger.debug('IO: Interrupt configured for falling edge')


    def stop(self):
        self.alive = False
        logger.debug('IO: Module stopped')

    def parse_item(self, item):
        if 'input_pin' in item.conf:
            self._ports[item.conf['input_pin']] = item
            logger.debug("IO: Parse item: {0}".format(item))
            return self.update_item
        else:
            return None
   

    def parse_logic(self, logic):
        return None

    def update_item(self, item, caller=None, source=None, dest=None):
        logger.debug("IO: update function started")
        if caller != 'io_detect':
            if 'input_pin' in item.conf:
                self.set_port(item.conf['netio_port'], item())
                logger.debug('IO: Port updated externally')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    myplugin = Plugin('io_plugin')
    myplugin.run()         
