"""
generate_data.py — backward-compatibility shim.

The implementation has moved to lib/twin_primes/datasets/dubner_ball.py.
This file delegates to that module so existing direct invocations still work:

    python generate_data.py [LIMIT] [--non-witnesses] [--output PATH]
    python generate_data.py 500 > data.json
"""

if __name__ == "__main__":
    import runpy
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
    runpy.run_module('twin_primes.datasets.dubner_ball', run_name='__main__')
