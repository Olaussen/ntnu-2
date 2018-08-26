#!/usr/bin/python3

from math import log2, floor


def fractional_bits(bits):
    m = [int(bit) for bit in bits]
    s = 1 + sum([bit*2**-(i+1) for i, bit in enumerate(m)])
    return s


def eksponent(bits):
    e = [int(bit) for bit in bits][::-1]
    s = sum([bit*2**i for i, bit in enumerate(e)])
    l = 2**(len(e)-1) - 1
    #print('---------', s, l, s-l, bits)
    return s - l


def fortegn(bit):
    return -1 if int(bit) else 1


def tall_fra_bit(bits, bitpresisjon=64):
    sign = fortegn(bits[0])
    f = fractional_bits(bits[1:24 if bitpresisjon == 32 else 53])
    e = eksponent(bits[24 if bitpresisjon == 32 else 53:])
    return sign * f * 2**e


def tall_fra_64bit(bits):
    return tall_fra_bit(bits, 64)


def tall_fra_32bit(bits):
    return tall_fra_bit(bits, 32)


print('Fra bit til desimaltall:')
print('9.4   =>', tall_fra_64bit('000101100110011001100110011001100110011001100110011010000000010'))
print('1.25  =>', tall_fra_64bit('001000000000000000000000000000000000000000000000000001111111111'))
print('14    =>', tall_fra_32bit('01100000000000000000000010000010'))
print('263.3 =>', tall_fra_32bit('00000011101001100110011010000111'))
print('0.25  =>', tall_fra_32bit('00000000000000000000000001111101'))
print('0.25  =>', tall_fra_64bit('000000000000000000000000000000000000000000000000000001111111101'))


def tall_til_binær(tall, bredde=0, legg_til_foran=True):
    retning = '>' if legg_til_foran else '<'
    return ('{:' + retning + '0' + str(bredde) + 'b}').format(int(tall))


def tall_til_binærdesimal(desimaltall, presisjon=64):
    bits = []
    acc = desimaltall
    for i in range(presisjon):
        acc *= 2
        if acc >= 1:
            bits.append('1')
            acc -= 1
        else:
            bits.append('0')
    return ''.join(bits)


def tall_til_bit(tall, bitpresisjon=64):
    fortegn_binær = '0' if tall >= 0 else '1'

    eksponent_bias = 2**(7 if bitpresisjon == 32 else 10) - 1
    eksp = floor(log2(abs(tall)))
    eksponent_binær = tall_til_binær(eksponent_bias + eksp, 8 if bitpresisjon == 32 else 11)

    heltall = abs(int(tall))
    desimaltall = abs(tall) - heltall
    heltall_binær = tall_til_binær(heltall)
    desimaltall_binær = tall_til_binærdesimal(desimaltall, bitpresisjon)

    mantissa_binær = heltall_binær + desimaltall_binær
    normalisert_mantissa_binær = mantissa_binær[mantissa_binær.index('1') + 1:][:23 if bitpresisjon == 32 else 52]

    #print(heltall_binær, desimaltall_binær, normalisert_mantissa_binær, eksp)
    #print(fortegn_binær + normalisert_mantissa_binær + eksponent_binær, eksponent_binær)
    return fortegn_binær + normalisert_mantissa_binær + eksponent_binær


def tall_til_64bit(tall):
    return tall_til_bit(tall, 64)


def tall_til_32bit(tall):
    return tall_til_bit(tall, 32)


# d)
def fl(a):
    return tall_fra_bit(tall_til_bit(a))


def fl32(a):
    return tall_fra_32bit(tall_til_32bit(a))


def fl64(a):
    return tall_fra_64bit(tall_til_64bit(a))

print()
print('Oppgave d)')
print(' - 0.25 =>', fl32(0.25))
print(' - 4.5  =>', fl32(4.5))
print(' - 0.1  =>', fl32(0.1))
