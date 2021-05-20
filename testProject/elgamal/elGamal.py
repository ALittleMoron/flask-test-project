import string
import re
from typing import Union, List, Tuple, Optional


from .cryptomath import co_prime_number, find_mod_inverse


EncryptedMessage, DecryptedMessage = List[Tuple[int]], str
Result = List
SessionID = int


def get_alhabet_indexes_list_from_text(message: str):
    return [(string.ascii_lowercase+' ').find(x.lower()) for x in message]

def get_text_from_alphabet_indexes(alphabet_indexes: list):
    return ''.join([(string.ascii_lowercase+' ')[x] for x in alphabet_indexes])


def elgamal(
        message: Union[str, list],
        keys: Union[str, List, Tuple],
        to_encrypt: bool,
        to_decrypt: bool):
    
    if isinstance(keys, str):
        keys = re.findall(r'\d+', keys)
    
    # ASCII representation of message
    if isinstance(message, str) and not '(' in message:
        message = get_alhabet_indexes_list_from_text(message)
    elif '(' in message:
        semi_message = []
        for string_represent in message:
            a, b = re.findall(r'\d+', string_represent)
            semi_message.append((a,b))
        message = semi_message

    # keys formal choose
    if len(keys) == 3: 
        y, g, p = keys
    elif len(keys) == 4:
        y, g, p, x = keys

    # SessionID
    k = co_prime_number(p-1) 

    result = []
    # action choose
    if to_encrypt:
        a, b = [], []
        for ascii_letter in message:
            a.append(pow(g, k, p))
            b.append(pow(pow(y, k, p)*pow(ascii_letter, 1, p), 1, p)) # метод цепочки
        semi_result = str(list(zip(a, b))).replace(' ', '')
        result.append(re.findall(r'\(.+?\)', semi_result))
    if to_decrypt:
        semi_result = ''
        if to_encrypt:
            message = result[0]
        for tuple_of_bigram in message:
            enc_a, enc_b = re.findall(r'\d+', tuple_of_bigram)
            decryptedLetter = pow(pow(int(enc_b), 1, p)*find_mod_inverse(int(enc_a)**x, p), 1, p) # тоже метод цепочки
            try:
                if decryptedLetter != 26:
                    semi_result += string.ascii_lowercase[decryptedLetter]
                else:
                    semi_result += ' '
            except IndexError as e:
                semi_result += '<Not recognized>'
        result.append(semi_result)

    return result


if __name__ == "__main__":
    from keyGen import keyGen
    keys = keyGen(8)
    pub_key, priv_key = keys
    keys = *pub_key, priv_key
    y, g, p, x = *pub_key, priv_key
    print(len(keys))
    message = 'message to encrypt and decrypt'
    result = elgamal(message, keys, True, True)
    print(result)