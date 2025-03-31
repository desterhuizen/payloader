size_t arraysize = (int) sizeof(buf) -1;
size_t keysize = (int) sizeof(xor_key) -1;
int i;
for (int i=0; i<arraysize; i++)
{
	buf[i] ^= xor_key[i%keysize];
}
