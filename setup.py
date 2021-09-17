from setuptools import setup

setup(
    name='turinglab',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
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