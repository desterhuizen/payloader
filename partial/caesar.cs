for (int i = 0; i < buf.Length; i++)
{
    buf[i] = (byte)(((uint)buf[i] - key)&&0xff);
}
