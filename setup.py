import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simple-kube-marosmola",
    version="0.0.1",
    author="marosmola",
    author_email="ssmolenm@gmail.com",
    description="Simplify kubernetes-client library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marosmola/simple-kube",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)