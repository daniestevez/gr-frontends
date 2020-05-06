#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: WAV 44.1KHz file streamer
# Author: Daniel Estevez
# Description: Streams a WAV 44.1kHz file
# GNU Radio version: 3.8.1.0

from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation


class wav_44kHz(gr.top_block):

    def __init__(self, destination='localhost', input_file='', port=7355):
        gr.top_block.__init__(self, "WAV 44.1KHz file streamer ")

        ##################################################
        # Parameters
        ##################################################
        self.destination = destination
        self.input_file = input_file
        self.port = port

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=160,
                decimation=147,
                taps=None,
                fractional_bw=None)
        self.blocks_wavfile_source_0 = blocks.wavfile_source(input_file, False)
        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_short*1, destination, port, 1472, True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_short*1, 48000,True)
        self.blocks_float_to_short_0 = blocks.float_to_short(1, 32767)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_float_to_short_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_udp_sink_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_float_to_short_0, 0))


    def get_destination(self):
        return self.destination

    def set_destination(self, destination):
        self.destination = destination

    def get_input_file(self):
        return self.input_file

    def set_input_file(self, input_file):
        self.input_file = input_file

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port




def argument_parser():
    description = 'Streams a WAV 44.1kHz file'
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "--destination", dest="destination", type=str, default='localhost',
        help="Set localhost [default=%(default)r]")
    parser.add_argument(
        "-f", "--input-file", dest="input_file", type=str, default='',
        help="Set file [default=%(default)r]")
    parser.add_argument(
        "--port", dest="port", type=intx, default=7355,
        help="Set port [default=%(default)r]")
    return parser


def main(top_block_cls=wav_44kHz, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(destination=options.destination, input_file=options.input_file, port=options.port)

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
