<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $len = $_POST['length'];
    $vars = $_POST['vars'];
    $vars = array_map('trim', str_getcsv($vars));
    $wsv = implode(" ", $vars);
    $dh = $_POST['interval'];
    $date = $_POST['date'];
    $date = str_replace('-', '', $date)."00";
    $file = $_FILES['nc']['tmp_name'];
    $hash = uniqid();

    mkdir("_nc/${hash}", 0777, true);
    move_uploaded_file($file, "_nc/${hash}/${date}.nc");
    system("cd scripts && python palette.py --time ${date} --dhour ${dh} --items ${wsv} -f --src ../_nc/${hash} --dest ../hash/${hash}");
    $schema = ['names' => [$date], 'items' => $vars, 'dh' => $dh, 'length' => $len];
    $json = fopen("hash/${hash}/dataset.json", "w");
    fwrite($json, json_encode($schema));
    fclose($json);
    header("Location: index.html?hash=${hash}");
    die();
}
?>

<!DOCTYPE html>
<html lang="en"><head>
  <meta http-equiv="content-type" content="text/html; charset=UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Upload netcdf</title>
  <!-- bootstrap -->
  <link rel="stylesheet" href="css/bootstrap.css">
  <script src="js/bootstrap.js"></script>
</head>
<body>
  <div class="container">
      <div class="col-md-6 col-md-offset-3">
    <br><br> <!-- Orz -->
    <h1>Upload your netcdf</h1>
    <form method="post" enctype="multipart/form-data">
      <div class="form-group">
        <label><h3>File Name:</h3></label>
        <input class="form-control-file" name="nc" accept=".nc" required="" type="file">
      </div>
      <div class="form-group">
        <label><h3>Start date:</h3></label>
        <input class="form-control" name="date" placeholder="2016-12-01" required="" type="date">
      </div>
      <div class="form-group">
        <label><h3>Variable names:</h3></label>
        <input class="form-control" name="vars" placeholder="var1, var2" required="" type="text">(in csv)
      </div>
      <div class="form-group">
        <label><h3>Length of each record:</h3></label>
        <input class="form-control" name="length" placeholder="180" required="" type="text">
      </div>
      <div class="form-group">
        <label><h3>Interval:</h3></label>
        <input class="form-control" name="interval" min="1" value="6" required="" type="number"> (in hours)
      </div>
      <button class="btn btn-primary">Submit</button>
    </form>
  </div>
  </div>
</body>
</html>
