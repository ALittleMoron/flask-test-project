import string
import re
from typing import Union, List, Tuple, Optional


from .cryptomath import co_prime_number


EncryptedMessage, DecryptedMessage = str, str
Result = List[Optional[EncryptedMessage], Optional[DecryptedMessage]]
SessionID = int


def get_alhabet_indexes_list_from_text(message: str):
    return [(string.ascii_lowercase+' ').find(x.lower()) for x in message]

def get_text_from_alphabet_indexes(alphabet_indexes: list):
    return ''.join([(string.ascii_lowercase+' ')[x] for x in alphabet_indexes])


def elgamal(
        message: str,
        keys: Union[str, List, Tuple],
        to_encrypt: bool,
        to_decrypt: bool) -> List[SessionID, Result]:
    
    if isinstance(keys, str):
        keys = re.findall(r'\d+', keys)
    
    # ASCII representation of message
    message = get_alhabet_indexes_list_from_text(message)

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
            b.append(pow(y, k, p)) # BUG: не тот метод шифрования. 
                                   #      Там нужно что-то другое
        semi_result = str(list(zip(a, b))).replace(' ', '')
        result.append(re.findall(r'\(.+\)', semi_result))
    if to_decrypt:
        a, b = [], []
        message = result[0] if to_encrypt else message
        if isinstance(message, list):
            pass
        elif isinstance(message, str):
            pass

    return result


if __name__ == "__main__":
    pass