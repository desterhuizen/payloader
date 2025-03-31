	For counter = LBound(buf) To UBound(buf)
		key = key * -1
		buf(counter) = (buf(counter) - key) And &HFF
	Next counter
