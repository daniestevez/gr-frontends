#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: WAV 48KHz file real time streamer (little-endian platform)
# Author: Daniel Estevez
# Description: Streams a WAV 48kHz file in real time
# Generated: Fri Aug 26 18:18:02 2016
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser

class wav_48kHz_realtime_le(gr.top_block):

    def __init__(self, input_file="", port=7355, destination="localhost"):
        gr.top_block.__init__(self, "WAV 48KHz file real time streamer (little-endian platform)")

        ##################################################
        # Parameters
        ##################################################
        self.input_file = input_file
        self.port = port
        self.destination = destination

        ##################################################
        # Blocks
        ##################################################
        self.blocks_wavfile_source_0 = blocks.wavfile_source(input_file, False)
        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_short*1, destination, port, 1472, True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_short*1, 48000,True)
        self.blocks_float_to_short_0 = blocks.float_to_short(1, 32767)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_float_to_short_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.blocks_udp_sink_0, 0))    
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_float_to_short_0, 0))    


    def get_input_file(self):
        return self.input_file

    def set_input_file(self, input_file):
        self.input_file = input_file

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port

    def get_destination(self):
        return self.destination

    def set_destination(self, destination):
        self.destination = destination


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option("-f", "--input-file", dest="input_file", type="string", default="",
        help="Set file [default=%default]")
    parser.add_option("", "--port", dest="port", type="intx", default=7355,
        help="Set port [default=%default]")
    parser.add_option("", "--destination", dest="destination", type="string", default="localhost",
        help="Set localhost [default=%default]")
    (options, args) = parser.parse_args()
    tb = wav_48kHz_realtime_le(input_file=options.input_file, port=options.port, destination=options.destination)
    tb.start()
    tb.wait()
