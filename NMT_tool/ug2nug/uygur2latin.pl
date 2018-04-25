#!/usr/bin/perl -w

use Getopt::Long;
use File::Basename;

my $maptxt = dirname($0)."/map.txt";

GetOptions(
"m|map=s" => \$maptxt,
"skip-X"  => \$skip_X,
"h|help"  => \$help
) or die &usage;

if($help)
{
    &usage;
    exit;
}

binmode(STDIN,":raw:encoding(utf8)");
binmode(STDOUT,":raw:encoding(utf8)");
binmode(STDERR,":raw:encoding(utf8)");
#print STDOUT "\x{feff}";
#print STDERR "\x{feff}";


%QuesChHs = ();
%ChrJPHs  = ();#保存“维语老文字=>键盘字符”的hash
open(MAPLIST, "<:raw:encoding(utf8)", $maptxt) || die("Can not open $maptxt!\n");
$linenum = 0;
while($line = <MAPLIST>)
{
	$linenum++;
	if($linenum == 1){
		$char = substr($line, 0, 1);
		if(ord $char == 0xfeff){
			$line = substr($line, 1);#去掉文件编码头
		}
	}
	$line =~ s/\r|\n|^\s+|\s+$//g;
	next if($line eq "" || $line =~ /^\#/);
	
	@arrays = split(/\t/, $line);
	die("$maptxt-$linenum: wrong line!\n") if(@arrays != 4);
    if($linenum == 2 and $skip_X){
    	$ChrJPHs{$arrays[1]} = "";#老文字 => 键盘
    } else {
		$ChrJPHs{$arrays[1]} = $arrays[-1];#老文字 => 键盘
    }
}
close MAPLIST;
print STDERR "$maptxt read over!\n";

$linenum = 0;
while($line = <STDIN>){
	$linenum++;
	if($linenum == 1){
		$char = substr($line, 0, 1);
		if(ord $char == 0xfeff){
			$line = substr($line, 1);#去掉文件编码头
		}
	}
	$line =~ s/\r|\n|^\s+|\s+$//g;
    if($line eq ""){
        print STDERR "Empty line: $linenum++\n";
    }
	
	#print STDOUT $line."\r\n";
	
	@chars = split(//, $line);
	$chJP = "";
	for($i = 0; $i < @chars; $i++)
	{
		$c = $chars[$i];
		if(exists $ChrJPHs{$c}){
			#if($ChrJPHs{$c} eq "*"){#注意映射表中的第一个字符，*表示没有对应符号
			#	next;
			#}
			$chJP = $chJP.$ChrJPHs{$c};
		}
		elsif($c =~ /^[\s\.\;\,\?\:\'\"\<\>\!\%\(\)\*\-\+\=\@\#\$\&0-9a-zA-Z\/\\]$/){
			$chJP = $chJP.$c;
		}
		else{
            #$QuesChHs{$c}=$QuesChHs{$c}."$linenum $line |||";
			$chJP = $chJP.$c;
			#next;
			#die("$txtin-$linenum: Illegal char!\n");
		}
	}#for($i = 0; $i < @chars; $i++)
	print STDOUT "$chJP\r\n";
}

$bHave = 0;
foreach (sort keys %QuesChHs){
	$d = sprintf("%04x", ord $_);
	print STDERR $_."\t".$d."\t$QuesChHs{$_}\r\n";
	$bHave = 1;
}
if($bHave == 0){
	print STDERR "Congratulation! Your uyghur text STDIN is good!\n";
}

print STDERR "Convert Ok!\n";
print STDERR "please examine log in STDERR\n";


## End of main

sub usage
{
print <<__USAGE__;
usage: $0 < input > output
  -m,map     mapping file ( default: map_v0.1.txt in the same dir with $0)
  -skip-X    do not convert the special symbal( resembles a ear ) to "X"
             turn on this option for uygur to chinese MT system
  -h,help    print this help information
__USAGE__
}


