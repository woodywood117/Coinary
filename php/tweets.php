<?php
  require "twitteroauth/autoload.php";
  use Abraham\TwitterOAuth\TwitterOAuth;

  date_default_timezone_set('America/New_York');

  define("CONSUMER_KEY", "get consumer key from dev.twitter.com");
  define("CONSUMER_SECRET", "get consumer secret from dev.twitter.com");
  define("ACCESS_TOKEN", "get access token from dev.twitter.com");
  define("ACCESS_TOKEN_SECRET", "get access token secret from dev.twitter.com");

  define("COINARY_ACCESS_KEY", "defaultKeyChangeBeforeUse");

  if($_POST["coinaryaccesskey"] != COINARY_ACCESS_KEY) {
    exit(1);
  }

  $connection = new TwitterOAuth(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET);

  $query = array (
    "q" => "@".$_POST["handle"],
    "result_type" => "recent",
    "lang" => "en",
    "count" => $_POST["count"],
    "since_id" => $_POST["lastID"],
  );

  $content = $connection->get("search/tweets", $query);

  $csv_filename = $_SERVER['DOCUMENT_ROOT']."/tweets/".$_POST["handle"]."-".date("d.m.Y").".csv";
  $file = fopen($csv_filename, "a");

  $index = count($content->statuses);

  while($index) {
    $fileContents .= $content->statuses[--$index]->user->screen_name.",";
    $fileContents .= $content->statuses[$index]->id_str.",";
    $fileContents .= $content->statuses[$index]->created_at.",\"";
    $fileContents .= $content->statuses[$index]->text."\"\n";
  }

  $fileContents = str_replace("\n\n", "\n", $fileContents);
  fputs($file, $fileContents);

  fclose($file);

  echo $content->statuses[0]->id_str."\n";
?>
