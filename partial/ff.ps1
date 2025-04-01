for ($i = 0; $i -lt $buf.Count; $i++) {
	$buf[$i] = ($buf[$i] - $key) -band 0xff
}
