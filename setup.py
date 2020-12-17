from setuptools import setup, find_packages 
 
#with open('requirements.txt') as f: 
#    requirements = f.readlines() 
 
long_description = '' 
  
setup( 
        name ='uphyloplot2', 
        version ='2.3',
        author ='Stefan Kurtenbach', 
        author_email ='stefan.kurtenbach@med.miami.edu',
        description ='', 
        long_description = long_description, 
        long_description_content_type ="text/markdown", 
        license ='MIT', 
        packages = find_packages(),
        entry_points = {
         'console_scriptS': [
             'uphyloplot2=uphyloplot2:main',
          ],
        },
        classifiers =[ 
            "Programming Language :: Python :: 3", 
            "License :: OSI Approved :: MIT License", 
            "Operating System :: OS Independent", 
        ], 
        keywords ='', 
        #install_requires = requirements, 
        zip_safe = False
) 
