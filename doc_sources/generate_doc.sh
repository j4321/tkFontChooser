#! /bin/bash
# -*- coding:Utf-8 -*-

rm -r ../docs
make html
mv ../html ../docs
