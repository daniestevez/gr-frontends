# gr-frontends
GNUradio frontends that stream from different hardware to UDP

This repository is a collection of frontends that serve to stream from several
different SDR hardware, recordings and other sources to UDP. The UDP data can be
processed by another program.

The stream format is 1 channel, 48kHz, little-endian int16_t. It is the same
format that gqrx uses to stream audio
(http://gqrx.dk/doc/streaming-audio-over-udp)

The main goal of this repository is to be used with gr-satellites
(https://github.com/daniestevez/gr-satellites), but it can be used with many
other pieces of software.

