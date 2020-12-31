"""setup script for data analyze tool, please run 'python setup.py install' before using analyze
"""
from setuptools import setup

if __name__ == "__main__":
    requirements = [
        'matplotlib', 'jieba', 'numpy', 'xlrd', 'pandas', 'openpyxl'
    ]
    setup(name='data_process_tool',
          version='0.0.1',
          install_requires=requirements)
