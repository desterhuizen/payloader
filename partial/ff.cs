for (int i = 0; i < buf.Length; i++)
{
    key *= -1
    buf[i] = (byte)(((uint)buf[i] - key) && 0xff);
}
