#!/usr/bin/perl -p

s/&quot\;/ /;
s{\[[^]]*\.png\]}{ }g;
s/[^A-Za-z\s'\.,-]/ /g;
s/^\s*//g;
s/\s+/\n/g;
