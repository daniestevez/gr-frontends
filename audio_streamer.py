#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Audio source streamer
# Author: Daniel Estevez
# Description: Streams an audio source
# Generated: Thu Jan  5 15:13:23 2017
##################################################

from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser


class audio_streamer(gr.top_block):

    def __init__(self, port=7355, destination='localhost', device=''):
        gr.top_block.__init__(self, "Audio source streamer")

        ##################################################
        # Parameters
        ##################################################
        self.port = port
        self.destination = destination
        self.device = device

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

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port

    def get_destination(self):
        return self.destination

    def set_destination(self, destination):
        self.destination = destination

    def get_device(self):
        return self.device

    def set_device(self, device):
        self.device = device


def argument_parser():
    description = 'Streams an audio source'
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option, description=description)
    parser.add_option(
        "", "--port", dest="port", type="intx", default=7355,
        help="Set port [default=%default]")
    parser.add_option(
        "", "--destination", dest="destination", type="string", default='localhost',
        help="Set localhost [default=%default]")
    parser.add_option(
        "", "--device", dest="device", type="string", default='',
        help="Set device [default=%default]")
    return parser


def main(top_block_cls=audio_streamer, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(port=options.port, destination=options.destination, device=options.device)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
