#!/usr/bin/env python3
import atheris
import sys

from construct import ConstError, StreamError
import struct

import fuzz_helpers

with atheris.instrument_imports():
    from regipy.registry import RegistryHive

ctr = 0
def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    global ctr
    ctr += 1
    try:
        with fdp.ConsumeTemporaryFile(suffix='.dat', all_data=True, as_bytes=True) as f:
            reg = RegistryHive(f)
        reg.recurse_subkeys(as_json=fdp.ConsumeBool())
    except (ConstError, UnicodeDecodeError, StreamError):
        return -1
    #except (struct.error, StopIteration) as e:
     #   if ctr > 100:
      #      raise e
       # return -1

def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
