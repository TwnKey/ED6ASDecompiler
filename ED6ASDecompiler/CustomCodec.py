
import codecs
import struct

codec_name = 'sora_fr'

map = { 'À' : 0xA0, 
        'Â' : 0xA1, 
        'Ä' : 0xA4, 
        'Ç' : 0xA6, 
        'È' : 0xA7, 
        'É' : 0xA8, 
        'Ê' : 0xA9, 
        'Ë' : 0xAA, 
        'Î' : 0xAB, 
        'Ï' : 0xAC, 
        'Ô' : 0xAD, 
        'Ù' : 0xAE, 
        'Û' : 0xAF, 
        'Ü' : 0xB0, 
        'à' : 0xB1, 
        'â' : 0xB2, 
        'ä' : 0xB3, 
        'ç' : 0xB4, 
        'è' : 0xB5, 
        'é' : 0xB6, 
        'ê' : 0xB7, 
        'ë' : 0xB8, 
        'î' : 0xB9, 
        'ï' : 0xBA, 
        'ô' : 0xBB, 
        'ù' : 0xBC, 
        'û' : 0xBD, 
        'ü' : 0xBE, 
        'ÿ' : 0xBF, 
        'Œ' : 0xC0, 
        'œ' : 0xC1, 
        'Ÿ' : 0xC2, 
        'À' : 0xC3, 
        '°' : 0xC4, 
        '«' : 0xC5, 
        '»' : 0xC6, }

class Codec(codecs.Codec):
    def encode(self, input, errors='strict'):
        output = bytearray()

        for char in input:
            if char in map.keys():
                output.extend(struct.pack('<B', map[char]))
            else:
                output.extend(char.encode("cp932"))

        return bytes(output), len(output)
        #return codecs.charmap_encode(input, errors, encoding_map)

    def decode(self, input, errors='strict'):
        return codecs.charmap_decode(input, errors, decoding_map)


class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final=False):
        return codecs.charmap_encode(input, self.errors, encoding_map)[0]

class IncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input, final=False):
        return codecs.charmap_decode(input, self.errors, decoding_map)[0]


class StreamReader(Codec, codecs.StreamReader):
    pass

class StreamWriter(Codec, codecs.StreamWriter):
    pass


def _register(encoding):
    if encoding == codec_name:
        return codecs.CodecInfo(
            name=codec_name,
            encode=Codec().encode,
            decode=Codec().decode,
            incrementalencoder=IncrementalEncoder,
            incrementaldecoder=IncrementalDecoder,
            streamreader=StreamReader,
            streamwriter=StreamWriter)

codecs.register(_register)