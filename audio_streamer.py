#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Audio source streamer
# Author: Daniel Estevez
# Description: Streams an audio source
# GNU Radio version: 3.8.1.0

from gnuradio import audio
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation


class audio_streamer(gr.top_block):

    def __init__(self, destination='localhost', device='', port=7355):
        gr.top_block.__init__(self, "Audio source streamer")

        ##################################################
        # Parameters
        ##################################################
        self.destination = destination
        self.device = device
        self.port = port

        ##################################################
        # Blocks
        ##################################################
        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_short*1, destination, port, 1472, True)
        self.blocks_float_to_short_0 = blocks.float_to_short(1, 32767)
        self.audio_source_0 = audio.source(48000, device, True)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.audio_source_0, 0), (self.blocks_float_to_short_0, 0))
        self.connect((self.blocks_float_to_short_0, 0), (self.blocks_udp_sink_0, 0))


    def get_destination(self):
        return self.destination

    def set_destination(self, destination):
        self.destination = destination

    def get_device(self):
        return self.device

    def set_device(self, device):
        self.device = device

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port




def argument_parser():
    description = 'Streams an audio source'
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "--destination", dest="destination", type=str, default='localhost',
        help="Set localhost [default=%(default)r]")
    parser.add_argument(
        "--device", dest="device", type=str, default='',
        help="Set device [default=%(default)r]")
    parser.add_argument(
        "--port", dest="port", type=intx, default=7355,
        help="Set port [default=%(default)r]")
    return parser


def main(top_block_cls=audio_streamer, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(destination=options.destination, device=options.device, port=options.port)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
