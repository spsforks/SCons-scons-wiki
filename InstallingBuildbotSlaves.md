
[[!toc 2]] 


# Installing a Buildbot slave

By setting up a Buildbot slave and registering it with our master process at `buildbot.scons.org` ([link](http://buildbot.scons.org)) you can contribute to the SCons project a lot. We are always looking for volunteers to help us cover additional platforms or build options in [BuildBot](BuildBot). Having a good amount of diversity among the provided slave setups helps us to keep SCons cross-platform and functioning in general. 

It's not that complicated to get a Buildbot slave running and is a good way to get involved without having to spend a lot of time on it.  If you are able to provide a spare machine for this purpose, your help is greatly appreciated! 

Here you'll find a list the packages to install and steps for: 

* Windows XP, 32bit, Home Edition and 
* a Fedora 17 Linux, 32bit, Desktop Edition 
Free to improve this instructions and complement them where necessary. In general, apply common sense. 


# Setup Mercurial

We use Mercurial for all the source control stuff, so your Buildbot slave needs it to get the freshest version of the code. 

Ensure that you have `hg` installed and that you can call Mercurial directly in the command line (DOS prompt, terminal, shell, ...whatever). So download it from 

[http://mercurial.selenic.com/wiki/Download](http://mercurial.selenic.com/wiki/Download) 

and install it, if required. The command 


```txt
> hg
```
should give you a help text about the different options that `hg` can be called with. Make sure that the `bin` directory of `hg` is added to your `PATH` variable, such that you can execute the command from anywhere without specifying the full path. 

For automatic testing you need to enable `purge` extension. Find or create `~/.hgrc` file (Linux). If you plan to do some development on this machine, don't forget to add a user entry. The file should look like this: 


```txt
[ui]
user = John Doe <john.doe@whoami.com>

[extensions]
hgext.purge=
```

# Under Windows XP


## Download and installation

If you don't already have a Python version installed, download and install Python 2.7.x from: 

[http://www.python.org/download](http://www.python.org/download) 

The next package you'll need is `pywin32`. Download and install it from: 

[http://sourceforge.net/projects/pywin32/files/pywin32](http://sourceforge.net/projects/pywin32/files/pywin32) 

Now, download the `setuptools` from: 

[http://pypi.python.org/pypi/setuptools#downloads](http://pypi.python.org/pypi/setuptools#downloads) 

and watch out for the correct Python version. It should match with the one you have installed in your system. You probably want the MSWindows installer (`.exe`) not the EGG! 

Install the `setuptools` and update the `PATH` such that `easy_install.exe` is found on the commandline. 

Then download and install Twisted from: 

[http://twistedmatrix.com/trac/wiki/Downloads](http://twistedmatrix.com/trac/wiki/Downloads) 

Install the additionally required `zope.interface` with: 


```txt
> easy_install zope.interface
```
This command should automatically download the matching EGG and install it. If this doesn't work as advertised, you can try one of the direct downloads which are available at [http://pypi.python.org/pypi/zope.interface](http://pypi.python.org/pypi/zope.interface). 

Finally, download `buildbot-slave` from: 

[http://code.google.com/p/buildbot/downloads/list](http://code.google.com/p/buildbot/downloads/list) 

Get the ZIP archive of the latest version (`buildbot-slave*.zip`), unzip it, and then install by changing into the extracted folder (`buildbot-slave*`) and executing: 


```txt
> c:\Python26\python.exe setup.py install
```
(Please, replace the path to Python with the version that you have installed.) 


## Getting registered

Send an email to [scons-dev@scons.org](mailto:scons-dev@scons.org), signalling that you want to setup a Buildslave. Include some basic info about your system, like Windows vs Linux and the used Python version. After a short while, you get an answer with the builder name and password that your Buildslave should use to register and communicate with the server. 


## Starting the first time

Add a new directory like 


```txt
c:\buildbot
```
, and under it 


```txt
c:\buildbot\buildslave
```
. Change to `c:\buildbot\buildslave` and check whether you can call the buildslave script: 


```txt
> c:\Python26\Scripts\buildslave.bat --version
```
should give you the version numbers of Twisted and buildbot. Now create your buildslave account and local info files with: 


```txt
> c:\python26\Scripts\buildslave.bat create-slave -r . buildbot.scons.org:9989 your_builder_name your_password
```
Then edit the files `info/admin` and `info/host` accordingly and finally start the slave with: 


```txt
> c:\Python26\Scripts\buildslave.bat start c:\buildbot\buildslave
```
For setting the buildslave up as service, find more infos at: 

[http://trac.buildbot.net/wiki/RunningBuildbotOnWindows](http://trac.buildbot.net/wiki/RunningBuildbotOnWindows) 


## Setup service

The following steps assume that you have a separate user named "buildslave" in your system, which gets assigned the right to automatically start the service at bootup. Create this account now, if you haven't already done so. 

Here are the further steps I used to setup my Buildbot client under Windows XP Home. The "Home" is important, because it means that you can't easily start a `cmd` exe with all proper Administrator rights, such that you could successfully execute the following commands (as found on the internet in various places). 

The only thing that worked for me was, to restart Windows in "Secured mode" (press F8 key while booting) and to login as Administrator directly. If you have a "full" Windows installation, the following steps should also work in a command prompt that you "Execute as: Administrator" while being logged in normally. 

Okay, so assuming we have a command prompt with full admin access rights, first thing to do is to create the service: 


```txt
> sc create BuildBot DisplayName= "Buildbot client" binPath= "c:\Python26\python.exe c:\Python26\Scripts\buildbot_service.py start c:\buildbot\buildslave " start= auto obj= LocalSystem
```
Note, how there is always a separating blank between each "command=" and the actual value, and also at the end of the binPath value! 

If the command above was successful you should be able to run a 


```txt
> sc sdshow BuildBot
```
, showing you the current access rights for starting/stopping the service. This is where we now have to add our user "buildslave". For this, we need his account SID on the local system. Open the registry editor by calling 


```txt
> regedit
```
and browse to the key `LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList`. Search through the single entries until you find the one that has the buildslave user name in its _[ProfileImagePath](ProfileImagePath)_. Note the SID, which should look something like `S-1-5-21-2103278432-2794320136-1883075150-1000`. 

Now write the output of the sdshow command into a text file: 


```txt
> sc sdshow BuildBot > scset.bat
```
and edit it. Append the following text snippet to the end of the line 


```txt
(A;;RPWPCR;;;S-1-5-21-2103278432-2794320136-1883075150-1000)
```
while replacing the SID above with your own. Then prepend the commands `sc sdset BuildBot` to the line, such that the full batch file command reads like: 


```txt
sc sdset BuildBot D:(A;; [...] )(A;;RPWPCR;;;S-your-local-SID-for-buildslave)
```
Save the batch file and run it 


```txt
> scset.bat
```
After a reboot you should be allowed to start/stop the [BuildBot](BuildBot) service as user "buildslave". 


# Under Fedora


## Installation

First, I did a full Fedora install, additionally selecting some development packages: 

* development-tools, development-libs 
* java, java-development 
* kde-desktop, kde-software-development 
* xfce-desktop, xfce-software-development 
* x-software-development 
Then I installed the following packages, actually required to get the Buildslave going: 

* python, python-devel, python-setuptools 
* python-twisted 
* buildbot, buildbot-slave 
For installing the required zope.interface, I simply called: 


```txt
> easy_install zope.interface
```
Then, I installed the following tools: 

* gcc, gcc-g++, gcc-fortran 
* mercurial 
* sip, swing 
where only mercurial (hg) is really required. The others were added to simply cover more tests. For the same reason I also installed [TeXlive](TeXlive) 2012 via its `install-tl` program, and had to add another dependency: 

* perl-digest-MD5 
since the installer is written in Perl. 


## Registering/Starting

Registering and actually starting the Buildslave under Linux is very similar to the Windows description above. So I'll just quickly outline some of the commands, the rest should get clear from this. 

First, add a new user `buildslave` (group: `buildslave`) to your system. Login as `buildslave` and create a `buildbot/buildslave` folder in your home directory: 


```txt
> mkdir -p ~/buildbot/buildslave
```
Check that you can call the buildslave script: 


```txt
> buildslave --version
```
and get the version numbers of Twisted and buildbot printed out. Change into your build directory 


```txt
> cd ~/buildbot/buildslave
```
and init the buildslave account with 


```txt
> buildslave create-slave -r . buildbot.scons.org:9989 your_builder_name your_password
```
Then edit the files `info/admin` and `info/host` accordingly and finally start the slave with: 


```txt
> buildslave start /home/buildslave/buildbot/buildslave
```

## Reboot/virtualenv

Quoting Bill Deegan: 

On linux I'd suggest creating a separate user just for the buildslave, and starting buildbot slave via a crontab entry "`@reboot`" 

Here's what I have on one of my machines; 


```txt
@reboot /home/sconsbuildbot/slave/bbenv/bin/buildslave start /home/sconsbuildbot/slave
```
For installing a buildbot slave on linux I use: 


```txt
virtualenv --no-site-packages bbenv
bbenv/bin/activate
pip install buildbot-slave
```
After it finishes: 


```txt
mkdir slave
cd slave
$HOME/bbenv/bin/buildslave create-slave -r . buildbot.scons.org:9989 your_builder_name your_password
```

# Under Debian


## Install prerequisites

You need to be root to do this. 
```txt
apt-get install mercurial python-virtualenv
```

## Add user

Add `scons` user. You need to be root to do this. 
```txt
adduser scons
su scons
cd ~
```
Everything below is made under `scons` user account. 


## Setup Mercurial

Enable purge extension: 
```txt
vim ~/.hgrc
```

## Setup build slave

Debian, as usual, includes only outdated versions of software, so we install buildbot slave from Python packages. 


```txt
mkdir ~/buildbot
cd ~/buildbot

# install in virtual environment to keep it tidy
virtualenv --no-site-packages venv
. ./venv/bin/activate
pip install buildbot-slave

# create environment
buildslave create-slave . buildbot.scons.org:9989 your_builder_name your_password

# run the slave
buildslave start
```