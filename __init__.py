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
        return not self.__default_returned__

    def get(self, key, default=''):
        """
        return the value in dict d which matches the key
        using a str and upper comparision.  Tries normal get
        first.

        :param key: key to return, converts to str
        :param default: default value if not found
        :return: the value found or default if not found
        """
        self.__default_returned__ = False
        value = super().get(key)
        if value:
            return value

        requested_key = str(key).upper().strip()
        for k, v in self.items():
            match_key = str(k).upper().strip()
            if match_key == requested_key:
                return v
            if match_key.replace('_', ' ') == requested_key:
                return v
            if match_key.replace(' ', '_') == requested_key:
                return v
            if match_key.replace(' ', '-') == requested_key:
                return v
            if match_key.replace('-', ' ') == requested_key:
                return v
        value = self.__get_map_value__(key, default)
        if value != default:
            return value
        self.__default_returned__ = True
        return default

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
            return default

        for k in map_keys:
            value = super().get(k, None)
            if value:
                return value

        return default


if __name__ == '__main__':
    d = PermissiveDict({'A': 1, 'A B': 2, 'b': 3, 4: 4, 'lab': 'woof!'})
    d.set_map(dict(dog=['puppy', 'pupper', 'lab']))
    assert d.get('a') == d.get('A') == 1
    assert d.get('A_b') == 2
    assert d.get('B') == 3
    assert d.a == 1
    assert d.A == 1
    assert d.a_b == 2
    assert d.q == ''
    assert d['a'] == 1
    assert d['A'] == 1
    assert d['A '] == 1
    assert d[' a '] == 1
    assert d[' a-b '] == 2
    assert d['A-b '] == 2
    assert d[' a_b '] == 2
    assert ' a_b ' in d
    assert 'A' in d
    assert 'a' in d
    assert 'q' not in d
    assert '4' in d
    assert d.get(4) == d.get('4') == 4
    assert d.dog == d['dog'] == d.get('dog') == 'woof!'
