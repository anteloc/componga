# Usage:
# res = []
# to_keypaths({'a': {'b': {'c': 1, 'd': 2}, 'e': 3}, 'f': 4}, keypaths=res)
# print(f"res: {res}")
# Result:
# res: [(['a', 'b', 'c'], 1), (['a', 'b', 'd'], 2), (['a', 'e'], 3), (['f'], 4)]
def to_keypaths(adict, stack=[], keypaths=[]):
    for key, value in adict.items():
        stack.append(key)
        if isinstance(value, dict):
            to_keypaths(value, stack, keypaths)
        else:
            keypaths.append((stack.copy(), value))
        stack.pop()
