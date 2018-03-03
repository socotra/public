[![N|Solid](http://docs2.socotra.com/production/_static/socotraLogoBlack.svg)](https://www.socotra.com)

# Socotra Library

Socotra's insurance platform is designed to be extended through configuration and its open APIs. While the product handles the "core", there are often many enhancements or extensions that may match your situation.  To ease the learning curve, Socotra provides integrations, code samples, example product configuration, and helpful test utilities that may aid in your processes. Feel free to use as-is or modify to best suit your needs.

Visit docs2.socotra.com or contact us at support@socotra.com

## Table of Contents

**[default_config]:** The default configuration files serve as realistic examples of how a variety of features are used in practice. Default products include auto and term life.

**[socotratools]:**  This 2.7 Python package can be installed using pip. It includes a client wrapper for REST calls and utilities to manipulate dates in a specific timezone.

**[create_policy]:** Sometimes it's helpful to create a policy programatically.  This simple script uses json files to generate motor policies using the default configuration.

**[document_tools]:** These tools show how to render a template in Socotra without using the front-end - helpful for document develoment. Scripts for adding and removing documents are also added for convenience.

**[premium_test]:** These tools allow you to quickly iterate to develop your ratings engine using an existing policy/peril or by creating a peril from JSON files.

**[general_ledger]:** A common operation is to take the Soctora standard reports and import them into general ledger software systems for financial reporting.  This example uses PeopleSoft's import format but journal entries should be similar in other systems.

##### Coming Soon
  - Stripe Integration
  - Data Dictionary Generation
  - Consumer Website Example


License
----

GNU Lesser General Public License 


**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [default_config]: <https://github.com/socotra/public/tree/master/default_config>
   [socotratools]: <https://github.com/socotra/public/tree/master/socotratools>
   [create_policy]: <https://github.com/socotra/public/tree/master/create_policy>
   [document_tools]: <https://github.com/socotra/public/tree/master/document_tools>
   [premium_test]: <https://github.com/socotra/public/tree/master/premium_test>
   [general_ledger]: <https://github.com/socotra/public/tree/master/general_ledger>
