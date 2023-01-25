import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aa-py-csv",
    author="Rudolf Byker",
    author_email="rudolfbyker@gmail.com",
    description="Utilities for working with CSV files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AutoActuary/aa-py-csv",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    use_scm_version={
        "write_to": "aa_py_csv/version.py",
    },
    setup_requires=[
        "setuptools_scm",
    ],
    install_requires=[
        "locate>=1.1.1,==1.*",
        "pandas>=1.3.1,==1.*",
        "pandasql>=0.7.3,==0.7.*",
    ],
    package_data={
        "": [
            "py.typed",
        ],
    },
)
