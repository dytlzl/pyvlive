from setuptools import setup, find_packages


setup(
    name='vlive_api',
    version="0.0.1",
    description="API of VLIVE",
    long_description="Scraping Tool of VLIVE(https://www.vlive.tv/)",
    url='https://github.com/mcgela/vlive_scraper',
    author='MC Gela',
    license='MIT',
    classifiers=[
        "Topic :: Utilities"
    ],
    keywords='VLIVE',
    install_requires=[
        "requests"
    ]
)