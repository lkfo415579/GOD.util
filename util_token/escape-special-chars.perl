#!/usr/bin/perl -w

use strict;

while(<STDIN>) {
  chop;

  # avoid general madness
  s/[\000-\037]//g;
  s/\s+/ /g;
	s/^ //g;
	s/ $//g;

  # special characters in moses
  s/\&/\&amp;/g;   # escape escape
  s/\|/\&bar;/g;  # factor separator
  s/\</\&lt;/g;    # xml
  s/\>/\&gt;/g;    # xml
  s/\[/\&bra;/g;   # syntax non-terminal
  s/\]/\&ket;/g;   # syntax non-terminal
  
  # restore xml instructions
  s/\&lt;(\S+) translation=&quot;(.+?)&quot;&gt; (.+?) &lt;\/(\S+)&gt;/\<$1 translation=\"$2\"> $3 <\/$4>/g;
  print $_."\n";
}
