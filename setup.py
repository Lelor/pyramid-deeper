from setuptools import setup


requires = [
    'marshmallow',
    'pyramid',
    'pyramid_jinja2',
    'pymongo',
    'waitress'
]


dev_requires = [
    'pyramid_debugtoolbar',
    'webtest'
]

setup(
    name='deeper',
    install_requires=requires,
    extras_require={
        'dev': dev_requires
    },
    entry_points={
        'paste.app_factory': [
            'main = app:main'
        ],
    },
)