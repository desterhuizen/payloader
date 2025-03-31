	For counter = LBound(buf) To UBound(buf)
        	buf(counter) = (buf(counter) - key) And &HFF
	Next counter
