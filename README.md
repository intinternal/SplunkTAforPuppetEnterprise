Puppet TA for Puppet Enterprise
[![Documentation Status](https://readthedocs.org/projects/splunktaforpuppetenterprise/badge/?version=latest)](http://splunktaforpuppetenterprise.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/domeger/SplunkTAforPuppetEnterprise.svg?branch=master)](https://travis-ci.org/domeger/SplunkTAforPuppetEnterprise)
======

Documentation
-------------
The Puppet TA for Puppet Enterprise requires that you have the following installed:

[**Splunk Enterprise 7.0+**](https://www.spunk.com)


[**Puppet Enterprise 2017.1.1+**](https://www.puppet.com)

Version 1.0.7:
Puppet Enterprise Add-on Rewrite
    - Includes Support for Self Signed (8081) + HTTP (8080) for PuppetDB Calls
    - Rewrite of all Extraction Fields + Cleanup of Resources, Classes, and CertName
    - Fixed API Key Storage
    - Fixed Title to Match Pulls
    - Fixed Help Text to Match Fields
    - Fixed Issue with Memoryleak on Timeout API Calls



Installation
------------

**Method: #1**

#### Install via Splunk Package

First, you'll need to export a Splunk Package by cloning the repo and exporting
the contents.

```
$ git clone https://github.com/domeger/SplunkTAforPuppetEnterprise.git SplunkTAforPuppetEnterprise
$ cd SplunkTAforPuppetEnterprise
$ git archive \
    --format=tar.gz \
    --prefix=SplunkTAforPuppetEnterprise/ \
    --output=SplunkTAforPuppetEnterprise.tar.gz \
    HEAD
$ mv SplunkTAforPuppetEnterprise.tar.gz SplunkTAforPuppetEnterprise.spl
```

After exporting the Splunk Package `.spl`, you can install the package using
Splunk's built-in Apps page.

1. Select "Manage Apps" from the Apps dropdown.
1. Select the "Install app from file" button.
1. Select the generated `SplunkTAforPuppetEnterprise.spl` package.
1. Splunk will walk you through all required setup.

External Resource: Splunk GUI Installation Interface - [Splunk Documentation - Install App](https://docs.splunk.com/Documentation/AddOns/released/Overview/Distributedinstall "Splunk Docs")


**Method: #2**

#### Install via Git Clone

You can install the git repository directly into your Splunk app contents and
keep the scripts updated.

```
$ export SPLUNK_HOME="/path/to/Splunk"
$ cd $SPLUNK_HOME/etc/apps
$ git clone https://github.com/domeger/SplunkTAforPuppetEnterprise.git SplunkTAforPuppetEnterprise
```

Restart Splunk after cloning the repository, then open the Setup page from the
Manage Apps page to configure your Puppet Enterprise server info. From the Manage Apps page
you can also enable and disable the Puppet Enterprise Addon for Splunk.

** Next Steps: Generate a Token **

```curl -k -X POST -H 'Content-Type: application/json' -d '{"login": "<YOUR PE USER NAME>", "password": "<YOUR PE PASSWORD>"}' https://$<HOSTNAME>:4433/rbac-api/v1/auth/token```


Developing and Contributing
---------------------------
The Puppet TA for Puppet Enterprise requires Splunk 6.4+ and Splunk Addon Builder 2.0+ in order to properly add new features or bug fixes. Please refer to the [Splunk Documentation - Addon Builder](https://docs.splunk.com/Documentation/AddonBuilder/2.2.0/UserGuide/Importandexport) on how to use Git to develop and push your changes to this repo as a branch and following the standard code review process.

License
-------

See [LICENSE](LICENSE) file.

Third Party License
-------------------
http://docs.splunk.com/Documentation/AddonBuilder/2.2.0/UserGuide/Validate#Credit_third-party_libraries

Support
-------

Are you a Splunk + Puppet customer who enjoys sharing knowledge and want to put some great feature into an opensource project. We encourage you to submit issues and pull request so that we can make this Technical Addon better and help the community as a whole get better insight to their Puppet Enterprise deployments.

Feel free to leave comments or questions. We are here to make this community project more adaptive to all types of use cases.
