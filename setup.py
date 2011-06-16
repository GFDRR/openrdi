import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name="africa",
    version="0.1",
    author="Ariel Nunez",
    author_email="ingenieroariel@gmail.com",
    description="Code behind africa.openrdi.org",
    long_description=(read('README')),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: GeoNode',
        'License :: OSI Approved :: GNU Library or General Public License (GPL)',
    ],
    license="GPL 3",
    keywords="haitidata geonode django",
    url='https://github.com/GFDRR/africa',
    scripts = [
               'scripts/africa',
              ],
    packages=find_packages('.'),
    include_package_data=True,
    zip_safe=False,
)
