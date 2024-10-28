from setuptools import setup, find_packages

setup(
    name="pdf_image_handler",
    version="0.1.0",
    license="GNU General Public License",
    author="fcasalen",
    author_email="fcasalen@gmail.com",
    description="library to convert pdf to iamges",
    packages=find_packages(),
    include_package_data=True,
    install_requires=open('requirements.txt').readlines(),
    long_description=open("README.md").read(),
    classifiers=[
        "Development Status :: 5 - Prodution/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11"
    ]
)
