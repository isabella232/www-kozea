from setuptools import find_packages, setup

tests_requirements = [
    'pytest',
    'pytest-cov',
    'pytest-flake8',
    'pytest-isort',
]

setup(
    name="kozea",
    version="0.1.dev0",
    description="Website for Kozea",
    url="https://www.kozea.fr",
    author="Kozea",
    packages=find_packages(),
    include_package_data=True,
    scripts=['kozea.py'],
    install_requires=[
        'Flask',
        'mandrill-37',
        'libsass',
    ],
    tests_require=tests_requirements,
    extras_require={'test': tests_requirements}
)