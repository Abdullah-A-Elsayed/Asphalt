<?php


// required headers
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");
header('Cache-Control: no-cache, must-revalidate');
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Max-Age: 3600");
header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");

//==============================================
// file handeling

if(! isset($_FILES['img']['tmp_name'])) {
   echo json_encode (['result' => "error upload image"]);
   exit;
}

//===============================================

// temp path not saved
$imgpath = $_FILES['img']['tmp_name'];
//$imgpath = '/var/www/html/ocrapi/imgs/sample11.jpg';
//run command and connect to api on server
$result = `python /var/www/html/ocrapi/api.py $imgpath`;
// remove extra \n from result
$result = trim(preg_replace('/\s+/', '', $result));


// splitting numbers from letters
$letters = "";
$ns = "";
$ar_array = str_split($result);

foreach ($ar_array as $char) {
 if(preg_match("/[0-9]/", $char)){
    $ns = $ns . $char;
  } else{
    $letters = $letters . $char;
 }
}


// splitting letters ...
$let_arr = str_split($letters);
$l_len = count($let_arr);

$fl = $let_arr[$l_len - 1]; $sl ="" ; $tl = "";
if($l_len > 1 ){
        $sl= $let_arr[$l_len - 2] ;
}
if($l_len > 2){
        $tl= $let_arr[$l_len - 3] ;
}


// translate to arrabic
translate($fl, $fl);
translate($sl, $sl);
translate($tl, $tl);

//getting fines from smart api
$link = "http://85.187.140.233/api/?first_letter=$fl&second_letter=$sl&third_letter=$tl&numbers=$ns";
$curl = curl_init();

curl_setopt_array($curl, array(
  CURLOPT_URL => $link,
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "GET",
  CURLOPT_HTTPHEADER => array(
    "cache-control: no-cache"
  ),
));
$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);
//var_dump($response);

//sending results ...
http_response_code(200);
echo $response;


function translate($source,&$ar_result)
                {
                        // lowercase it all to start with
                        //$source = strtolower($source);
                        // start by looking for the 8 letters that have an approximate equivalent in arabic
                        // these are B,F,K,L,M,N,R and Z
                                // hack to pick out i
                        if(strlen($source) == 1)
                        {
                                if($source=='i')
                                {
                                        $ar_result ="آ ";
                                }
                        }
                        // check for arabic chars in
                        // remove all the vowels unless they're doubled up or u or ie
                        for ($i = 0; $i < strlen($source); $i++)
                        {
                                $char = substr($source, $i, 1);
                                // check for arabic characters in the string and just output them if they exist
                                if(ord(substr($source, 0, 1))==216 || ord(substr($source, 0, 1))==217)
                                {
                                        $ar_result =substr($source, $i, 2);
                                        $i++;
                                        continue;
                                }
                                $char = strtolower($char);
                                switch($char)
                                {
                                        case 'a':
                                                $ar_result ='ا '; // alif
                                        break;
                                        case 'b':
                                                $ar_result = 'ب'; // bah
                                        break;
                                        case 'c':
                                                $ar_result = 'ص' ;// sad
                                        break;
                                        case 'd':
                                                $ar_result = 'د'; // dal
                                        break;
                                        case 'e':
                                                $ar_result = 'ي'; // yeh
                                        break;
                                        case 'f':
                                                $ar_result = 'ف'; // feh
                                        break;
                                        case 'g':
                                                $ar_result = 'ج'; // ghaim
                                        break;
                                        case 'h':
                                                $ar_result = 'ه'; // heh
                                        break;
                                        case 'i':
                                                $ar_result = 'ي'; // yeh
                                        break;
                                        case 'j':
                                                $ar_result = 'ج'; // jeem
                                        break;
                                        case 'k':
                                                $ar_result = 'ك'; // kaf
                                        break;
                                        case 'l':
                                                $ar_result = 'ل'; // lam
                                        break;
                                        case 'm':
                                                $ar_result = 'م'; // meem
                                        break;
                                        case 'n':
                                                $ar_result = 'ن'; // noon
                                        break;
                                        case 'o':
                                                $ar_result = 'و'; // waw
                                        break;
                                        case 'p':
                                                $ar_result = 'ب'; // beh
                                        break;
                                        case 'q':
                                                $ar_result = 'ك'; // kah
                                        break;
                                        case 'r':
                                                $ar_result = 'ر'; // reh
                                        break;
                                        case 's':
                                                $ar_result = 'س'; // seen
                                        break;
                                        case 't':
                                                $ar_result = 'ط'; // tah
                                        break;
                                        case 'u':
                                                $ar_result = 'و'; // waw
                                        break;
                                        case 'v':
                                                $ar_result = 'ڤ'; // veh
                                        break;
                                        case 'w':
                                                $ar_result = 'و'; // waw
                                        break;
                                        case 'x':
                                                $ar_result = 'كس'; // kaf and seen
                                        break;
                                        case 'y':
                                                $ar_result = 'ي'; // yeh
                                        break;
                                        case 'z':
                                                $ar_result = 'ز'; // zain
                                        break;
                                        default:
                                                $ar_result = $char;
                                        break;
                                }
                        }
                }


?>