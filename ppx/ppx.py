"""The command line entry point for ppx"""
import sys
import logging
from pathlib import Path
from argparse import ArgumentParser

from . import __version__
from . import find_project

LOGGER = logging.getLogger(__name__)


def get_parser():
    """Parse the command line arguments"""
    desc = f"""Use this command line utility to download files from the PRIDE and MassIVE
    proteomics repositories. The paths to the downloaded files are written to
    stdout."""

    epilog = "More documentation and examples at: https://ppx.readthedocs.io"
    parser = ArgumentParser(description=desc, epilog=epilog)

    parser.add_argument(
        "identifier",
        type=str,
        help=(
            "The ProteomeXchange, PRIDE, or MassIVE identifier for the "
            "project."
        ),
    )

    parser.add_argument(
        "files",
        type=str,
        nargs="*",
        help=(
            "One or more files to download. If none are provided, all files "
            "associated with the project are downloaded. Unix-style glob "
            "wildcards can be used, but they will need to be enclosed in "
            "quotation marks so as not to match files in your current "
            "working directory."
        ),
    )

    parser.add_argument(
        "-l",
        "--local",
        type=str,
        help=(
            "The local directory where data will be downloaded. The default "
            "is ~/.ppx/<identifier>. This can also be changed globally by "
            "setting the PPX_DATA_DIR environment variable to your desired "
            "location."
        ),
    )

    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        help="The maximum amount of time to wait for a server response.",
    )

    parser.add_argument(
        "-f",
        "--force",
        default=False,
        action="store_true",
        help=(
            "Should ppx download files that are already present in the local "
            "data directory?"
        ),
    )

    parser.add_argument(
        "--version",
        action="version",
        help="Get the version of ppx.",
        version="%(prog)s " + __version__,
    )

    return parser


def main():
    """Run ppx"""
    logging.basicConfig(
        level=logging.INFO, format="[%(levelname)s]: %(message)s"
    )

    parser = get_parser()
    args = parser.parse_args()
    proj = find_project(args.identifier, args.local, timeout=args.timeout)
    remote_files = proj.remote_files()

    if len(args.files) > 0:
        matches = set()
        passed = []
        for pat in args.files:
            pat_match = set(f for f in remote_files if Path(f).match(pat))
            passed.append(bool(pat_match))
            matches.update(pat_match)

        if not all(passed):
            failed = "  \n".join(
                [f for f, p in zip(args.files, passed) if not p]
            )

            raise FileNotFoundError(
                "Unable to find one or more of the files or patterns:"
                f"\n  {failed}"
            )

    else:
        matches = remote_files

    LOGGER.info(
        "Downloading %i files from %s...", len(matches), args.identifier
    )
    downloaded = proj.download(matches)

    for local_file in downloaded:
        sys.stdout.write(str(local_file) + "\n")

    LOGGER.info("DONE!")


if __name__ == "__main__":
    main()
