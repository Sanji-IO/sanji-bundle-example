#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import os
from sanji.core import Sanji
from sanji.core import Route
from sanji.model_initiator import ModelInitiator
from sanji.connection.mqtt import Mqtt


class Example(Sanji):

    def init(self, *args, **kwargs):
        path_root = os.path.abspath(os.path.dirname(__file__))
        """
        Config will be located at ./data/example.json
        If ./data/example.json not exist,
            modelInitiator will create from ./example.json.factory
            and program could access dict object from self.model.db
        (modelInitiator is optional, you can handle data/config by your own)
        """
        self.model = ModelInitiator("example", path_root)

        # Check daemon status here and start/stop it.

    @Route(methods="get", resource="/example")
    def get(self, message, response):
        # Response dict
        # response code => http status code
        #          data => payload
        return response(code=200, data=self.model.db)

    @Route(methods="put", resource="/example")
    def put(self, message, response):
        # Assign incomming dict object to self.model.db
        self.model.db = message.data

        # Save to ./data/example.json
        self.model.save_db()

        # Response current dict object
        #   response code default = 200
        return response(data=self.model.db)


if __name__ == "__main__":
    FORMAT = "%(asctime)s - %(levelname)s - %(lineno)s - %(message)s"
    logging.basicConfig(level=0, format=FORMAT)
    logger = logging.getLogger("Example")
    hellosanji = Example(connection=Mqtt())
    hellosanji.start()
