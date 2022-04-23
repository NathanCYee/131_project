from setuptools import setup

tests_require = [
    'pytest'
]

setup(
    name='e-buy',
    version='0.0.1',
    packages=['app'],
    install_requires=['pytest', 'Flask', 'flask-wtf', 'flask-sqlalchemy', 'flask-login'],
    extras_require={
        'test': tests_require
    },
)
