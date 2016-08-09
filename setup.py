try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
 
setup(
    name='coolsms_python_sdk',
    version='2.0', 
    packages=['sdk', 'api'], 
	package_dir={'sdk': 'sdk', 'api': 'sdk/api'},
    #package_data={'examples': ['examples/*']},
    license='MIT License',
    author='nurigo',
    author_email='sms-team@nurigo.net',
    url='https://github.com/coolsms/python-sdk',
    description='Send Message, Kakao Alimtalk, Message Management using PHP and REST API.',
    keywords=['sms', 'rest', 'restapi', 'restsms', 'smsrest', 'coolsms', 'nurigo', 'python sdk', 'alimtalk', 'kakao'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
