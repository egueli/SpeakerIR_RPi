#!/bin/bash

set -e

ir-keytable --write=acer.toml
ir-keytable -D 100 -P 100
