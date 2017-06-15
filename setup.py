from setuptools import setup, find_packages

setup(
    name='django-export-csv',
    version='0.1.2',
    keywords=['django', 'csv', 'export', 'queryset'],
    description='a CSV exporter for Django',
    license='MIT License',
    long_description=open('README.md').read(),
    author='oddcc',
    author_email='skycc71640@gmail.com',
    url='https://github.com/oddcc/django-export-csv',
    install_requires=[
        'django>=1.8.8',
        'unicodecsv>=0.14.1'
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Environment :: Plugins",
        "Framework :: Django",
        "License :: OSI Approved :: GNU General Public License (GPL)"
    ],
    packages=find_packages(exclude=('demo_app',)),
)