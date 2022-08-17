# Socotra Library

Socotra's insurance platform is designed to be extended through configuration and its open APIs. While the product handles the "core", there are often many enhancements or extensions that may match your situation.  To ease the learning curve, Socotra provides integrations, code samples, example product configuration, and helpful test utilities that may aid in your processes. Feel free to use as-is or modify to best suit your needs.

Visit docs.socotra.com or contact us at support@socotra.com

## Table of Contents

**[default_config]:** The default configuration files serve as realistic examples of how a variety of features are used in practice. Default products include auto and term life.

**[socotratools]:**  This 2.7 Python package can be installed using pip. It includes a client wrapper for REST calls and utilities to manipulate dates in a specific timezone.

**[create_policy]:** Sometimes it's helpful to create a policy programatically.  This simple script uses json files to generate motor policies using the default configuration.

**[document_tools]:** These tools show how to render a template in Socotra without using the front-end - helpful for document develoment. Scripts for adding and removing documents are also added for convenience.

**[premium_test]:** These tools allow you to quickly iterate to develop your ratings engine using an existing policy/peril or by creating a peril from JSON files.

**[general_ledger]:** A common operation is to take the Soctora standard reports and import them into general ledger software systems for financial reporting.  This example uses PeopleSoft's import format but journal entries should be similar in other systems.

**[data_dictionary]:** When developing against the API, it's helpful to have a reference of all the product fields configured in an instance.  This script generates a CSV of all fields and associated data types.

**[stripe]:** This example uses Stripe's payment processor to pay a policyholder's outstanding invoices.

**[cognito]:** These tools show how to use an external directory service to add permissions to Socotra for various API function calls.  The example provided uses the AWS Cognito service.

**[product_examples]:** Socotra can be configured for any line of business.  In this directory, you can find sample product configurations for various lines of business to adapt to your needs.


MIT License
----

Copyright (c) 2022 Socotra

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [default_config]: <https://github.com/socotra/public/tree/master/default_config>
   [socotratools]: <https://github.com/socotra/public/tree/master/socotratools>
   [create_policy]: <https://github.com/socotra/public/tree/master/create_policy>
   [document_tools]: <https://github.com/socotra/public/tree/master/document_tools>
   [premium_test]: <https://github.com/socotra/public/tree/master/premium_test>
   [general_ledger]: <https://github.com/socotra/public/tree/master/general_ledger>
   [data_dictionary]: <https://github.com/socotra/public/tree/master/gen_data_dictionary.py>
   [stripe]: <https://github.com/socotra/public/tree/master/stripe>
   [cognito]: <https://github.com/socotra/public/tree/master/cognito>
   [product_examples]: <https://github.com/socotra/public/tree/master/product_examples>
