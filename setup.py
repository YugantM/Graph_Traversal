from distutils.core import setup
setup(
  name = 'ggraph',         
  packages = ['ggraph'],   
  version = '1.0',      
  license='MIT',        
  description = 'This package returns topological list of packages from the current directory.',   
  url = 'https://github.com/YugantM/Graph_Traversal',   
  download_url = 'https://github.com/YugantM/Graph_Traversal.git',
  entry_points = {
              'console_scripts': ['add = add.__main__:main',],
              },
  scripts=['scripts/add'],  
  keywords = ['addition', 'calculation'],  
  
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)