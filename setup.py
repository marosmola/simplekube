from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="simplekube",
    version="0.0.8",
    author="marosmola",
    author_email="ssmolenm@gmail.com",
    description="Simplify kubernetes-client library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marosmola/simplekube",
    packages=find_packages(),
    package_data={'simplekube': ['templates/*.j2']},
    install_requires=[
        "Jinja2==2.11.1",
        "kubernetes==11.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)