<?php
// required headers
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Max-Age: 3600");
header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");
//==============
$fl = $_REQUEST['first_letter'];
if ( $fl=== "" ) { $fl = "empty_"; }
$sl = $_REQUEST['second_letter'];
if ( $sl === "" ) { $sl = "empty_"; }
$tl = $_REQUEST['third_letter'];
if ( $tl === "" ) { $tl = "empty_"; }
$ns= $_REQUEST['numbers'];
//file_put_contents($filename, $data);
$result = `perl mroor-scraping.pl $fl $sl $tl $ns`;
//===============
http_response_code(200);
echo json_encode([
	"result" => $result,
	"first_letter" => $fl,
	"second_letter" => $sl,
	"third_letter" => $tl,
	"numbers" => $ns
]);
