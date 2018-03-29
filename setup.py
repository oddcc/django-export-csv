from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)

setup(
    name='django-export-csv',
    version='0.1.3.1',
    keywords=['django', 'csv', 'export', 'queryset'],
    description='A CSV exporter for Django, this tool create a shortcut to render a queryset to a CSV steaming HTTP response.',
    license='MIT License',
    long_description=open('README.md').read(),
    author='oddcc',
    author_email='skycc71640@gmail.com',
    url='https://github.com/oddcc/django-export-csv',
    install_requires=[
        'django>=1.8.8, <2.0',
        'unicodecsv>=0.14.1',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Environment :: Plugins",
        "Framework :: Django",
        "License :: OSI Approved :: GNU General Public License (GPL)"
    ],
    packages=find_packages(exclude=('tests',)),
    tests_require=[
        'tox',
    ],
    cmdclass={'test': Tox},
)
