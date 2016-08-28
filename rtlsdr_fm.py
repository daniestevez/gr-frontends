#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: FM/FSK receiver for an RTL-SDR device
# Author: Daniel Estevez
# Description: Receives with an RTL-SDR and streams the FM audio
# Generated: Sun Aug 28 13:02:21 2016
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import gpredict
import math
import osmosdr
import time


class rtlsdr_fm(gr.top_block):

    def __init__(self, bb_gain=20, destination="localhost", filter_width=20000, freq=0, freq_corr=0, gpredict_port=4532, if_gain=20, offset=50e3, port=7355, rf_gain=40):
        gr.top_block.__init__(self, "FM/FSK receiver for an RTL-SDR device")

        ##################################################
        # Parameters
        ##################################################
        self.bb_gain = bb_gain
        self.destination = destination
        self.filter_width = filter_width
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
        self.samp_rate = samp_rate = 2.4e6
        self.doppler_freq = doppler_freq = freq

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "rtl" )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(freq-offset, 0)
        self.osmosdr_source_0.set_freq_corr(freq_corr, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(rf_gain, 0)
        self.osmosdr_source_0.set_if_gain(if_gain, 0)
        self.osmosdr_source_0.set_bb_gain(bb_gain, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        self.gpredict_doppler_0 = gpredict.doppler(self.set_doppler_freq, "localhost", 4532, False)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(50, (firdes.low_pass(1, samp_rate, filter_width/2.0, filter_width/20.0)), doppler_freq-freq+offset, samp_rate)
        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_short*1, destination, port, 1472, True)
        self.blocks_float_to_short_0 = blocks.float_to_short(1, 32767)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(0.2)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.blocks_float_to_short_0, 0))    
        self.connect((self.blocks_float_to_short_0, 0), (self.blocks_udp_sink_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_quadrature_demod_cf_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))    

    def get_bb_gain(self):
        return self.bb_gain

    def set_bb_gain(self, bb_gain):
        self.bb_gain = bb_gain
        self.osmosdr_source_0.set_bb_gain(self.bb_gain, 0)

    def get_destination(self):
        return self.destination

    def set_destination(self, destination):
        self.destination = destination

    def get_filter_width(self):
        return self.filter_width

    def set_filter_width(self, filter_width):
        self.filter_width = filter_width
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1, self.samp_rate, self.filter_width/2.0, self.filter_width/20.0)))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_doppler_freq(self.freq)
        self.osmosdr_source_0.set_center_freq(self.freq-self.offset, 0)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.doppler_freq-self.freq+self.offset)

    def get_freq_corr(self):
        return self.freq_corr

    def set_freq_corr(self, freq_corr):
        self.freq_corr = freq_corr
        self.osmosdr_source_0.set_freq_corr(self.freq_corr, 0)

    def get_gpredict_port(self):
        return self.gpredict_port

    def set_gpredict_port(self, gpredict_port):
        self.gpredict_port = gpredict_port

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain
        self.osmosdr_source_0.set_if_gain(self.if_gain, 0)

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
        self.osmosdr_source_0.set_center_freq(self.freq-self.offset, 0)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.doppler_freq-self.freq+self.offset)

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.osmosdr_source_0.set_gain(self.rf_gain, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1, self.samp_rate, self.filter_width/2.0, self.filter_width/20.0)))

    def get_doppler_freq(self):
        return self.doppler_freq

    def set_doppler_freq(self, doppler_freq):
        self.doppler_freq = doppler_freq
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.doppler_freq-self.freq+self.offset)


def argument_parser():
    description = 'Receives with an RTL-SDR and streams the FM audio'
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option, description=description)
    parser.add_option(
        "", "--bb-gain", dest="bb_gain", type="eng_float", default=eng_notation.num_to_str(20),
        help="Set baseband gain [default=%default]")
    parser.add_option(
        "", "--destination", dest="destination", type="string", default="localhost",
        help="Set localhost [default=%default]")
    parser.add_option(
        "", "--filter-width", dest="filter_width", type="eng_float", default=eng_notation.num_to_str(20000),
        help="Set FM filter width [default=%default]")
    parser.add_option(
        "-f", "--freq", dest="freq", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set frequency [default=%default]")
    parser.add_option(
        "", "--freq-corr", dest="freq_corr", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set frequency correction (ppm) [default=%default]")
    parser.add_option(
        "", "--gpredict-port", dest="gpredict_port", type="intx", default=4532,
        help="Set GPredict port [default=%default]")
    parser.add_option(
        "", "--if-gain", dest="if_gain", type="eng_float", default=eng_notation.num_to_str(20),
        help="Set IF gain [default=%default]")
    parser.add_option(
        "", "--offset", dest="offset", type="eng_float", default=eng_notation.num_to_str(50e3),
        help="Set centre frequency offset [default=%default]")
    parser.add_option(
        "", "--port", dest="port", type="intx", default=7355,
        help="Set port [default=%default]")
    parser.add_option(
        "", "--rf-gain", dest="rf_gain", type="eng_float", default=eng_notation.num_to_str(40),
        help="Set RF gain [default=%default]")
    return parser


def main(top_block_cls=rtlsdr_fm, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(bb_gain=options.bb_gain, destination=options.destination, filter_width=options.filter_width, freq=options.freq, freq_corr=options.freq_corr, gpredict_port=options.gpredict_port, if_gain=options.if_gain, offset=options.offset, port=options.port, rf_gain=options.rf_gain)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
