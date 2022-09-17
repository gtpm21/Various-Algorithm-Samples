#Simple implementation of the Vigenere cipher using ASCII characters in the range of 32 to 127.

def Vigenere(txt, key, type):
    if not txt:
        print ('Needs text.')
        return
    if not key:
        print ('Needs key.')
        return
    if type not in ('d', 'e'):
        print ('Type must be "d" or "e".')
        return
    if any(t not in universe for t in key):
        print ('Invalid characters in the key. Must only use ASCII symbols.')
        return

    ret_txt = ''
    k_len = len(key)

    for i, l in enumerate(txt):
        if l not in universe:
            ret_txt += l
        else:
            txt_idx = universe.index(l)

            k = key[i % k_len]
            key_idx = universe.index(k)
            if type == 'd':
                key_idx *= -1

            code = universe[(txt_idx + key_idx) % uni_len]

            ret_txt += code

    return ret_txt

if __name__ == "__main__":

    universe = [c for c in (chr(i) for i in range(32,127))]
    uni_len = len(universe)

    type = input("Enter 'e' for encryption or 'd' for decryption: \n")
    msg = input("Enter text: \n")
    key = input("Enter key: \n")
    print ("Result: ", Vigenere(msg, key, type))
    