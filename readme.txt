class PyMacroParser: 
    ���Խ���cpp�ļ����������е�Ԥ����ָ��ĺ궨�壬����������յ���cpp�ļ��о�����ͬ�궨���cpp�ļ���
�����ӿڣ�
    load(f):
	����һ���ַ�������ʾΪҪ�����cpp�ļ��������ļ��к궨��������ݻ��浽����ı����У�����֮�����
    preDefine(s)
	����һ���ַ������ַ����а�';'�ָ��ַ�������ΪԤ����꣬����ʱ�����ͷ��
    dumpDict()
	���ݽ��յ�cpp�ļ��Լ�Ԥ����꣬�����ۺϺ��еĺ꼰���ֵ������Ϊdict������Ϊ������ֵΪֵ��
    dump(f)
	�����ļ���Ϊf��cpp�ļ������ļ��а��������б����˵ĺ궨�塣

˽�г�Ա��
    __preData: ���ڱ��������ĺ궨��
    __sData: ���ڱ���Ԥ����ĺ���
    __mark: ������ɱ�־����ΪTrue����ֱ�Ӵ�__preData����ȡ���ݣ������ظ�����
    __preDirection: ���ڻ���cpp�ļ��е�Ԥ����ָ��

    __readNextPre(inFile):
	��ȡinFile�е����ݣ�������һ����Ԥ����ָ����ַ���
    __analysis(valueStr):
	�����ַ���valueStr������ת��Ϊ��Ӧ��python���ͷ���
    __str2tuple(valueStr):
	�����ַ���valueStr����cpp�еľۺ�תΪtuple
    __ord(valueStr):
	���ַ�valueStrת��Ϊint
    __str(valueStr):
	���ַ���valueStrת��Ϊstr
    __unicode(valueStr):
	���ַ���valueStrת��Ϊunicode
    __makeDict():
	����__sData��__preDirection�е����ݣ�����__preData.
    __outputStr(value):
	��valueֵת��Ϊ���ʵ�cpp�ļ��е��ַ�����ʽ���
    __outputtuple(tup):
	���ۺ�tupת��Ϊcpp�еľۺ���ʽ���
    __strout(valueStr):
	���ַ���valueStrת��Ϊcpp�ļ��е��ַ������
	