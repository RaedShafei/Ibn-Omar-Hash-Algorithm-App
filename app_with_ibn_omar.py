
from flask import Flask, request, jsonify
import math
import time

app = Flask(__name__)

def rShift(s1, d):
    rs = s1[0:len(s1) - d]
    rss = s1[len(s1) - d:]
    return rss + rs

def lShift(s1, d):
    ls = s1[0:d]
    lss = s1[d:]
    return lss + ls

def reverse(seq, start, stop):
    seq = list(seq)
    size = stop + start
    for i in range(start, (size + 1) // 2):
        j = size - i
        seq[i], seq[j] = seq[j], seq[i]
    return ''.join(seq)

def sanitize_input(text):
    return text.replace('\n', '\\n').replace('\r', '').strip()

def ibn_omar_hash(i):
    ti = time.time()
    isize = len(i)

    i = map(bin, bytearray(i))
    i = ''.join(i).replace('0b', '')

    A = '1100010001111001001110110001010001100101001011000101100110010011101100010111111001010010'
    B = '11001000111110010011101100100100011001010001110010011101100011001011001010010'
    C = '11000101101110010011111100011011111001010001110010100001100100101011001010010'
    D = '1100100001111001001110110010001001100100111011001000101110010011111100100011011001010010'
    E = '1100011001111001001110110001110011100101001011001000001110010011101100011010111001010010'
    F = '1100100001011001001110110001100011100100111011000110100110010011101100010101011001010010'
    G = '110001010111100100111011000101110110010011101100011000011001010010'
    H = '110001101101100100111011000111000110010100001100011101011001010010'

    b = i + A + i + B + i + C + i + D + i + E + i + F + i + G + i + H + i
    block = b + b + '1'
    bSize = len(block)

    if bSize < 2048:
        padL = ''.ljust((2048 % bSize), '0')
        blocks = block + padL
    elif bSize > 2048:
        pv = ((bSize // 2048) + 1) * 2048 - bSize
        padG = ''.ljust(pv, '0')
        blocks = block + padG
    else:
        blocks = block

    blocksR = rShift(blocks, 604)
    andR = int(blocks) & int(blocksR)
    xoR = int(blocks) ^ int(blocksR)
    bR = andR | xoR
    bR = rShift(str(bR), 604)
    bR = int(bR)
    bR = '{0:b}'.format(bR)

    blocksL = lShift(blocks, 309)
    andL = int(blocks) & int(blocksL)
    xoL = int(blocks) ^ int(blocksL)
    bL = andL | xoL
    bL = lShift(str(bL), 309)
    bL = int(bL)
    bL = '{0:b}'.format(bL)

    bLDec = sum([int(d) for d in bL])
    bRDec = sum([int(d) for d in bR])
    iDecimal = sum([int(d) for d in blocks])

    bLDecF = bRDec * bLDec
    bRDecF = bLDec * bRDec

    bLDecSTR = str(bLDecF)
    bRDecSTR = str(bRDecF)

    try:
        bLDec = ((bLDecF - int(lShift(bRDecSTR, 1270))) +
                 (bLDecF - int(rShift(bRDecSTR, 309))) +
                 (bLDecF - int(reverse(bRDecSTR, -31, 286)))) ** 3
        bRDec = ((bRDecF - int(lShift(bLDecSTR, 1469))) +
                 (bRDecF - int(rShift(bLDecSTR, 309))) +
                 (bRDecF - int(reverse(bLDecSTR, 46, 199)))) ** 5
    except:
        return "HASH_ERROR"

    bLDec = abs(int(bLDec))
    bRDec = abs(int(bRDec))

    iLen = len(i)
    try:
        Yl = abs(math.log(bLDec, iLen))
        Yr = abs(math.log(bRDec, iLen))
    except:
        return "HASH_ERROR"

    primes = [101, 103, 107, 109, 113, 127, 131, 137, 139, 149,
              151, 157, 163, 167, 173, 179, 181, 191, 193, 197,
              199, 211, 223, 227, 229, 233, 239, 241, 251, 257,
              263, 269, 271, 277, 281, 283, 293, 307, 311, 313]

    for e in primes:
        eL = int(math.ceil((e * Yr) / iLen))
        bLDec = (eL * bLDec) + eL

    for e in primes:
        eR = int(math.ceil((e * Yl) / iLen))
        bRDec = (eR * bRDec) + eR

    try:
        Y = int(math.floor(Yl * Yr))
        bDec = (bRDec + bLDec) / Y
        bDec = int(lShift(str(bDec), Y))
        bBin = bin(bDec).replace('0b', '')
        pad_length = ((len(bBin) // 1024) + 1) * 1024 - len(bBin)
        bBin = bBin + ''.ljust(pad_length, '0')
        bBin = reverse(bBin, -306, -604)
        bBin = lShift(bBin, 1024)
        bBin = reverse(bBin, -910, -295)
        finalBlock = bBin[:1024]
        final = hex(int(finalBlock, 2)).replace('L', '')
        return final
    except:
        return "HASH_ERROR"

@app.route('/hash', methods=['POST'])
def hash_input():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing text field'}), 400

    raw_text = data['text']
    clean_text = sanitize_input(raw_text)
    hashed = ibn_omar_hash(clean_text)

    with open('hash_log.txt', 'a') as log:
        log.write("input: {}\n".format(clean_text))
        log.write("hash : {}\n".format(hashed))
        log.write("-----\n")

    return jsonify({'hash': hashed})

if __name__ == '__main__':
    app.run(debug=True)
