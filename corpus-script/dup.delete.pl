#!/usr/bin/perl -w

#Auther: Liang Tian, University of Macau
#Date: 22/08/2013
#This is the step-3: Put the *.txt file under this directory, this script will seperate *.txt with two kind language into two different files. To get a parallel corpus. 
#
binmode(STDIN, ":utf8");
binmode(STDOUT, ":utf8");
binmode(STDERR, ":utf8");
use utf8;
use LWP::Simple;
use strict;
use warnings;

my $inputFile1 = $ARGV[0];#######input NAME!!!!
my $inputFile2 = $ARGV[1];


open E, "<:utf8", $inputFile1 or die $!;
open C, "<:utf8", $inputFile2 or die $!;
open TEST,">:utf8", "test.txt" or die $!;

#We take English-Chinese as the Example
#使用前请将英文语料库中的某些标点符号前的空格去掉 以便统一！例如：\s,->,  \s.->.
#Before using this script, please check some punctuations and error blanks. Delete these like: \s, into ,  and \s.into.

###############write two files into one new file#############################
print "START: write two files into one new file\n";
$a=0;
my @store=<C>;
while (<E>) {
  s/\n$/@@@@@/g;          #replace/n to mark"@@@@@"
  print TEST $_;
  print TEST $store[$a];
  $a++;
}
close(E);
close(C);
close(TEST);

##############################################################################
#######################delete duplicate records###############################
print "START: delete duplicate records\n";
open TEST,"<:utf8", "test.txt" or die $!;
open TEST_OUT,">:utf8", "test_out.txt" or die $!;
my %hash;
while (<TEST>) {
    if (!$hash{$_}) {
        print TEST_OUT;
      $hash{$_} += 1;
    }
}
close(TEST_OUT);
close(TEST);
################################################################################
print "START: write final 2 files\n";

my $finalinputFile1 = 'final_'.$inputFile1; ###output NAME
my $finalinputFile2 = 'final_'.$inputFile2;
open TEST_OUT,"<:utf8", "test_out.txt" or die $!;
open E_OUTPUT,">:utf8", $finalinputFile1 or die $!;     #The final corpus of English
open C_OUTPUT,">:utf8", $finalinputFile2 or die $!;     #The final corpus of Chinese
while (<TEST_OUT>)
{
	if (/(^.+)@@@@@(.*)/)
	{
		print E_OUTPUT $1."\n";
		print C_OUTPUT $2."\n";
	}
}
close(TEST_OUT);
close(E_OUTPUT);
close(C_OUTPUT);

unlink("test.txt");
unlink("test_out.txt");
print "Done\n";
