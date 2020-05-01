import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="charm-k8s-graylog",
    version="0.1.0",
    author="Peter De Sousa",
    author_email="peter.de.sousa@canonical.com",
    description="Kubernetes Charm for graylog",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VariableDeclared/charm-k8s-graylog",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
