#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("requirements.txt", "r") as reqs:
    requirements = reqs.readlines()

setup(
    name="conn-trackr",
    version="0.0.1",
    description="Track new connections and block port scans",
    author="Philip Bove",
    install_requires=requirements,
    author_email="phil@bove.online",
    packages=find_packages(),
    scripts=["bin/conn-track"],
)