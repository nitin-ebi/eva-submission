import glob
from distutils.core import setup
from os.path import join, abspath, dirname

base_dir = abspath(dirname(__file__))
requirements_txt = join(base_dir, 'requirements.txt')
requirements = [l.strip() for l in open(requirements_txt) if l and not l.startswith('#')]

setup(
    name='eva_submission',
    packages=['eva_submission', 'eva_submission.ENA_submission', 'eva_submission.xlsx'],
    package_data={'eva_submission': ['nextflow/*', 'etc/*']},
    version='0.5.8',
    license='Apache',
    description='EBI EVA - submission processing tools',
    url='https://github.com/EBIVariation/eva-submission',
    keywords=['ebi', 'eva', 'python', 'submission'],
    install_requires=requirements,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3'
    ],
    scripts=glob.glob(join(dirname(__file__), 'bin', '*.py'))
)
