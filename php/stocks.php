<?php
  date_default_timezone_set('America/New_York');

  define("COINARY_ACCESS_KEY", "defaultKeyChangeBeforeUse");

  if($_POST["coinaryaccesskey"] != COINARY_ACCESS_KEY) {
    exit(1);
  }

  $csv_filename = "stocks-".$_POST["ticker"]."-".date("d.m.Y").".csv";
  $file = fopen($csv_filename, "a");

  $fileContents .= $_POST["data"]."\n";

  fputs($file, $fileContents);
  fclose($file);
?>
