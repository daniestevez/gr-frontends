# gr-frontends
GNUradio frontends that stream from different hardware to UDP

This repository is a collection of frontends that serve to stream from several
different SDR hardware, recordings and other sources to UDP. The UDP data can be
processed by another program.

The stream format is 1 channel 48kHz int16_t. It is the same format that
[gqrx uses to stream audio](http://gqrx.dk/doc/streaming-audio-over-udp)

The main goal of this repository is to be used with
[gr-satellites](https://github.com/daniestevez/gr-satellites), but it can be
used with many other pieces of software.

## Usage

You can open the `.grc` file with `gnuradio-companion` and edit the parameters
(they are on the upper part of the flowgraph). You can also run the `.py` script
and specify the parameters on the command line. Use the `-h` flag to get help
on how to specify the parameters.

## WAV file streamers

You have to choose the appropriate sampling rate. The available streamers are the following:

  * `wav_48kHz` 48kHz WAV streamer
  * `wav_44kHz` 44.1kHz WAV streamer

*Hint:* It is sometimes useful to play a WAV file repeatedly in loop. By default
 the streamers will only play the file once, but you can edit them with
 `gnuradio-companion` and set the WAV file to repeat.
 
