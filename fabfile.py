#!/usr/bin/env python
# encoding: utf-8

"""
fabfile.py

Created by Brant Faircloth on 09 October 2010 21:26 PDT (-0700).
Copyright (c) 2010 Brant C. Faircloth. All rights reserved.
"""

import os
import sys
import pdb
from fabric.api import *
from urlparse import urlparse
#from fabric.colors import green

SOURCE_DIRECTORY = '/home/bbox/src'

def check_for_source_directory():
    """ensure the directory that holds the source exists"""
    if not os.isdir(SOURCE_DIRECTORY):
        run('mkdir -p {0}'.format(SOURCE_DIRECTORY))
    else:
        pass
    
def _msg(message, color):
    """print a message in a color"""
    print(color(message))

def _update_path():
    run('export PATH=/usr/local/bin:$PATH')
    sudo('ln -s /usr/local/bin/python2.7 /usr/local/bin/python')
    print "Switched PATHs and symlinked python2.7"

def _apt_get(pkg):
    print 'Installing {}'.format(pkg)
    sudo('sudo apt-get install --no-install-recommends -q -y {0}'.format(pkg))

def _python_package_installer(package, flags, svn=False):
    if not svn:
        run('tar -xf {0}'.format(package))
        package_name = package.split('.')[0]
    else:
        package_name = package
    with cd('{0}*'.format(package_name)):
        if flags:
            run('python setup.py build {0}'.format(flags))
        else:
            run('python setup.py build')
        sudo('python setup.py install')
    return package_name

def _hash_checker(package, **kwargs):
    if kwargs['type'] == 'md5':
        local_md5 = run('md5sum {0}'.format(package)).split(' ')[0]
        if kwargs['hash'] == local_md5:
            return True
    elif kwargs['type'] == 'sha256':
        local_sha256 = run('sha256sum {0}'.format(package)).split(' ')[0]
        if kwargs['hash'] == local_sha256:
            return True
    else:
        return False

def svn(url, name, flags=None):
    with cd(SOURCE_DIRECTORY):
        package = name
        run('svn co {0} {1}'.format(url, name))
        package_name = _python_package_installer(package, flags, True)
    print "Installed {0}".format(package)


def source(url, flags=None, **kwargs):
    with cd(SOURCE_DIRECTORY):
        good_hash = None
        run('wget -q {0}'.format(url))
        package = os.path.basename(urlparse(url).path)
        #pdb.set_trace()
        if kwargs:
            good_hash = _hash_checker(package, **kwargs)
            if good_hash:
                 package_name = _python_package_installer(package, flags)
            else:
                 abort('Checksums do not match')
        elif not kwargs:
            warn('No checksum to evaluate...')
            package_name = _python_package_installer(package, flags)
    print "Installed {0}".format(package)

def install_python_2_7():
    """install Python 2.7 from source"""
    if sys.version_info < (2, 7):
        # get some python dependencies installed
        reqs = ['libreadline5-dev', 'libssl-dev', 'libbz2-dev', 'libsqlite3-dev']
        for pkg in reqs:
            _apt_get(pkg)
        # make sure in the correct dir
        with cd(SOURCE_DIRECTORY):
            run('wget http://python.org/ftp/python/2.7/Python-2.7.tgz')
            run('tar -xf Python-*')
            with cd('Python-*'):
                run('./configure')
                run('make')
                sudo('make altinstall')
        print "Python successfully installed"
    else:
        print "Python is at 2.7"
    # update our path
    _update_path()

def build():
    # we'll need gfortran for numpy and scipy
    #_apt_get('gfortran')
    #_check_for_source_directory()
    #install_python_2_7()
    #source('http://pypi.python.org/packages/source/s/setuptools/setuptools-0.6c11.tar.gz', hash='7df2a529a074f613b509fb44feefe74e', type='md5')
    #source('http://pypi.python.org/packages/source/F/Fabric/Fabric-0.9.2.tar.gz',type='md5', hash='5ba652d4d4525fb6b470edf55747ea45')
    #_apt_get('libblas-dev libatlas-base-dev liblapack-dev')
    #source('http://sourceforge.net/projects/numpy/files/NumPy/1.5.0/numpy-1.5.0.tar.gz', '--fcompiler=gnu95', type='md5', hash='3a8bfdc434df782d647161c48943ee09')
    
    # scipy 0.8.0 has a bug in csr_wrap that halts compilation - just get a rev that i know works
    #svn('http://svn.scipy.org/svn/scipy/trunk/@6832', 'scipy-dev6832')
    #source('http://biopython.org/DIST/biopython-1.55.tar.gz')
    #source('http://pypi.python.org/packages/source/p/pyfasta/pyfasta-0.3.9.tar.gz', type='md5',hash='a8a0bd3d3b6eb84ceab969af342ecbff')
    #source('http://pypi.python.org/packages/source/b/bx-python/bx-python-0.6.0.tar.gz',type='md5',hash='bbc9db96406e94b0bde3d2ca8d85782b')