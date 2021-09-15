from setuptools import setup

setup(
    name='turinglab',
    version='0.1.0',
    author='Maxim Slipenko',
    packages=['turinglab'],
    install_requires = [
        'python-docx'
    ],
    entry_points = {
        'console_scripts': [
            'turinglab = turinglab.__main__:main'
        ]
    }
)