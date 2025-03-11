from setuptools import setup, find_packages

setup(
    name="zteradb",
    version="1.0.3",
    packages=find_packages(),
    install_requires=[],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='ZTeraDB',
    author_email='iashokin@gmail.com',
    description="ZTeraDB is a Python client library designed to simplify interactions with ZTeraDB."
                "It provides a set of classes and tools that enable seamless integration, allowing developers to "
                "easily manage database operations and queries.",
    url='https://github.com/zteradb/zteradb-python.git',
    tests_require=["unittest"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    license='ZTeraDB',
)

