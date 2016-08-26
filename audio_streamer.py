#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Audio source streamer
# Author: Daniel Estevez
# Description: Streams an audio source
# Generated: Fri Aug 26 21:19:49 2016
##################################################

from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser

class audio_streamer(gr.top_block):

    def __init__(self, port=7355, destination="localhost"):
        gr.top_block.__init__(self, "Audio source streamer")

        ##################################################
        # Parameters
        ##################################################
        self.port = port
        self.destination = destination

        ##################################################
        # Blocks
        ##################################################
        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_short*1, destination, port, 1472, True)
        self.blocks_float_to_short_0 = blocks.float_to_short(1, 32767)
        self.audio_source_0 = audio.source(48000, "", True)

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


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option("", "--port", dest="port", type="intx", default=7355,
        help="Set port [default=%default]")
    parser.add_option("", "--destination", dest="destination", type="string", default="localhost",
        help="Set localhost [default=%default]")
    (options, args) = parser.parse_args()
    tb = audio_streamer(port=options.port, destination=options.destination)
    tb.start()
    tb.wait()
