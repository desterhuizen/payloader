For counter = LBound(buf) To UBound(buf)
		pos = counter Mod Len(key)
		buf(counter) = buf(counter) Xor Asc(Left(Mid(key, pos + 1), 1))
	Next counter
