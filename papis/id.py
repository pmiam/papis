import hashlib
import random
from typing import Optional

import papis.document


def compute_an_id(doc: papis.document.Document,
                  seed: Optional[str] = None) -> str:
    """Make an id for the input document *doc*.

    This is a non-deterministic function if *separator* is *None* (a random value
    is used). For a given value of *separator*, the result is deterministic.

    :arg doc: a document for which to generate an id.
    :arg separator: a string used to separate the document fields that go into
        constructing the id.

    :returns: a (hexadecimal) id for the document that is unique to high probability.
    """

    seed = seed if seed is not None else str(random.random())

    digest = hashlib.md5()
    digest.update(seed.encode())

    for path in sorted(doc.get_files()):
        with open(path, "rb") as fd:
            digest.update(fd.read())

    return digest.hexdigest()


def key_name() -> str:
    """Reserved key name for databases and documents."""
    return "papis_id"


def has_id(doc: papis.document.DocumentLike) -> bool:
    """Check if the given *doc* has an id."""
    return key_name() in doc


def get(doc: papis.document.DocumentLike) -> str:
    """Get the id from a document."""
    key = key_name()

    if not has_id(doc):
        raise ValueError(
            "Papis ID key '{}' not found in document: '{}'"
            .format(key, papis.document.describe(doc)))

    return str(doc[key])
