from setuptools import setup, find_packages

setup(
    name='oidc-auth',
    version='0.1.0',
    packages=find_packages(include=['oidc_auth', 'oidc_auth.*']),
    tests_require=['pytest'],
    setup_requires=['flake8'],
    install_requires=[
        ],
    entry_points={
        'console_scripts': [
            'oidc-auth=oidc_auth.cli:main',
        ]
    }
)
