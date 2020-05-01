#!/usr/bin/env python3

import hashlib


def sha256_string(string):
    m = hashlib.sha256()
    m.update(str.encode(string))
    return m.digest().hex()
