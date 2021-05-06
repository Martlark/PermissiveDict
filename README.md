# PermissiveDict

Dictionary class with loose rules for returning an attribute or a requested key value.  
--------------------------------------------------------------------------------------
    
Note: may resort to iterating the dict values to find the matching requested key, so is potentially slow.

Key is first directly found using the exact key, and then loose rules are used.

Installing
----------

    pip install permissive-dict

Key Search Rules:
-----------------

1. Keys compared without regard to case.
2. Spaces, underscores, full-stops and dashes are equivalent in a requested key.
3. Requested key is converted to str and stripped for wild card searching.
4. Items in the list can be retrieved by, get, attribute_access, call or array requested_key.
5. First matching element is returned.
6. Default of '' is used instead of dict standard None or raising KeyError
7. Multiple keys can be supplied separated with , (comma)
        
Example:
        
        from permissive_dict import PermissiveDict
        
        a = PermissiveDict({'A B': 2, 4: 4})
        a.get('A_b') == a['a_b'] == a['A b'] == a['A_B'] == a['a-b '] == a['a.b '] == a.a_b == a.A_b == a('a-b')
        
        a.get('blue,4') == 4
        
        a.get('4') == a[4] == a(4) == a('4')

Items with multiple wildcard keys matching in the dictionary will return the first item found.

Keys can be accessed as attributes, array index, get() or by calling the instance variable.

Key and value can be set as an attribute.
-----------------------------------------

Example:

    a = PermissiveDict()
    a.hello = 4
    a.hello == a['hello'] == a('hello') == a.get('HellO')

Converting an entire list of dicts
----------------------------------

An entire list of dictionaries can be converted to PermissiveDict using
the `convert_list` method.  NOTE: no deep conversion is done and child 
dictionaries are not converted.

Example:

    list_of_dicts = [dict(a=n) for n in range(10)]
    permissive_list = PermissiveDict.convert_list(list_of_dicts)

Notes
-----

Only Python 3 is supported.

Release history
---------------
1.0.4 Fix missing handling of _ and -
