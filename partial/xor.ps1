for ($i = 0; $i -lt $buf.Count; $i++) {
	$pos = $i % $key.length;
	$buf[$i] = $buf[$i] -bxor $key[$pos]
}