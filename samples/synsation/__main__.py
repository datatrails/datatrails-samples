# pylint: disable=missing-docstring

import sys

from . import analyze
from . import charger
from . import initialise
from . import jitsuinator

# from . import multitenant
from . import wanderer


def main():
    key = sys.argv[1]
    del sys.argv[1]

    if key == "initialise":
        initialise.entry()
        sys.exit(0)

    if key == "analyze":
        analyze.entry()
        sys.exit(0)

    if key == "charger":
        charger.entry()
        sys.exit(0)

    if key == "jitsuinator":
        jitsuinator.entry()
        sys.exit(0)

    if key == "wanderer":
        wanderer.entry()
        sys.exit(0)

    sys.exit(1)


if __name__ == "__main__":
    # execute only if run as a script
    main()
