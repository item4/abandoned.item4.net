from setuptools import find_packages, setup

install_requires = {
    'django[argon2] >= 1.11.5',
    'django-timezone-field >= 2.0',
}

tests_require = {
    'mypy >= 0.521',
    'pytest >= 3.2.1',
}

extras_require = {
    'tests': tests_require,
    'lint': {
        'flake8 >= 3.4.1',
        'flake8-import-order >= 0.13',
    },
}

setup(
    name='innocent',
    version='0.0.0',
    description='innocent website',
    url='http://item4.net',
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extras_require,
)
