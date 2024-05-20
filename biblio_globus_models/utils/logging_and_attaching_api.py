import logging
import json
import allure
from requests import Response
from allure_commons.types import AttachmentType


def response_logging(response: Response):
    logging.info("Request: " + response.request.url)
    if response.request.body:
        logging.info("INFO Request body: " + response.request.body)
    logging.info("Request headers: " + str(response.request.headers))
    logging.info("Response code " + str(response.status_code))
    logging.info("Response: " + response.text)


def response_attaching(response: Response):
    allure.attach(
        body=response.request.url,
        name='request url',
        attachment_type=AttachmentType.TEXT,
        extension='.txt'
    )

    allure.attach(
        body=str(response.status_code),
        name='response status code',
        attachment_type=AttachmentType.TEXT,
        extension='.txt'
    )

    allure.attach(
        body=response.text,
        name='response text',
        attachment_type=AttachmentType.TEXT,
        extension='.txt'
    )

    if response.request.body:
        allure.attach(
            body=json.dumps(str(response.request.body)),
            name='request body',
            attachment_type=AttachmentType.JSON,
            extension='.json'
        )

