#!/usr/bin/perl -w

# Liang Tian, write for split one file into separate files 
use LWP::Simple;
use utf8; 
use Encode;
use Encode::CN;
use Cwd qw(abs_path);
binmode(STDIN, ":utf8");
binmode(STDOUT, ":utf8");
binmode(STDERR, ":utf8");
use HTML::Entities;

($input) = $ARGV[0];

# $input = decode("unicode", '雅思双语阅读：开心工作的十二条秘诀.txt');
# $output = encode("unicode", $output);
# $output1=$input.'.zh';
# $output2=$input.'.en';
# $input =~ s/\\/\\\\/g;

# my @files=glob(encode(gb2312,"gtct-training"));##########type of File!###################
my @files=glob(encode(gb2312,$input));
foreach $fileName (@files){ 
	# $abs_fileName = abs_path($fileName);
	# print $abs_fileName;
	$newfileName=$fileName;
	$newfileName =~ s/\.txt//g;
	$newfileName1 = $newfileName."-1\.txt";
	$newfileName2 = $newfileName."-2\.txt";
	open FILE,"<:utf8", $fileName or die $!;
	open C1,">:utf8", $newfileName1 or die $!;
	open C2,">:utf8", $newfileName2 or die $!;
	$a=0;
	while (<FILE>) 
	{
		decode_entities();
		no warnings "utf8";
		&encode_utf_8;
		if ($a!=1)
		{
			print C1 $_;
			$a++;
		}
		else
		{
			print C2 $_;
			$a=0;
		}
	}
	close (FILE);
	close (C1);
	close (C2);
}
print "Done";


sub encode_utf_8 {
    # my $string = @_;
  my $string = $_;
 
    my $utf8_encoded = '';
    eval {
        $utf8_encoded = Encode::encode('UTF-8', $string, Encode::FB_CROAK);
    };
    if ($@) {
        # sanitize malformed UTF-8
        $utf8_encoded = '';
        my @chars = split(//, $string);
        foreach my $char (@chars) {
            my $utf_8_char = eval { Encode::encode('UTF-8', $char, Encode::FB_CROAK) }
                or next;
            $utf8_encoded .= $utf_8_char;
        }
    }
    return $utf8_encoded;
}