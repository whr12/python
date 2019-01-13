class PyMacroParser: 
    可以接收cpp文件并解析其中的预处理指令的宏定义，并生成与接收到的cpp文件中具有相同宏定义的cpp文件。
公共接口：
    load(f):
	接收一个字符串，表示为要载入的cpp文件名。将文件中宏定义相关内容缓存到对象的变量中，用于之后解析
    preDefine(s)
	接收一个字符串，字符串中按';'分隔字符串，作为预定义宏，解析时放至最开头。
    dumpDict()
	根据接收的cpp文件以及预定义宏，返回综合后含有的宏及宏的值，返回为dict，宏名为键，宏值为值。
    dump(f)
	生成文件名为f的cpp文件，该文件中包含对象中保存了的宏定义。

私有成员：
    __preData: 用于保存解析后的宏定义
    __sData: 用于保存预定义的宏名
    __mark: 解析完成标志，若为True，则直接从__preData中提取数据，不再重复解析
    __preDirection: 用于缓存cpp文件中的预处理指令

    __readNextPre(inFile):
	读取inFile中的内容，返回下一条含预处理指令的字符串
    __analysis(valueStr):
	解析字符串valueStr，将其转换为对应的python类型返回
    __str2tuple(valueStr):
	解析字符串valueStr，将cpp中的聚合转为tuple
    __ord(valueStr):
	将字符valueStr转换为int
    __str(valueStr):
	将字符串valueStr转换为str
    __unicode(valueStr):
	将字符串valueStr转换为unicode
    __makeDict():
	根据__sData及__preDirection中的内容，生成__preData.
    __outputStr(value):
	将value值转换为合适的cpp文件中的字符串形式输出
    __outputtuple(tup):
	将聚合tup转换为cpp中的聚合形式输出
    __strout(valueStr):
	将字符串valueStr转换为cpp文件中的字符串输出
	