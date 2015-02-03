# DIY EEGs via ThinkGear/MindFlex

This is a basic EEG toy built for MindFlex's ThinkGear headset.

## Hardware needed

 - [MindFlex](https://en.wikipedia.org/wiki/Mindflex) Headset -- you can get one [relatively cheap on eBay](http://www.ebay.com/sch/i.html?_nkw=Mindflex+headset).
 - HC-06 Bluetooth transciever -- see [Amazon](http://www.amazon.com/gp/product/B0093XAV4U).
 - Any TTL link -- for changing the baudrate on HC-06... an Arduino will work

## Instructions

### Hardware

 - Solder connections to the T (transmit), R (recieve), ground, and power pins in the ThinkGear headset
 - Set HC-06 to 57600 baud with command AT+BAUD7 via TTL (only necessary once)
 - Connect HC-06 to the ThinkGear headset

There are more detailed setup instructions below in the references.

### Software

Setup: run `pip install -r requirements.txt` for python dependencies

 - Connect to the HC-06 via bluetooth
 - Run `mindflex.py`

Note, mindflex.py will switch the ThinkGear into Mode 0x02 by sending the following command over 57600 baud after each power up: `0x00, 0xF8, 0x00, 0x00, 0x00, 0xE0`.

## Data

Example response data:

```python
{
	'quality': 0, 		# Signal strength (0-200, lower is better)
	'attention': 100, 	# NeuroSky attention score (0-100)
	'meditation': 75 	# NeuroSky meditation score (0-100)
	'eeg': [			# Array of eight FFT values
		1572953, 		# Delta
		14811157, 		# Theat
		7077897, 		# Low alpha
		14876686, 		# High alpha
		14417931, 		# Low beta
		3932175, 		# High beta
		7208965, 		# Low gamma
		4784137], 		# Mid gamma
}
```

## References

 - See these instructions on [soldering and HC-06 firmware](http://www.instructables.com/id/Mindflex-EEG-with-raw-data-over-Bluetooth/?ALLSTEPS).
 - More information on [how it works](http://frontiernerds.com/brain-hack).
 - [MindSet Communications Protocol](http://wearcam.org/ece516/mindset_communications_protocol.pdf).
 - For reference: Arduino [Brain library](https://github.com/kitschpatrol/Brain), [brain.py](https://gist.github.com/zatarra/6d2be801010c7eb844f0)

# Thanks

Many thanks to [arpruss](http://www.instructables.com/member/arpruss/), [David Gouveia](http://www.davidgouveia.net/2014/06/converting-the-mindflex-into-an-open-source-wireless-eeg-tool/), and [Eric Mika](https://github.com/kitschpatrol) for their documentation and code on working with mindflex.

# License

Copyright (c) 2015, Stephen LaPorte
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
