import sys
from serial import Serial

DEBUG = False
VERBOSE = False  # Verbose mode provides more raw EEG updates
DEFAULT_PORT = '/dev/cu.MindflexOne-DevB'

MAX_PACKET_LEN = 169
RESET_CODE = '\x00\xF8\x00\x00\x00\xE0'

def _cb(data):
    print data

def mf_parser(packet):
    # See the MindSet Communications Protocol
    ret = {}
    # The first byte in the list was packet_len, so start at i = 1 
    i = 1
    while (i < len(packet) - 1):
        code_level = ord(packet[i])
        # signal quality
        if code_level == 0x02:
            ret['quality'] = ord(packet[i + 1])
            i += 2
        # attention
        elif code_level == 0x04:
            ret['attention'] = ord(packet[i + 1])
            i += 2
        # meditation
        elif code_level == 0x05:
            ret['meditation'] = ord(packet[i + 1])
            i += 2
        # EEG power
        elif code_level == 0x83:
            ret['eeg'] = []
            for c in xrange(i + 1, i + 25, 3):
                ret['eeg'].append(ord(packet[c]) << 16 | 
                                  ord(packet[c + 1]) << 8 | 
                                  ord(packet[c + 2]))
            i += 26
        # Raw Wave Value
        elif code_level == 0x80:
            ret['eeg_raw'] = ord(packet[i+1]) << 8 | ord(packet[i+2])
            i += 4
    return ret


class MindFlexConnection(object):
    def __init__(self, port=DEFAULT_PORT, debug=DEBUG, verbose=VERBOSE):
        self.debug = debug
        self.verbose = verbose
        self.ser = Serial(port=port, baudrate=57600)
        if self.debug:
            print 'Connection open'
        if self.debug:
            self.received = []

    def close(self):
        if self.ser.isOpen():
            try:
                self.ser.close()
            except Exception as e:
                pass
                #import pdb; pdb.post_mortem()
            print 'Connection closed'

    def read(self, callback=_cb):
        prev_byte = 'c'
        in_packet = False
        try:
            while True:
                cur_byte = self.ser.read(1)
                if self.debug:
                    self.received.append(cur_byte)

                # If in Mode 1, enable Mode 2
                if (not in_packet and 
                    ord(prev_byte) == 224 and 
                    ord(cur_byte) == 224):
                    # Send reset code
                    self.ser.write(RESET_CODE)
                    if self.debug and ord(self.ser.read(1)) != 224:
                        print 'Mode 2 enabled'
                    prev_byte = cur_byte
                    continue

                # Look for the start of the packet
                if (not in_packet and 
                    ord(prev_byte) == 170 and 
                    ord(cur_byte) == 170):
                    # print 'Start of new packet'
                    in_packet = True
                    packet = []
                    continue

                if in_packet:
                    if len(packet) == 0:
                        if ord(cur_byte) == 170:
                            continue
                        packet_len = ord(cur_byte)
                        checksum_total = 0
                        packet = [cur_byte]
                        if packet_len >=  MAX_PACKET_LEN:
                            print 'Packet too long: %s' % packet_len
                            in_packet = False
                            continue
                    elif len(packet) - 1  == packet_len:
                        packet_checksum = ord(cur_byte)
                        in_packet = False
                        if (~(checksum_total & 255) & 255) == packet_checksum:
                            try:
                                if self.verbose or packet_len > 4:
                                    ret = mf_parser(packet)
                                    if self.debug:
                                        print ret
                                    callback(ret)
                            except Exception as e:
                                print 'Could not parse because of %s' % e
                        else:
                            print 'Warning: invalid checksum'
                            print ~(checksum_total & 255) & 255
                            print packet_checksum
                            print packet
                            if self.debug:
                                import pdb; pdb.set_trace()
                    else:
                        checksum_total += ord(cur_byte)
                        packet.append(cur_byte)

                # keep track of last byte to catch sync bytes
                prev_byte = cur_byte
 
        except KeyboardInterrupt as e:
            self.close()
            if self.debug:
                print 'Exiting'
            sys.exit(0)

def get_argparser():
    from argparse import ArgumentParser
    desc = 'Connect to MindFlex via bluetooth'
    prs = ArgumentParser(description=desc)
    prs.add_argument('--port', '-p', default=DEFAULT_PORT)
    prs.add_argument('--debug', action='store_true')
    prs.add_argument('--verbose', '-v', action='store_true')
    return prs

if __name__ == '__main__':
    parser = get_argparser()
    args = parser.parse_args()
    connection = MindFlexConnection(port=args.port, 
                                    debug=args.debug, 
                                    verbose=args.verbose)
    connection.read()
