for (int i = 0; i < buf.Length; i++)
{
    buf[i] = (byte)(((uint)buf[i] ^ key[i%key.Length]));
}