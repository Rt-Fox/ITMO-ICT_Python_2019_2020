def encrypt_caesar(plaintext, k) -> str:
    """
        >>> encrypt_caesar("PYTHON")
        'SBWKRQ'
        >>> encrypt_caesar("python")
        'sbwkrq'
        >>> encrypt_caesar("Python3.6")
        'Sbwkrq3.6'
        >>> encrypt_caesar("")
        ''

        """
    ciphertext = ''
    for ch in plaintext:
        if ch.isalpha():
            code = ord(ch) + k
            if 'a' <= ch <= 'z' and code > ord('z'):
                code -= 26
            elif 'A' <= ch <= 'Z' and code > ord('Z'):
                code -= 26
            ciphertext += chr(code)
        else:
            ciphertext += ch
    return ciphertext


def decrypt_caesar(ciphertext, k) -> str:
    """
        >>> decrypt_caesar("SBWKRQ")
        'PYTHON'
        >>> decrypt_caesar("sbwkrq")
        'python'
        >>> decrypt_caesar("Sbwkrq3.6")
        'Python3.6'
        >>> decrypt_caesar("")
        ''
        """
    plaintext = ''
    for ch in ciphertext:
        if ch.isalpha():
            code = ord(ch) - k
            if 'a' <= ch <= 'z' and code < ord('a'):
                code += 26
            elif 'A' <= ch <= 'Z' and code < ord('A'):
                code += 26
            plaintext += chr(code)
        else:
            plaintext += ch
    return plaintext


plaintext = str(input('Your message: '))
k = int(input('Shift: '))
while k > 26:
    k = int(input('Shift: '))

ciphertext = encrypt_caesar(plaintext, k)
print("Cod: " + ciphertext)
print("Not Cod: " + decrypt_caesar(ciphertext, k))