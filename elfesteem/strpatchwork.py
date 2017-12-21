from array import array
from sys import maxsize


class StrPatchwork:

    def __init__(self, s="", paddingbyte="\x00"):
        s_raw = str(s)
        val = array("B")
        val.fromstring(s_raw)
        self.s = val
        # cache s to avoid rebuilding str after each find
        self.s_cache = s_raw
        self.paddingbyte = paddingbyte

    def __str__(self):
        return self.s.tostring()

    def __getitem__(self, item):
        s = self.s
        if type(item) is slice:
            end = item.stop
            l = len(s)
            if l < end and end != maxsize:  # XXX hack [x:] give 2GB limit
                # This is inefficient but avoids complicated maths if step is
                # not 1
                s = s[:]

                tmp = array("B")
                tmp.fromstring(self.paddingbyte * (end - l))
                s.extend(tmp)
            r = s[item]
            return r.tostring()

        else:
            if item > len(s):
                return self.paddingbyte
            else:
                return chr(s[item])

    def __setitem__(self, item, val):
        if val == None:
            return
        val_array = array("B")
        val_array.fromstring(str(val))
        if type(item) is not slice:
            item = slice(item, item + len(val_array))
        end = item.stop
        l = len(self.s)
        if l < end:
            tmp = array("B")
            tmp.fromstring(self.paddingbyte * (end - l))
            self.s.extend(tmp)
        self.s[item] = val_array
        self.s_cache = None

    def __repr__(self):
        return "<Patchwork %r>" % self.s.tostring()

    def __len__(self):
        return len(self.s)

    def __contains__(self, val):
        return val in str(self)

    def __iadd__(self, other):
        tmp = array("B")
        tmp.fromstring(str(other))
        self.s.extend(tmp)
        return self

    def find(self, pattern, start=0, end=None):
        if not self.s_cache:
            self.s_cache = self.s.tostring()
        return self.s_cache.find(pattern, start, end)

    def rfind(self, pattern, start=0, end=None):
        if not self.s_cache:
            self.s_cache = self.s.tostring()
        return self.s_cache.rfind(pattern, start, end)
