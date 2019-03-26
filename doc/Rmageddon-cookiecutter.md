# QBiC R analysis template

This repo holds a [cookiecutter](https://github.com/audreyr/cookiecutter) template for reproducible analysis with R at QBiC.

## Template using cookiecutter

You can easily create an R container from the template with [cookiecutter](https://github.com/audreyr/cookiecutter), a Python command-line tool for the creation of projects from templates. Just use ``pip`` ([https://pip.pypa.io/en/stable/](https://pip.pypa.io/en/stable/)) to install it:

```
$ pip install cookiecutter
```
In order to create a project from the `rmageddon-cookiecutter`, just type:

```
$ cookiecutter https://github.com/qbicsoftware/rmageddon-cli
r_version [3.2.4]: 
author_name [Sven Fillinger]: 
author_email [sven.fillinger@qbic.uni-tuebingen.de]: 
container_version [0.1dev]: 
project_code [QABCD]: 
description [Put a short analyses description here]: 
```
As you see, the command line will prompt you for some information. If you just hit `<enter>`, it will take the default value (In brackets).

Cookiecutter will replace placeholders with the information you provided and you get a ready base R project layout like this:

```
├── QABCD
│   │   ├── data
│   │   │   └── input_data
│   │   ├── Dockerfile
│   │   ├── environment.yml
│   │   └── scripts
│   │       └── example.R

```
The environment.yml file can be used for Rmageddon-build if you are not using your own anaconda environment file.

# Author

This template was created by Sven Fillinger [@sven1103](https://github.com/sven1103), QBiC, University of Tübingen.

# Acknowledgements

I want to thank the creators of [cookiecutter](https://github.com/audreyr/cookiecutter) for this amazing templating tool!
