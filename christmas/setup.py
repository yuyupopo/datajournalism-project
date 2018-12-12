import os
import setuptools

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
README_FILE = os.path.join(CURR_DIR, "README.md")

with open(README_FILE, "r") as fh:
    long_description = fh.read()   # pylint: disable=C0103

setuptools.setup(
    name="christmas",
    version="0.0.1",
    author="hcid",
    author_email="hcid.snu.ac.kr",
    description="Christmas Place Analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache 2.0 License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['christmas=christmas:main'],
    },
    install_requires=[
        'numpy', 'nltk', 'beautifulsoup4', 'hypertools', 'matplotlib',
        'pandas', 'scikit-learn', 'seaborn', 'selenium'
    ]
)
