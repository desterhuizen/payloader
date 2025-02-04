    For counter = LBound(buf) To UBound(buf)
		pos = counter Mod Len(en_key)
        buf(counter) = buf(counter) Xor Asc(Left(Mid(en_key, pos + 1), 1))
	Next counter