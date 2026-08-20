from .keyshort import KeyShort

class ManagerKeyShort:

    """
    Manages a collection of KeyShorts, allowing for their registration, 
    deregistration, retrieval, and status updates.
    """

    def __init__(self):
        self._keys_short: dict[str, KeyShort] = {}

    def register(self, *keys_short: KeyShort):

        """ Registry one or more new KeyShorts. """

        for key in keys_short:
            if key.tag in self._keys_short:
                raise KeyError(f"Key {key.tag!r} has existed") 
            self._keys_short[key.tag] = key 

    def unregister(self, *keys_short: KeyShort):

        """ Unregistry one or more new KeyShorts. """

        for key in keys_short:
            if key.tag not in self._keys_short:
                raise KeyError(f"Key {key.tag!r} has not existed") 
            self._keys_short.pop(key.tag)

    def get_keys_short(self) -> dict[str, KeyShort]:

        """ Return all stored KeyShorts. """
        return self._keys_short

    def get(self, name: str) -> KeyShort:

        """ Return a specific KeyShort through `name`. """

        if name not in self._keys_short:
            raise KeyError(f"Key {name!r} has not existed")
        return self._keys_short[name]

    def update(self):

        """ Check and trigger the callbacks of all managed KeyShorts. """

        for key_short in self._keys_short.values():
            key_short.active()