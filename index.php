<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
  $name = $_POST["name"];
  $phone = $_POST["phone"];
  $ip = $_SERVER['REMOTE_ADDR'];

  $escaped_name = htmlspecialchars($name, ENT_QUOTES, 'UTF-8');
  $escaped_phone = htmlspecialchars($phone, ENT_QUOTES, 'UTF-8');

  $command = "/usr/bin/python3 gate_for_php.py";
  $descriptorspec = array(
    0 => array("pipe", "r"),
    1 => array("pipe", "w"),
    2 => array("pipe", "w")
  );

  $process = proc_open($command, $descriptorspec, $pipes);

  fwrite($pipes[0], $escaped_name . "\n");
  fwrite($pipes[0], $escaped_phone . "\n");
  fwrite($pipes[0], $ip . "\n");
  fclose($pipes[0]);

  $stdout = stream_get_contents($pipes[1]);
  fclose($pipes[1]);
  fclose($pipes[2]);

  proc_close($process);
}
?>

<!DOCTYPE html>
<html>
<head>
<title>Отправка данных в Python</title>
</head>
<body>
<form method="post">
  Имя: <input type="text" name="name"><br>
  Телефон: <input type="text" name="phone"><br>
  <input type="submit" value="Отправить">
</form>
</body>
</html>
