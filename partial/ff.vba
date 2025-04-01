For counter = LBound(buf) To UBound(buf)
		en_key = en_key * -1
		buf(counter) = (buf(counter) - en_key) And &HFF
	Next counter
