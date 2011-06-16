import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name="openrdi",
    version="0.1",
    author="Ariel Nunez, Robert Soden",
    author_email="anunezgomez@worldbank.org",
    description="Code behind africa.openrdi.org",
    long_description=(read('README')),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: GeoNode',
        'License :: OSI Approved :: BSD',
    ],
    license="BSD",
    keywords="geonode django",
    url='https://github.com/GFDRR/openrdi',
    scripts = [
               'scripts/openrdi',
              ],
    packages=find_packages('.'),
    include_package_data=True,
    zip_safe=False,
)
