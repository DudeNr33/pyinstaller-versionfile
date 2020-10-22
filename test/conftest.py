import os
import pytest
import tempfile


@pytest.fixture()
def temp_dir():
    tempdirobj = None
    try:
        tempdirobj = tempfile.TemporaryDirectory(dir=tempfile.gettempdir())
        dirname = tempdirobj.name
    except AttributeError:
        # Python 2.7 does not have tempfile.TemporaryDirectory
        dirname = tempfile.mkdtemp()
    yield dirname
    if tempdirobj:
        tempdirobj.cleanup()
    else:
        import shutil
        shutil.rmtree(dirname)


@pytest.fixture()
def temp_version_file(temp_dir):
    return os.path.join(temp_dir, "version_file.txt")
