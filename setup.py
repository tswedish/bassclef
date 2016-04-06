#! /usr/bin/env python3

"""setup.py - setup script for bassclef."""

import sys
import os, os.path
import shutil
import pip
import subprocess
import textwrap
import urllib
import zipfile

SUBMODULES = ['font-awesome', 'html5shiv', 'open-sans', 'skeleton']

URLS = ['https://github.com/' + path for path in
        ['tomduck/bassclef-font-awesome/archive/master.zip',
         'aFarkas/html5shiv/archive/master.zip',
         'tomduck/bassclef-open-sans/archive/gh-pages.zip',
         'dhg/Skeleton/archive/master.zip']]

#----------------------------------------------------------------------------

def check_for_binaries():
    """Checks that binary dependencies are installed."""

    print()
    
    # Check for make
    print("Testing make's availability... ", end='')
    if shutil.which('make') is None:
        msg = """

        Cannot find 'make'.  Please ensure that 'make' is available from
        the command line.

        Please submit an Issue to the bassclef developers:

            https://github.com/tomduck/bassclef

        """
        print(textwrap.dedent(msg))
        sys.exit(3)
    print('OK.')


    # Check for pandoc
    print("Testing pandoc's availability... ", end='')
    if shutil.which('pandoc') is None:
        msg = """

        Cannot find 'pandoc'.  Please ensure that 'pandoc' is available from
        the command line.

        To download pandoc, see:

            https://github.com/jgm/pandoc/releases/latest

        """
        print(textwrap.dedent(msg))
        sys.exit(4)
    print('OK.')


    # Check for ImageMagick convert
    print("Testing convert's availability... ", end='')
    if shutil.which('convert') is None:
        msg = """

        Cannot find ImageMagick 'convert'.  Please ensure that 'convert' is
        available from the command line.

        To download ImageMagick, see:

            https://www.imagemagick.org/script/binary-releases.php

        """
        print(textwrap.dedent(msg))
        sys.exit(5)
    print('OK.\n')

#----------------------------------------------------------------------------

def install_pyyaml():
    """Installs pyyaml."""
    print('Installing pyyaml:')
    pip.main('install pyyaml --user'.split())

#----------------------------------------------------------------------------

def install_submodules():
    """Installs bassclef's submodules."""

    print('\nInstalling submodules:', end='')

    # Is this a git repository?
    is_repo = os.path.exists('.git')

    # Install the submodules
    if is_repo:   # Assume user has git installed

        print()

        if subprocess.call('git submodule update --init'.split()) != 0:
            msg = """

            Error installing submodules with git.  Please submit an Issue to
            the bassclef developers:
 
            https://github.com/tomduck/bassclef

            """
            print(textwrap.dedent(msg))
            sys.exit(6)

        print()


    else:  # Do it manually

        print()

        def prog(n=0):
            """Progress meter."""
            while True:
                if n%20 == 0:
                    print('.', end='')
                    sys.stdout.flush()
                yield
                n += 1
        report = prog().__next__

        os.chdir('submodules')

        for submodule, url in zip(SUBMODULES, URLS):
            if not os.listdir(submodule):
                print('\nDownloading %s...'%submodule, end='')
                urllib.request.urlretrieve(url, 'download.zip',
                                           lambda x, y, z: report())
                print(' Done.')

                print('Installing %s...'%submodule, end='')
                z = zipfile.ZipFile('download.zip', 'r')
                dirname = os.path.commonprefix(z.namelist())
                z.extractall()
                z.close()

                os.rmdir(submodule)
                os.rename(dirname, submodule)
                os.remove('download.zip')
                print(' Done.')

        os.chdir('..')
        print()

#----------------------------------------------------------------------------

def test():
    """Tests the install."""

    print('Testing install... ', end='')
    try:
        subprocess.check_output('make')
        print('Done.')
    except subprocess.CalledProcessError as e:

        msg = """

        'make' failed (error code %d).  Please submit an Issue to the bassclef
        developers:

            https://github.com/tomduck/bassclef

        """ % e.returncode
        print(textwrap.dedent(msg))
        sys.exit(7)

#----------------------------------------------------------------------------

def finish():
    """Finishes up."""

    msg = """

    Bassclef has installed successfully and all tests succeeded.

    """
    print(textwrap.dedent(msg))

#----------------------------------------------------------------------------

def main():
    """Main program."""

    check_for_binaries()
    install_pyyaml()
    install_submodules()
    test()
    finish()

if __name__ == '__main__':
    main()
