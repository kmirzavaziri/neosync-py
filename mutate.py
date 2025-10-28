import ctypes


class MutateResult(ctypes.Structure):
    _fields_ = [
        ("result", ctypes.c_char_p),
        ("error", ctypes.c_char_p)
    ]


lib = ctypes.CDLL("./neosync_exporter/main.so")
lib.Mutate.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
lib.Mutate.restype = MutateResult


class MutateException(Exception):
    pass


def mutate(js_code, value):
    result_struct = lib.Mutate(js_code.encode('utf-8'), str(value).encode('utf-8'))
    result = result_struct.result.decode('utf-8') if result_struct.result else ''
    err = result_struct.error.decode('utf-8') if result_struct.error else ''
    if err:
        raise MutateException(err)
    return result
