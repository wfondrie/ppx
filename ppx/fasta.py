"""
Download Uniprot FASTA files, optionally appending decoy
sequences.
"""
import urllib.request
import logging
import os
import shutil

class _UniprotFasta:
    """A base class for the Uniprot classes"""
    def __init__(self,
                 out_file,
                 append_decoys=True,
                 enzyme="trypsin",
                 decoy_prefix="decoy_",
                 reverse=False,
                 seed=42):
        """Initialize a _UniprotFasta"""
        self.url = "https://www.uniprot.org/uniprot/?query="
        self.out_file = out_file
        self.append_decoys = append_decoys
        self.enzyme = enzyme
        self.decoy_prefix = decoy_prefix
        self.reverse = reverse
        self.seed = seed
        self.targets = None
        self.decoys = None

    def add_decoys(self):
        pass


class UniprotProteome(_UniprotFasta):
    """Retrieve a set of protein sequence from Uniprot in FASTA format.

    Parameters
    ----------
    organism : int or {"human", "yeast", "mouse"}
        The proteome to retrieve. This may either be the Uniprot organism
        identifier, or the one of several common organism names.
    isoforms : bool
        Include isoforms or only retrieve conical sequences.
    """
    def __init__(self,
                 organism,
                 out_file,
                 append_decoys=True,
                 enzyme="trypsin",
                 decoy_prefix="decoy_",
                 reverse=False,
                 seed=42):
        """Initialize a UniprotProteome."""
        super().__init__(out_file=out_file,
                         append_decoys=append_decoys,
                         enzyme=enzyme,
                         decoy_prefix=decoy_prefix,
                         reverse=reverse,
                         seed=seed)
