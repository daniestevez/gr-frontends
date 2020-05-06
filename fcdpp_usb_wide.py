#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Wide SSB receiver for a FUNcube Dongle Pro+ device
# Author: Daniel Estevez
# Description: Receives with a FUNcube Dongle Pro+ and streams the wide USB audio (24kHz filter)
# GNU Radio version: 3.8.1.0

from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import fcdproplus
import gpredict


class fcdpp_usb_wide(gr.top_block):

    def __init__(self, bb_gain=20, destination='localhost', freq=145e6, freq_corr=0, gpredict_port=4532, if_gain=20, offset=40e3, port=7355, rf_gain=40):
        gr.top_block.__init__(self, "Wide SSB receiver for a FUNcube Dongle Pro+ device")

        ##################################################
        # Parameters
        ##################################################
        self.bb_gain = bb_gain
        self.destination = destination
        self.freq = freq
        self.freq_corr = freq_corr
        self.gpredict_port = gpredict_port
        self.if_gain = if_gain
        self.offset = offset
        self.port = port
        self.rf_gain = rf_gain

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 192e3
        self.doppler_freq = doppler_freq = freq

        ##################################################
        # Blocks
        ##################################################
        self.gpredict_doppler_0 = gpredict.doppler('localhost', gpredict_port, False)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(4, firdes.low_pass(1, samp_rate, 12000, 500), doppler_freq-freq+offset, samp_rate)
        self.fcdproplus_fcdproplus_0 = fcdproplus.fcdproplus('',1)
        self.fcdproplus_fcdproplus_0.set_lna(0)
        self.fcdproplus_fcdproplus_0.set_mixer_gain(0)
        self.fcdproplus_fcdproplus_0.set_if_gain(0)
        self.fcdproplus_fcdproplus_0.set_freq_corr(0)
        self.fcdproplus_fcdproplus_0.set_freq(freq-offset)
        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_short*1, destination, port, 1472, True)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_float_to_short_0 = blocks.float_to_short(1, 32767)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.analog_sig_source_x_0 = analog.sig_source_c(48000, analog.GR_COS_WAVE, 12000, 1, 0, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_float_to_short_0, 0))
        self.connect((self.blocks_float_to_short_0, 0), (self.blocks_udp_sink_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.fcdproplus_fcdproplus_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_multiply_xx_0, 1))


    def get_bb_gain(self):
        return self.bb_gain

    def set_bb_gain(self, bb_gain):
        self.bb_gain = bb_gain

    def get_destination(self):
        return self.destination

    def set_destination(self, destination):
        self.destination = destination

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_doppler_freq(self.freq)
        self.fcdproplus_fcdproplus_0.set_freq(self.freq-self.offset)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.doppler_freq-self.freq+self.offset)

    def get_freq_corr(self):
        return self.freq_corr

    def set_freq_corr(self, freq_corr):
        self.freq_corr = freq_corr

    def get_gpredict_port(self):
        return self.gpredict_port

    def set_gpredict_port(self, gpredict_port):
        self.gpredict_port = gpredict_port

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
        self.fcdproplus_fcdproplus_0.set_freq(self.freq-self.offset)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.doppler_freq-self.freq+self.offset)

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.low_pass(1, self.samp_rate, 12000, 500))

    def get_doppler_freq(self):
        return self.doppler_freq

    def set_doppler_freq(self, doppler_freq):
        self.doppler_freq = doppler_freq
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.doppler_freq-self.freq+self.offset)




def argument_parser():
    description = 'Receives with a FUNcube Dongle Pro+ and streams the wide USB audio (24kHz filter)'
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "--bb-gain", dest="bb_gain", type=eng_float, default="20.0",
        help="Set baseband gain [default=%(default)r]")
    parser.add_argument(
        "--destination", dest="destination", type=str, default='localhost',
        help="Set localhost [default=%(default)r]")
    parser.add_argument(
        "-f", "--freq", dest="freq", type=eng_float, default="145.0M",
        help="Set frequency [default=%(default)r]")
    parser.add_argument(
        "--freq-corr", dest="freq_corr", type=eng_float, default="0.0",
        help="Set frequency correction (ppm) [default=%(default)r]")
    parser.add_argument(
        "--gpredict-port", dest="gpredict_port", type=intx, default=4532,
        help="Set GPredict port [default=%(default)r]")
    parser.add_argument(
        "--if-gain", dest="if_gain", type=eng_float, default="20.0",
        help="Set IF gain [default=%(default)r]")
    parser.add_argument(
        "--offset", dest="offset", type=eng_float, default="40.0k",
        help="Set centre frequency offset [default=%(default)r]")
    parser.add_argument(
        "--port", dest="port", type=intx, default=7355,
        help="Set port [default=%(default)r]")
    parser.add_argument(
        "--rf-gain", dest="rf_gain", type=eng_float, default="40.0",
        help="Set RF gain [default=%(default)r]")
    return parser


def main(top_block_cls=fcdpp_usb_wide, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(bb_gain=options.bb_gain, destination=options.destination, freq=options.freq, freq_corr=options.freq_corr, gpredict_port=options.gpredict_port, if_gain=options.if_gain, offset=options.offset, port=options.port, rf_gain=options.rf_gain)

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
