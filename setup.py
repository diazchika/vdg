# setup.py
import vdg
from setuptools import setup, find_packages
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="vdg",
    version=vdg.__version__,
    author="diazchika",
    author_email="halberd-civic.0c@icloud.com",
    description="VCB-Studio Draft Generator 发布稿生成器",
    long_description=read('README.md'),
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'vdg': ['templates/*.jinja', 'templates/form.yml'],
    },
    entry_points={
        'console_scripts': [
            'vdg = vdg.main:main',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    project_urls={
        'github': 'https://github.com/diazchika/vdg',
    }
)
