#!/usr/bin/env python3
import sys

if not __package__:
    import os

    # Make CLI runnable from source tree with
    # > python package
    package_source_path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, package_source_path)

    from protocol.cli import main  # type: ignore

    sys.exit(main())

from .cli import main

sys.exit(main())
