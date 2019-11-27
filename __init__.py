class PermissiveDict(dict):
    """
    a dictionary class with loose rules for returning
    attribute or requested_key values.  Note: may resort to iterating the dict values
    to find the matching requested_key, so is potentially slow.

    Spaces, underscores and dashes are equivalent in a requested_key.

    Items in the list can be retrieved by, get, attribute_access or array requested_key

    example:
    a = PermissiveDict({'A': 1, 'A B': 2, 'b': 3, 4: 4})
    a.get('A_b') == a['a_b'] == a['A b'] == a['A_B'] a['a-b '] == a.a_b == a.A_b

    Items with multiple confused keys may return the first item found.

    """

    def __init__(self, kwargs):
        self.__map_fields = {}
        self.__default_returned = False
        return super().__init__(kwargs)

    def __getattr__(self, name):
        try:
            value = super().__getattr__(name)
            return value
        except AttributeError:
            return self.get(name)

    def __getitem__(self, name):
        try:
            value = super().__getitem__(name)
            return value
        except KeyError:
            return self.get(name)

    def __contains__(self, item):
        self.get(item)
        return not self.__default_returned

    def get(self, key, default=''):
        """
        return the value in dict d which matches the key
        using a str and upper comparision.  Tries normal get
        first.  Then a miscellany of common punctuation characters

        Use a comma to try a number of different keys for the same thing.

        :param key: key to find, converts to str
        :param default: default value if not found.  NOTE: unlike Python uses '' as the default
        :return: the value found or default if not found
        """
        self.__default_returned = False
        value = super().get(key)
        if value:
            return value

        requested_keys = str(key).upper().strip()
        for requested_key in [r for r in requested_keys.split(',') if len(r) > 0]:
            for r in [('', ''), ('_', ' '), (' ', '_'), (' ', '-'), ('-', ' '), (' ', '.'), ('.', ' ')]:
                value = super().get(requested_key.replace(*r))
                if value:
                    # print(f'short cut: {requested_key}')
                    return value

                for k, v in self.items():
                    match_key = str(k).replace(*r).upper().strip()
                    if match_key == requested_key:
                        # print(f'iterated: {requested_key}')
                        return v

        return self.__get_map_value__(key, default)

    @classmethod
    def convert_list(cls, items):
        return [PermissiveDict(item) for item in items]

    def set_map(self, map_fields):
        self.__map_fields = map_fields

    def __get_map_value__(self, key, default=''):
        """
        return value using map keys to map multiple keys to a tight requested_key
        example:

        d = PermissiveDict(a=1, b=2, q=3,z=4)
        d.set_map(dict(tree=['z','y','t']))
        d.tree == 4
        :param key: item to match
        :return: the value
        """
        map_keys = self.__map_fields.get(key)
        if not map_keys:
            self.__default_returned = True
            return default

        for k in map_keys:
            value = super().get(k, None)
            if value:
                return value

        self.__default_returned = True
        return default


if __name__ == '__main__':
    old_d = dict({'A': 1, 'A B': 2, 'b': 3, 4: 4, 'lab': 'woof!'})
    d = PermissiveDict(old_d)
    assert d.get('a') == d.get('A') == 1
    assert d.a_b == d.get('A_b') == 2
    assert d.get('B') == 3
    assert d.a == d.A == 1
    assert d.q == ''
    assert d['a'] == d['A'] == d['A '] == d[' a '] == 1
    assert d[' a-b '] == d['A-b '] == d[' a_b '] == d[' a.b '] == 2
    assert ' a_b ' in d
    assert 'A' in d
    assert 'a' in d
    assert 'q' not in d
    assert '4' in d
    assert 4 in d
    assert d.get(4) == d.get('4') == 4
    assert d.flong == d['flong'] == d.get('flong') == d.get('pling,plong,,') == ''
    assert d['flong,A'] == d.get('plok,a') == d.a

    # dog key could resolve using the dog, puppy, pupper or lab key
    d.set_map(dict(dog=['puppy', 'pupper', 'lab']))
    assert d.dog == d['dog'] == d.get('dog') == 'woof!'
