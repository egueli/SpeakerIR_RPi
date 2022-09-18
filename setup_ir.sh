#!/bin/bash

set -e

ir-keytable --write=lg.toml
ir-keytable -D 100 -P 100
