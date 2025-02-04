int arraysize = (int) sizeof(buf);
for (int i=0; i<arraysize-1; i++)
{
    buf[i] = buf[i]^xor_key;
}