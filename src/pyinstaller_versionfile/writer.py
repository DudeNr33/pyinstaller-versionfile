"""
Logic for writing the output file.
"""

import codecs
import os

from jinja2 import Template
from jinja2.exceptions import UndefinedError

from pyinstaller_versionfile.exceptions import InternalUsageError, UsageError

TEMPLATE_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "version_file_template.txt")


class Writer(object):
    """
    Creates the output file.
    """
    NECESSARY_PARAMETERS = (
        "Version",
        "CompanyName",
        "FileDescription",
        "InternalName",
        "LegalCopyright",
        "OriginalFilename",
        "ProductName",
    )

    def __init__(self, metadata):
        self.metadata = metadata
        self._content = None

    def render(self):
        """
        Render the content of the output file.
        """
        data = self.metadata.to_dict()
        if any(param not in data for param in self.NECESSARY_PARAMETERS):
            raise InternalUsageError("Not all necessary parameters provided by MetaData.to_dict()")

        with codecs.open(TEMPLATE_FILE, encoding="utf-8") as infile:
            template = Template(infile.read())
        try:
            self._content = template.render(**data)
        except UndefinedError as err:
            raise InternalUsageError(
                "Could not render template because parameters are missing (jinja2 UndefinedError)."
            ) from err

    def save(self, filepath):
        """
        Save the rendered outfile to disk.
        """
        if not self._content:
            raise InternalUsageError("Called Writer.save() before calling Writer.render()")
        if os.path.isdir(filepath):
            raise UsageError("You must specify a file to save the output. Received a directory name instead.")
        with codecs.open(filepath, "w", encoding="utf-8") as file_handle:
            file_handle.write(self._content)
