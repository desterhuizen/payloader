size_t arraysize = (int) sizeof(buf) -1;
size_t keysize = (int) sizeof(key) -1;
int i;
for (int i=0; i<arraysize; i++)
{
	buf[i] ^= key[i%keysize];
}
