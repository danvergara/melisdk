from setuptools import find_packages, setup

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='melisdk',
    version="0.1.3",
    description='A copy of MercadoLibre python SDK, but works',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Daniel Omar Vergara Pérez",
    packages=find_packages(exclude=("tests",)),
    author_email="daniel.omar.vergara@gmail.com",
    url='https://github.com/dany2691/melisdk',
    license='MIT',
    install_requires=[
        'requests>=2.22.0'
    ],
    classifiers=[        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'])
