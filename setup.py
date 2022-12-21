import setuptools
import glob

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cloudflare-sync",
    version="0.0.1",
    author="German Yepes",
    author_email="geryepes@gmail.com",
    description="DNS records sync with cloudflare",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    project_urls={
        "Bug Tracker": "",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=glob.glob("src/bin/*"),
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src", exclude=["tests"]),
    python_requires=">=3.6",
    install_requires=['cloudflare'],
)