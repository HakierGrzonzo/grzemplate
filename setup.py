import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = "grzemplate",
    version = "0.0.1",
    author = "Grzegorz Koperwas",
    author_email = "admin@grzegorzkoperwas.site",
    description = "Yet another static site generator",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/HakierGrzonzo/grzemplate',
    packages=setuptools.find_packages(),
    python_requires='>=3.8'
)
