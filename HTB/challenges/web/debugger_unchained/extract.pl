#!/usr/bin/env perl -w

use strict;
use MIME::Base64;

open(FH, '<traffic.pcapng');
while(<FH>) {
  my %s;
  foreach(m/(eyJ[A-Za-z0-9+\/=]+)/) {
    my $dec = decode_base64($1);
    print $dec,$/;
    $dec =~ tr/{}/()/;
    $dec =~ s/:/=>/g;
    %s = eval($dec);
    print decode_base64($s{'cmd'}) if(exists($s{'cmd'}));
    print decode_base64($s{'output'}) if(exists($s{'output'}));
    print $/;
  }
}
close(FH);
