from setuptools import setup, find_packages
if __name__ == "__main__":
    setup(
        name="Protomix",
        version="1.0.0",
        packages=find_packages(),
        install_requires=[
            'numpy',
            'pandas',
            'scipy',
            'plotly',
            
        ],
        # Metadata for the package
        author="Mohammed Zniber",
        author_email="zniber1995@gmail.com",
        description="A Python package for NMR preprocessing",
        long_description=open('README.md').read(),
        long_description_content_type="text/markdown",
        license="MIT",
        keywords="NMR, Preprocessing, metabolomics, serum, urine",
        url="https://github.com/mzniber/protomix",
    )
