# kw1fox-1
Software and tools for the KW1FOX-1 radio station

## Setting up Pulseaudio

There are a lot of ways to get audio in and out of a container, for rn i decided to try this method: https://github.com/mviereck/x11docker/wiki/Container-sound:-ALSA-or-Pulseaudio#pulseaudio-over-tcp

Maybe ill change it later, anyway, to load the module on the host, do this:

```
pactl load-module module-native-protocol-tcp  port=34567 auth-ip-acl=$Containerip
```
