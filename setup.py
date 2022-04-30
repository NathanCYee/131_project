from setuptools import setup

tests_require = [
    'pytest'
]

setup(
    name='e-buy',
    version='0.0.1',
    packages=['gigastore', 'app'],
    install_requires=['pytest', 'pytest-cov', 'Flask', 'flask-wtf', 'flask-sqlalchemy', 'flask-login', 'WTForms',
                      'SQLAlchemy', 'email_validator'],
    extras_require={
        'test': tests_require
    }
)
