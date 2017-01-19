<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);
date_default_timezone_set('America/Chicago');
require 'Predis/Autoloader.php';
use Predis\Collection\Iterator;
Predis\Autoloader::register();
$date = new DateTime();
$timestamp=$date->getTimestamp();
$curr_date=date_format($date, 'Y/m/d H:i:s');
$curr_date_min=date_format($date, 'Y/m/d H:i');
$hostname=gethostname();

if (isset($_GET['cmd']) === true) {
  $host = 'redis-master';
  if (getenv('GET_HOSTS_FROM') == 'env') {
    $host=getenv('REDIS_MASTER_SERVICE_HOST');
  }
  header('Content-Type: application/json');
  switch ($_GET['cmd']){
  case 'get':
       $host = 'redis-slave';
       if (getenv('GET_HOSTS_FROM') == 'env') {
        $host = getenv('REDIS_SLAVE_SERVICE_HOST');
       }
       $client = new Predis\Client([
        'scheme' => 'tcp',
        'host'   => $host,
        'port'   => 6379,
       ]);
       $value = $client->get($_GET['key']);
       $array=explode("@",$value);
       foreach($array as $element){
         if (!empty($element)){
           $element_arr=explode("=",$element);
    	   if ($element_arr[0]==$hostname)
             print $element_arr[0]." is ".$element_arr[1];
         }
       }
       break;
  default:
       print('http://host/map.php?cmd=set&key=key1&value=val1'.PHP_EOL);
  }
}else
  phpinfo();
?>
