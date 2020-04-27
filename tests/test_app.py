#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_api import status

from app.app import liveness_check, hello_world


def test_liveness_check():
    assert liveness_check() == ("OK", status.HTTP_200_OK)

def test_hello_world():
    assert hello_world() == ("Hello world!")
