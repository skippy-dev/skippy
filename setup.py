import setuptools
import skippy

with open('requirements.txt') as f:
  requirements = f.read().splitlines()

with open('README.md', encoding="utf8") as f:
    readme = f.read()

setuptools.setup(
    name='skippy-pad',
    version=skippy.__version__,
    description='Simple. Comfortable. Powerful. notepad for www.scpwiki.com.',
    long_description=readme,
    long_description_content_type="text/markdown",
    url='https://github.com/skippy-dev/skippy/',
    author='MrNereof',
    author_email='mrnereof@gmail.com',
    python_requires='>=3.4',
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'],
    keywords=['scp', 'wikidot', 'pyscp', 'skippy'],
    packages=['skippy', 'skippy.plugins', 'skippy.utils', 'skippy.assets',],
    install_requires=requirements,
    package_dir={'skippy': 'skippy'},
    package_data={'skippy': ['assets/*.*','assets/dark/*.*','assets/light/*.*']},
    entry_points={
          'console_scripts': [
              'skippy = skippy.__main__:run',
          ],
      },
)
