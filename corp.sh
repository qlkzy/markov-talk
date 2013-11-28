#!/bin/bash

xargs cat  <<ENT
corpus/cc.txt
corpus/rtut.txt
ENT
#find corpus -name 'what-if*' -type f | shuf | head -n30 | xargs cat

