from setuptools import setup, find_packages
from glob import glob
import os

version = '0.2'

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

install_requires = open(os.path.join(here, 'requirements.txt')).read().splitlines()

setup_requires = [
        'nose',
        ]

tests_require = install_requires + [
        'coverage',
        ]

setup(
        name='tilebox',
        version=version,
        description='Tools for managing tiles',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python',
            'Topic :: Scientific/Engineering :: GIS',
        ],
        author='Tom Payne',
        author_email='twpayne@gmail.com',
        url='http://github.com/twpayne/tilebox',
        license='BSD',
        packages=find_packages(exclude=['tiles', 'tilebox.tests']),
        zip_safe=True,
        install_requires=install_requires,
        setup_requires=setup_requires,
        tests_require=tests_require,
        test_suite='tilebox.tests',
        scripts=glob('tb-*'),
        entry_points="""
        # -*- Entry points: -*-
        """,
        long_description=README,
        )
