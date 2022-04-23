from setuptools import setup

tests_require = [
    'pytest'
]

setup(
    name='e-buy',
    version='0.0.1',
    packages=['e-buy'],
    requires=['pytest', 'pytest-cov', 'flask', 'flask-wtf', 'flask-sqlalchemy', 'flask-login'],
    extras_require={
        'test': tests_require
    }
)
