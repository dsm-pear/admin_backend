import bcrypt


class HashService(object):
    @staticmethod
    def hash_string_to_password(password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())\
            .decode('utf-8')

    @staticmethod
    def compare_pw_and_hash(password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
