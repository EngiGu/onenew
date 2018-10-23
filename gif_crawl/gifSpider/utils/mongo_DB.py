import hashlib
from pymongo import MongoClient


class MongoDB():
    def __init__(self, db_uri, db_name, need_auth=False, auth=()):
        self.db = MongoClient(db_uri)[db_name]
        if need_auth:
            self.db.authenticate(*auth)

    def insert_one(self, tb_name, data, encrypt_word):
        try:
            data['_id'] = hashlib.md5(encrypt_word.encode()).hexdigest()[:16]
            rs = self.db[tb_name].insert_one(data)
            return True
        except Exception as e:
            if 'duplicate key error index' in str(e):
                return False
            print('other mistake -->', e)
            return None

    def delete_one(self, tb_name, key_value_dict):
        try:
            self.db[tb_name].delete_one(key_value_dict)
            return True
        except Exception as e:
            return False

    def get_one_and_pop_one(self, tb_name):
        res = self.db[tb_name].find_one()
        if self.delete_one(tb_name, {'_id': res['_id']}):
            return res
        return None


if __name__ == '__main__':
    m = MongoDB('mongodb://sooko.ml:36565', 'yaohuo', need_auth=True, auth=('tk', 'Aa123456'))
    if m.insert_one('test', {"name": "li8", "age": 8}, 'xxxxx'):
        print('insert success!')
    else:
        print('already exists!')

    # if m.delete_one('test', {"age": 8}):
    #     print('delete success!')
    # else:
    #     print('delete failed!')

    print(m.get_one_and_pop_one('test'))
