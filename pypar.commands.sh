#!/usr/bin/env bash
# Notes and commands to upload to pypi
#
# https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56
# https://pypi.org/project/twine/
#
# https://python-packaging.readthedocs.io/en/latest/non-code-files.html
# edit setup.py
# to update the version

. venv37/bin/activate

# setup first

pip install setuptools
pip install wheel
pip install twine

# on each release

python setup.py sdist bdist_wheel
twine check dist/permissive_dict-1.0.3*
twine upload dist/permissive_dict-1.0.3* -u martlark
