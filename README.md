# API_validation
*****************************************************
*                   ReadNe                          *
*****************************************************
*   Author: Rene Yang
*   Email: yang.rene@outlook.com
*   Version: 1.0
*   Release Date: 2022-04-08
*   Programming language: python 3.8.x
*****************************************************
*                   Description                     *
*****************************************************
This script is used to do the validation check for the API message from the Web link.
    1. The default web link is as following,
        https://api.tmsandbox.co.nz/v1/Categories/6327/Details.json?catalogue=false
        If you hope to change the source API Web link, please input the valid target Web link to the command line parameter input.
    2. The default acceptance criteria is as following,
        • Name = "Carbon credits"
        • CanRelist = true
        • The Promotions element with Name = "Gallery" has a Description that contains the text "Good position in category".
        If you hope to change the acceptance criteria, please edit the "acceptance_criteria.json" with JSON format first.
    3. The validation result will be PASS when all the acceptance criteria are met. If one of them are not met, the validation result will be FAIL.
    4. The default logs folder is logs in the parent folder.
*****************************************************
*                   Usage                           *
*****************************************************
    1. edit "acceptance_criteria.json" with JSON format according to the acceptance criteria
       Notes: The format of the KSON object should follow the definition and format in the Weblink.
    2. python3 API_validation.py [valid target web link]
