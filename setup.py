try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
 
setup(
    name='coolsms_python_sdk',
    version='2.0.3', 
    packages=['sdk', 'sdk/api'], 
	package_dir={'sdk': 'sdk', 'api': 'sdk/api'},
    license='BSD License',
    author='Nurigo',
    author_email='sms-team@nurigo.net',
    url='https://github.com/coolsms/python-sdk',
	download_url = 'https://github.com/coolsms/python-sdk/releases',
    description='Send Message, Kakao Alimtalk and Management Message using Python and REST API.',
    keywords=['sms', 'rest', 'restapi', 'restsms', 'smsrest', 'coolsms', 'nurigo', 'python sdk', 'alimtalk', 'kakao'],
    classifiers=[
		'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
