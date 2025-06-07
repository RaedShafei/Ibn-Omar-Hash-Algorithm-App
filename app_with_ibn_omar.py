
from flask import Flask, request, jsonify
from flask_cors import CORS
import math
import time
import os

app = Flask(__name__)
CORS(app)

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

def ibn_omar_hash(i_text):
    ti = time.time()
    iLen = len(bytearray(i_text, 'utf-8'))

    i = map(bin, bytearray(i_text, 'utf-8'))
    i = ''.join(i)
    i = i.replace('0b', '')

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
    paddingValue = (2048 % bSize)
    pv = (bSize % 2048)

    if bSize < 2048:
        padL = ''.ljust(paddingValue, '0')
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

    bLDec = sum([int(d) * (2 ** idx) for idx, d in enumerate(reversed(bL))])
    bRDec = sum([int(d) * (2 ** idx) for idx, d in enumerate(reversed(bR))])

    factorL = sum([int(d) for d in str(bLDec)])
    factorR = sum([int(d) for d in str(bRDec)])

    bLDecF = factorR * bLDec
    bRDecF = factorL * bRDec

    bLDecSTR = str(bLDecF)
    bRDecSTR = str(bRDecF)

    bLDec = ((bLDecF - int(lShift(bRDecSTR, 1270))) + (bLDecF - int(rShift(bRDecSTR, 309))) + (
            bLDecF - int(reverse(bRDecSTR, -31, 286)))) ** 3

    bRDec = ((bRDecF - int(lShift(bLDecSTR, 1469))) + (bRDecF - int(rShift(bLDecSTR, 309))) + (
            bRDecF - int(reverse(bLDecSTR, 46, 199)))) ** 5

    bLDec = abs(int(bLDec))
    bRDec = abs(int(bRDec))

    if iLen <= 1:
        iLen = 2  # Prevent log base <= 1

    Yl = abs(math.log(bLDec, iLen))
    Yr = abs(math.log(bRDec, iLen))

    primes = [101, 103, 107, 109, 113, 127, 131, 137, 139, 149]

    for e in primes:
        eL = int(math.ceil((e * Yr) / iLen))
        eR = int(math.ceil((e * Yl) / iLen))
        bLDec = (eL * bLDec) + eL
        bRDec = (eR * bRDec) + eR

    Y = int(math.floor(Yl * Yr))
    bDec = (bRDec + bLDec) / Y
    bDec = lShift(str(int(bDec)), Y)

    bBin = bin(int(bDec)).replace('0b', '')

    if len(bBin) > 1024:
        bBin = bBin.ljust(((len(bBin) // 1024) + 1) * 1024, '0')

    bBin = reverse(bBin, -306, -604)
    bBin = lShift(bBin, 1024)
    bBin = reverse(bBin, -910, -295)

    finalBlock = bBin[:1024]
    final = hex(int(finalBlock, 2))

    return final

@app.route('/hash', methods=['POST'])
def hash_input():
    data = request.get_json()
    clean_text = data.get('text', '')
    try:
        hashed = ibn_omar_hash(clean_text)
        return jsonify({'hash': hashed})
    except Exception as e:
        return jsonify({'hash': 'HASH_ERROR', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
