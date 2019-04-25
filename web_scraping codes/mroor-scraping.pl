use WWW::Mechanize;
use strict;
use warnings;
use Data::Dumper;
use utf8;
use open qw(:std :utf8);

#==================== getting car data ==================================================#

use Encode qw(decode_utf8);
@ARGV = map { decode_utf8($_, 1) } @ARGV;

my $f_l = $ARGV[0];chomp $f_l; $f_l =~ s/empty_//;
my $s_l = $ARGV[1];chomp $s_l; $s_l =~ s/empty_//;
my $t_l = $ARGV[2];chomp $t_l; $t_l =~ s/empty_//;
my $nums = $ARGV[3];chomp $nums; $nums =~ s/empty_//;
#print $f_l."\n";
#print $s_l."\n";
#print $t_l."\n";
#print $nums."\n";

#========================================================================================#

#============================== scraping ================================================#
my $mech = WWW::Mechanize->new;

$mech->get('https://www.egypt.gov.eg/mobile/Services/NTPMOJ-GG/functions/PayFines.aspx');

# Submitting ..
my $response = $mech->submit_form(
  form_name => 'form1',
  fields => {
    'cSearch$txtPlateAlpaNum$txtFL' => $f_l ,
    'cSearch$txtPlateAlpaNum$txtSL' => $s_l ,
    'cSearch$txtPlateAlpaNum$txtTL' => $t_l ,
    'cSearch$txtPlateAlpaNum$txtDg' => $nums ,
  },
  button => 'cSearch$btnSearch',
);
#========================================================================================#


#========================================= reporting =====================================#
my $whole_report = $response->decoded_content(charset=>'utf8');

#succeded to bring it??
if ( $whole_report =~ m/<span id="cFinesSummary_lblTotalNew" class="keyword">(.+)?<\/span>/ ){
    # print "success\n" ;
    my $res =$1;
    if ($res =~ /لا يوجد/){
      print "no fines";
    }
    else{
      print $res;
    }
} else{
  print "failed getting car data";
}

#print $whole_report."\n";

#========================================================================================#


#========================================= debugging =====================================#
#get form names
# my $form =$mech->form_name('form1'); #hard coded
# my @inputfields = $form->param;
# foreach my $inputfield (@inputfields) {
#   print $inputfield."\n";
# }

# open(my $fh, '>', 'mroor-report.html');
# print $fh  $whole_report;
# close $fh;
# print "done\n";
#========================================================================================#
