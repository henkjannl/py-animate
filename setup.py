from distutils.core import setup

'''
Create a windows installer by calling from the command line:

python setup.py bdist_wininst

See also:
	http://docs.python.org/2/distutils/builtdist.html
'''

setup(name='Animate',
	version='2.00',
	py_modules=['Animate', 'Animate.Animate', 'Animate.Scripts', 
		'Animate.Constants', 'Animate.Items', 'Animate.Properties', 
		'Animate.DirectoryList'] )
