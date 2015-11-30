import sys

if __package__ is None and not hasattr(sys, "frozen"):
    # It is a direct call to __main__.py
    import os.path
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(os.path.dirname(path)))

import lmit

if __name__ == '__main__':
    print "Start LMIT"
    lmit.main()
