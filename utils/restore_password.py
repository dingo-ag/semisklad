import random
import string


def generate_key(size=50, chars=string.hexdigits.lower()):
    return ''.join([random.choice(chars) for _ in range(size)])


def create_code(user_id=None):
    if user_id is None:
        raise ValueError('User_id must be defined')
    key = generate_key()
    tmp = hex(user_id*5835)[2:]
    code = key[:31] + tmp + key[31:]
    return code


def check_code(code, user_id=None):
    tmp = code[31:-19]
    u_id = int(tmp, 16)/5835
    if user_id == u_id:
        return True
    else:
        return False


if __name__ == '__main__':
    print(create_code(user_id=2))
    print(create_code(user_id=2))
    assert (check_code(create_code(user_id=2), 2))
