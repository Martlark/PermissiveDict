import random
import string
import unittest

from permissive_dict import PermissiveDict


def random_string(length: int = 5) -> str:
    """
    return a <length> long character random string of ascii_letters

    :param length: {int} number of characters to return
    :return: {str} a string
    """
    return ''.join([random.choice(string.ascii_letters) for _ in range(length)])


def random_int(min_num=1, max_num=200):
    """
    return an int inclusively between min_nim and max_num

    :param min_num:
    :param max_num:
    :return: {int} a number
    """
    return random.randint(min_num, max_num)


def random_float(max_num=200):
    """
    return a float between 0 and max_num

    :param max_num: {int}
    :return: {float} a number
    """
    return random.random() * max_num


class TestDict(unittest.TestCase):
    def setUp(self):
        self.lab_value = random_string()
        self.float_key = random_float()
        self.float_value = random_float()
        self.int_key = random_int()
        self.int_value = random_int()
        self.normal_dict = {'A': 1, 'A B': 2, 'b': 3, 4: 4, self.int_key: self.int_value, 'lab': self.lab_value,
                            self.float_key: self.float_value}
        self.pd = PermissiveDict(self.normal_dict)

    def test_del(self):
        test_value = random_string()
        d = PermissiveDict(a=test_value)
        self.assertEqual(test_value, d.a)
        del d['a']
        self.assertFalse('a' in d)
        self.assertEqual('', d.a)

    def test_setattr(self):
        test_value = random_float()
        d = PermissiveDict()
        d.a = test_value
        self.assertEqual(test_value, d.a)
        self.assertEqual(test_value, d.A)

    def test_kwargs(self):
        d = PermissiveDict(a=1, b=2, c=3)
        self.assertEqual(1, d.a)
        self.assertEqual(2, d.B)
        self.assertEqual(3, d["q,C"])

    def test_convert_dict(self):
        self.assertEqual(self.normal_dict, self.pd)
        self.assertFalse(self.normal_dict.get('a'))
        self.assertTrue(self.pd.get('a'))

    def test_map(self):
        # dog key could resolve using the dog, puppy, pupper or lab key
        self.assertNotEqual(self.lab_value, self.pd.dog)
        self.pd.set_map(dict(dog=['puppy', 'pupper', 'lab']))
        assert self.pd.dog == self.pd['dog'] == self.pd.get('dog') == self.lab_value
        self.assertNotEqual(self.pd.dog, self.pd.pupper)
        self.pd.set_map({})
        self.assertNotEqual(self.lab_value, self.pd.dog)

    def test_get(self):
        old_d = {'A': 1, 'A B': 2, 'b': 3, 4: 4, 'lab': 'woof!', 'hyphen-word': 'hyphen-word'}
        d = PermissiveDict(old_d)
        assert d.get('hyphen-word') == d.hyphen_word
        assert d.get('a') == d.get('A') == 1
        assert d.a_b == d.get('A_b') == d.get('A-b') == 2
        assert d.get('B') == 3
        assert d.a == d.A == 1
        assert d.q == ''
        assert d['a'] == d['A'] == d['A '] == d[' a '] == 1
        assert d[' a-b '] == d['A-b '] == d[' a_b '] == d[' a.b '] == 2
        assert ' a_b ' in d
        assert 'A' in d
        assert 'a' in d
        assert 'q' not in d

    def test_callable(self):
        self.assertEqual(self.float_value, self.pd(self.float_key))
        self.assertEqual(self.pd.a, self.pd('A'))
        self.assertEqual(self.pd.a, self.pd('a'))
        self.assertEqual(self.pd.a, self.pd('a '))
        self.assertEqual(self.pd.a, self.pd(' a '))
        self.assertEqual(self.pd.a, self.pd(' a'))
        self.assertEqual(self.pd.a, self.pd(' a\n'))
        self.assertEqual(self.pd.a_b, self.pd('a.b'))
        self.assertEqual(self.pd.a_b, self.pd('a-b'))
        self.assertEqual(self.pd.a_b, self.pd('a b'))

    def test_key_strip(self):
        self.assertEqual(self.pd.a, self.pd('a '))
        self.assertEqual(self.pd.a, self.pd(' a '))
        self.assertEqual(self.pd.a, self.pd(' a'))
        self.assertEqual(self.pd.a, self.pd(' a     \n  '))
        self.assertEqual(self.pd.a, self.pd(' a\n'))
        self.assertEqual(self.pd.a, self.pd('quirky, a\n,blog'))

    def test_get_raw_number(self):
        self.assertTrue(self.int_key in self.pd)
        self.assertTrue(self.float_key in self.pd)
        self.assertFalse(self.float_value * random_float() in self.pd)
        self.assertEqual(self.pd.get(str(self.float_key)), self.float_value)

    def test_get_number(self):
        self.assertTrue('4' in self.pd)
        self.assertTrue(4 in self.pd)
        self.assertTrue(self.pd.get(4) == self.pd.get('4') == 4)

    def test_multiple_keys(self):
        # missing value
        assert self.pd.flong == self.pd['flong'] == self.pd.get('flong') == self.pd.get('pling,plong,,') == ''
        # found value
        assert self.pd['flong,A'] == self.pd.get('plok,a') == self.pd.a
        self.assertEqual(self.pd['bad,4,good'], self.pd.get(4))
        self.assertEqual(self.pd['4,good,bad'], self.pd.get(4))
        self.assertEqual(self.pd['good,bad,4'], self.pd.get(4))
        self.assertEqual(self.pd['4,a,a_b,good,bad,4'], self.pd.get(4))
        self.assertEqual(self.pd['a_b,good,bad,4'], self.pd.a_b)
        self.assertEqual(self.pd['A.b,good,bad,4'], self.pd.a_b)
        self.assertEqual(self.pd['a-b,good,bad,4'], self.pd.a_b)
        self.assertEqual(self.pd['a B,good,bad,4'], self.pd.a_b)
        self.assertEqual(self.pd['ayb,good,bad,45'], '')

    def test_default(self):
        self.assertEqual(self.pd.no_exists, '')
        self.assertEqual(self.pd.get('no_exists', 'flong'), 'flong')

    def test_all(self):
        d = PermissiveDict({'A': 1, 'a': 22, 'A B': 2, 'b': 3, 4: 4, 'lab': 'woof!'})
        # three key values
        self.assertEqual({1, 22, 4}, set(d.all('a,4,8')))
        self.assertEqual({'a', 'A', 4, 'A B'}, set(d.all('a,4,a-b', keys=True)))
        # upper and lower case a
        self.assertEqual({1, 22}, set(d.all('a')))
        self.assertEqual({'a', 'A'}, set(d.all('a', keys=True)))
        # nothing
        self.assertEqual([], d.all('and,400'))

    def test_convert_list(self):
        test_length = 20
        dicts = [{k: str(k)} for k in range(test_length)]

        p_dicts = PermissiveDict.convert_list(dicts)
        self.assertEqual(len(dicts), len(p_dicts))

        for z in range(test_length):
            self.assertEqual(dicts[z][z], p_dicts[z][z])
            self.assertEqual(dicts[z][z], p_dicts[z].get(z))
            self.assertEqual(dicts[z][z], p_dicts[z](z))
