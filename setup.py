from setuptools import setup

tests_require = [
    'pytest',
    'pytest-cov'
]

setup(
    name='e-buy',
    version='0.0.1',
    packages=['app'],
    install_requires=['pytest', 'pytest-cov', 'Flask', 'flask-wtf', 'flask-sqlalchemy', 'flask-login', 'WTForms==2.3.3',
                      'SQLAlchemy', 'email_validator'],
    extras_require={
        'test': tests_require
    },
)