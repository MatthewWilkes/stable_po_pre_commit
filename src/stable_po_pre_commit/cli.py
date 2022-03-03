import glob
from os import rename
import os.path
import time
import typing as t
import click
from babel.messages import frontend

CommandLineInterface = frontend.CommandLineInterface

HEADER = """
msgid ""
msgstr ""

"""


def skipping_rename(*args, **kwargs):
    """If something has already moved the file out of the way then babel assumes it's on windows and does a non-atomic
    move, which deletes the original file. This makes failed renames equal a no-op"""
    try:
        return rename(*args, **kwargs)
    except FileNotFoundError:
        return


def readd_header(po_path):
    with open(po_path, "r+", encoding="utf-8") as po_file:
        original_data = po_file.read()
        po_file.seek(0)
        po_file.write(HEADER)
        po_file.write(original_data)


@click.command()
@click.argument("files", nargs=-1)
@click.option("-o", "--output-file")
@click.option("-s", "--strip-comments")
@click.option("-F", "--mapping-file")
def main(
    files: t.List[str],
    output_file: t.Optional[str],
    strip_comments: t.Optional[str],
    mapping_file: t.Optional[str],
) -> None:
    frontend.os.rename = skipping_rename
    cli = CommandLineInterface()
    args = [
        "pybabel",
        "extract",
        "--no-location",
        "--omit-header",
        "--no-wrap",
        "--sort-output",
        "-k",
        "lazy_gettext",
        "-c",
        "BABEL:",
    ] + list(files)
    if output_file:
        args += ["-o", output_file]
    if strip_comments:
        args += ["-s", strip_comments]
    if mapping_file:
        args += ["-F", mapping_file]

    cli.run(args)

    if output_file:
        translations_dir = os.path.join(output_file, "..", "translations")
        translations_dir = os.path.abspath(translations_dir)
        args = [
            "pybabel",
            "update",
            "--ignore-obsolete",
            "--no-wrap",
            "--omit-header",
            "--no-fuzzy-matching",
            "-i",
            output_file,
            "-d",
            translations_dir,
        ]
        print(args)
        cli = CommandLineInterface()
        cli.run(args)

    # Add blank header to prevent being seen as fuzzy
    for po_path in glob.glob(f"{translations_dir}/**/*.po", recursive=True):
        readd_header(po_path)
