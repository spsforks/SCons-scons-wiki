

# Packaging and Dependency Management for SCons


## Motivation

Decomposing and Reusing Software is one of the key elements of mastering Software Complexity. Typically Package Management Systems like Gentoo Portage solve the Problem of managing Dependencies between software components and therefore help in decomposing software, but are only available for a specific Software Platform. 

One of the key benefits of using SCons is its Platform-Neutrality in building Software. To extend this Neutrality to Packaging and Dependency Management is the aim of this work. 


## Abstract

A software lifecycle could be visualized like this: 
```txt
  Creating -> Changing -> Building -> Testing -> Packaging -> Deploying
                 |                        |          |            |
                 --------------------------------------------------
```
Typical Build Tools help you in managing everything up to the Testing  State.  Anything else must be done by Hand, which is a tedious task if managing more than two projects. 

Adding Packaging to SCons will therefore enable: 

* Better Quality of your packages (It's easier to conform to given standards) 
* A faster Changing-->Packaging Cycle. 
* Greater recognition of your software, since it's almost instantly available on many platforms. 
Packaging provides a basic but independent building block for Dependency Management, since it's needed to provide Dependencies for other packages. 


## Roadmap

As integrated Packaging into SCons is a big task, i'd like to start out  with it. 

For a detailed view of what I'd like to achieve over the summer i've put together the following Roadmap: 

* 2006-05-30 - M1 Creating Source Distributions 
* 2006-06-15 - M2 Creating RPMS 
* 2006-06-30 - M3 Creating MSI or [IzPack](IzPack) Installer 
* 2006-07-05 - M4 Write a "Howto create a Packager" and Usage Information 
* 2006-07-10 - M5 Refactor Dependency Metadata to a SCons Builder 
* 2006-07-20 - M6 Add support for implicit Dependencies 
* 2006-08-04 - M7 Creating Gentoo ebuilds 
I left time at the end on purpose, to reorganize or add further Milestones based on my progress. 


## Outlook

As I also like to add Dependency Management Capabilities, here's the Direction in which i like the project to progress after Summer of Code. 

Imagine a Requires() function for SCons, which denotes that the given build requires specific software packages to be usable on the local machine. 

SCons would then ask the local package management system to install the given package if not already available. SCons would know about the availability of a package either through querying the local package management system or through a Configure Context. 

Examples would be: 
```txt
   Requires( "java-sdk", ">=1.5" )
   Requires( "commons-logging", "=1.4" )
   Requires( "commons-logging-modification" )
   Requires( "nativelibrary", type="shared-library", autoadd="1" )
```

## Further Explanation

Create a "Platform Packager" abstraction that can be used to build a Software Package for every Platform. This also includes a Abstraction of the Package Identifier and shared Metadata like Organization, Author ... 

Examples: RPM, DEB, Python Eggs, Ruby Gems, Windows MSI, Jar, [IzPack](IzPack) Installers, Klik, Zip, Tar/GZ, Tar/Bzip2, Gentoo ebuild 

Special care must be taken to ensure that existing Dependencies will be inherited to the underlying package management system. If a software package is dependent on the python runtime environment, this dependency should be encoded in the rpm package and a python runtime environment should be included in the Tar/GZ package. This could be called explicit  Dependency. While implicit Dependencies are those that are added through using special tools, which are not known before the build process has completed. 

Futhermore the Install() function could then be modified to create a package for the local system and install it through the package manager, allowing a more conforming installation, a cleaner uninstallation and being able to present your software as a dependency for other Software. 
