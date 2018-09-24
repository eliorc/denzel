from setuptools import setup, find_packages
from src import denzel

setup(
    name='denzel',
    version=denzel.__version__,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'Click',
        'docker'
    ],
    entry_points='''
        [console_scripts]
        denzel=denzel_cli.scripts.cli:cli
    ''',
)