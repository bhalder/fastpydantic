from setuptools import setup, find_packages

setup(
    name='fastpydantic',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'fastapi>=0.65.2',
        'uvicorn>=0.14.0',
        'sqlalchemy>=1.4.20',
        'pydantic>=1.8.2',
        'redis>=3.5.3',
        'aiohttp>=3.7.4'
    ],
    author='Barun Halder',
    author_email='barunhaldernvs@gmail.com',
    description='A library to auto-generate SQLAlchemy, Redis, and FastAPI code from Pydantic models',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/fastapi_auto',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Framework :: FastAPI',
    ],
    keywords='fastapi sqlalchemy pydantic redis',
)

