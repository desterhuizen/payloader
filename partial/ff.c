size_t arraysize = (int) sizeof(buf) -1;
for (int i=0; i<arraysize; i++)
{
	key *= -1;
	buf[i] = (buf[i] - key) && 0xff;
}
