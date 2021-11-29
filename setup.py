import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sensitivity_calculator_jtr6",
    version="0.0.1",
    author="J Ramasawmy",
    author_email="joanna.ramasawmy@stfc.ac.uk",
    description="Sensitivity calculator for AtLAST",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ukatc/AtLAST_sensitivity_calculator",
    project_urls={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6"
)