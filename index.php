
<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
  $name = $_POST["name"];
  $phone = $_POST["phone"];
  $ip = $_SERVER['REMOTE_ADDR'];
  // Запускаем Python-скрипт и передаем данные через pipe
  $command = "/usr/bin/python3 process_data.py";
  $descriptorspec = array(
    0 => array("pipe", "r"),  // stdin
    1 => array("pipe", "w"),  // stdout
    2 => array("pipe", "w")   // stderr
  );

  $process = proc_open($command, $descriptorspec, $pipes);

  if (is_resource($process)) {
    fwrite($pipes[0], $name . "\n");
    fwrite($pipes[0], $phone . "\n");
    fwrite($pipes[0], $ip . "\n");
    fclose($pipes[0]);

    $stdout = stream_get_contents($pipes[1]);
    $stderr = stream_get_contents($pipes[2]);
    fclose($pipes[1]);
    fclose($pipes[2]);

    $return_code = proc_close($process);

    if ($return_code == 0) {
      echo "Данные успешно отправлены в Python:
";
      echo "Вывод Python: " . htmlspecialchars($stdout) . "
";
    } else {
      echo "Ошибка при выполнении Python-скрипта:
";
      echo "Ошибка: " . htmlspecialchars($stderr) . "
";
    }
  } else {
    echo "Ошибка при запуске Python-скрипта";
  }
}
?>

<!DOCTYPE html>
<html>
<head>
<title>Отправка данных в Python</title>
</head>
<body>

<form method="post">
  Имя: <input type="text" name="name">

  Телефон: <input type="text" name="phone">

  <input type="submit" value="Отправить">
</form>

</body>
</html>
