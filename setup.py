from setuptools import setup

tests_require = [
    'pytest'
]

setup(
    name='gigastore',
    version='0.0.1',
    packages=['gigastore'],
    requires=['pytest', 'flask', 'flask-wtf', 'flask-sqlalchemy', 'flask-login'],
    extras_require={
        'test': tests_require
    }
)
