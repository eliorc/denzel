from setuptools import setup, find_packages
import denzel

setup(
    name='denzel',
    version=denzel.__version__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'docker'
    ],
    entry_points='''
        [console_scripts]
        denzel=cli.scripts.cli:cli
    ''',
)