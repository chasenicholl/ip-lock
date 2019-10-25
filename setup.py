"""ip-lock Module Setup"""

from setuptools import find_packages, setup

from ip_lock import __VERSION__


INSTALL_REQUIRES = [
    'pyyaml==5.1.2',
    'requests==2.21.0'
]


if __name__ == '__main__':
    setup(name='ip-lock',
          version=__VERSION__,
          description=("A utility for keeping your dynamic public"
                       " IP address up to date within your DNS provider."),
          author="Chase Nicholl",
          author_email='hello@chasenicholl.com',
          url='https://github.com/chasenicholl/ip-lock',
          packages=find_packages(),
          scripts=['bin/ip_lock'],
          install_requires=INSTALL_REQUIRES,
          include_package_data=True)
