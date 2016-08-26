# gr-frontends
GNUradio frontends that stream from different hardware to UDP

This repository is a collection of frontends that serve to stream from several
different SDR hardware, recordings and other sources to UDP. The UDP data can be
processed by another program.

The stream format is 1 channel, 48kHz, little-endian int16_t. It is the same
format that [gqrx uses to stream audio](http://gqrx.dk/doc/streaming-audio-over-udp)

The main goal of this repository is to be used with
[gr-satellites](https://github.com/daniestevez/gr-satellites), but it can be
used with many other pieces of software.

## Usage

You can open the `.grc` file with `gnuradio-companion` and edit the parameters
(they are on the upper part of the flowgraph). You can also run the `.py` script
and specify the parameters on the command line. Use the `-h` flag to get help
on how to specify the parameters.

## WAV file streamers

The WAV file streamers can be:

  * Fast. This means that the WAV is streammed as fast as possible. The
    receiving application may loose data if it can't process it as fast. The
    streamer should run almost instantly.
  * Realtime. This means that the WAV file is played in realtime at normal
    speed. The streamer runs for the whole duration of the WAV file at normal
    playback speed.

The WAV file streamers also depend on the endiannes of your platform (if in
doubt, try little-endian first).

The available streamers are the following:

  * `wav_48kHz_fast_be` 48kHz WAV fast streamer (big-endian)
  * `wav_48kHz_fast_le` 48kHz WAV fast streamer (little-endian)
  * `wav_48kHz_realtime_be` 48kHz WAV realtime streamer (big-endian)
  * `wav_48kHz_realtime_le` 48kHz WAV realtime streamer (little-endian)

*Hint:* It is sometimes useful to play a WAV file repeatedly in loop. By default
 the streamers will only play the file once, but you can edit them with
 `gnuradio-companion` and set the WAV file to repeat.
 