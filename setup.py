from setuptools import setup, find_packages

setup(
    name='oidc-auth',
    version='0.1.0',
    packages=find_packages(include=['oidc_auth', 'oidc_auth.*']),
    tests_require=['pytest'],
    setup_requires=['flake8'],
    install_requires=[
        'requests==2.28.1',
        'Flask==2.2.2',
        ],
    entry_points={
        'console_scripts': [
            'oidc-auth=oidc_auth.cli:main',
        ]
    }
)
