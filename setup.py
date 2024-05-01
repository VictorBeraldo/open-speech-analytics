from setuptools import setup, find_packages

setup(
    name='open_speech_analytics',
    version='0.1',
    package_dir={'': 'src'},  # Indica que os pacotes estão dentro de 'src'
    packages=find_packages(where='src'),  # Descobre todos os pacotes dentro de 'src'
)