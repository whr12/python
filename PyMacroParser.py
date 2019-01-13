# -*- coding: cp936 -*-

numsuffix = ('u','l','i64','ui64','ll');
escape_sequence = {'a':'\a','b':'\b','f':'\f','n':'\n','r':'\r','t':'\t','v':'\v','\'':'\'','\"':'\"','\\':'\\','?':'?'};
rescape_sequence = {'\a':'\\a','\b':'\\b','\f':'\\f','\n':'\\n','\r':'\\r','\t':'\\t','\v':'\\v','\'':'\\\'','\"':'\\\"','\\':'\\\\','?':'\\?'};

oct_digit = ('0','1','2','3','4','5','6','7');
hex_digit = ('0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','a','b','c','d','e','f');

class PyMacroParser:

    
    def __init__(self):
        self.__preData = dict();            #store the macro names and values
        self.__sData = list();              #store the predefined macro names     
        self.__mark = False;                #the flag whether the dict of .__preData has maked

        self.__preDirective = list();       #store the preprocessor directives in the cpp files

    def load(self, f):
        '''
        P.load(self filename) --> null

        load a cpp file and store the preprocessor directives in .__preDirective and return nothing.
        
        ._preDirective is a list whose value is a list that represent a preprocessor directives.
        The structure of the preprocessor directives is as follows:
        the 0th value is a number that represent the preprocessor keywords.
                0  -->  #define
                1  -->  #undef
                2  -->  #ifdef or #ifndef
                3  -->  #else
        the following value of the list is depend on the directive in the 0th value.
        Usually, the middle values stores the argument of a directive and the last value store the index of the next directive in .__preDirective.
        #define
                index           value
                    0           0
                    1           macro name
                    2           macro value(None if value is null)
                    3           index of next directive
        #undef
                index           value
                    0           0
                    1           macro name
                    2           index of next directive
        #ifdef or ifndef
                index           value
                    0           0
                    1           macro name
                    2           boolean value that marks the condition(True means #ifdef and False is #ifndef)
                    3           index of the true condition(condition is equal to the 2th value)
                    4           index of the false condition
        #else
                index           value
                    0           0
                    1           index of next directive
                
        '''
        self.__mark = False;
    	inFile = open(f,'r');
    	lines = self.__readNextPre(inFile);
    	cnt = 0;
    	ifstack = list();
    	while(lines):
            strList = lines.split(None,2);
            directive = list();
            if(strList[0] == "define"):
                if(len(strList)>=2):
                    cnt = cnt+1;
                    directive.append(0);
                    directive.append(strList[1]);
                    if(len(strList)==3):
                        directive.append(self.__analysis(strList[2]));
                    else:
                        directive.append(None);
                    directive.append(cnt);
                    self.__preDirective.append(directive);
            elif(strList[0]=="undef"):
                cnt = cnt+1;
                directive.append(1);
                directive.append(strList[1]);
                directive.append(cnt);
                self.__preDirective.append(directive);
            elif(strList[0]=="ifdef"):
                directive.append(2);
                directive.append(strList[1]);
                directive.append(True);
                ifstack.append(cnt);
                cnt = cnt+1;
                directive.append(cnt);
                directive.append(None);
                self.__preDirective.append(directive);

            elif(strList[0]=="ifndef"):
                directive.append(2);
                directive.append(strList[1]);
                directive.append(False);
                ifstack.append(cnt);
                cnt = cnt+1;
                directive.append(cnt);
                directive.append(None);
                self.__preDirective.append(directive);

            elif(strList[0]=="else"):
                directive.append(3);
                directive.append(None);
                lastif = ifstack[-1];
                ifstack[-1] = cnt;
                self.__preDirective.append(directive);
                cnt = cnt+1;
                self.__preDirective[lastif][-1] = cnt;
            elif(strList[0]=="endif"):
                lastif = ifstack.pop();
                self.__preDirective[lastif][-1] = cnt;
            lines = self.__readNextPre(inFile);
        inFile.close();
        return;

    def __readNextPre(self,inFile):
        '''
        P.__readNextPre(inFile) --> string

        Return the next preprocessor directive string with comment and leading and trailing whitespace and '#'
        removed in inFile. If no directives remains in inFile, return an empty string.
        '''
        lines = inFile.readline();
        while(lines):
            left = 0;
            i = 0;
            charMark = False;
            strMark = False;
            length = len(lines);
            newLine = "";
            while(i<length):
                c = lines[i];
                if(c=='"'):
                    if(charMark): pass;
                    else: strMark = not strMark;
                elif(c=="'"):
                    if(strMark): pass;
                    else: charMark = not charMark;
                elif(c=='\\'):
                    i = i+1;
                elif(c=='/'):
                    if(charMark or strMark): pass;
                    else:
                        if(lines[i+1]=='*'):
                            newLine = newLine+lines[0:i]+" ";
                            index = lines.find("*/",i+2);
                            while(index<0):
                                lines = inFile.readline();
                                index = lines.find("*/");
                            lines = lines[index+2:];
                            i = -1;
                            length = len(lines);
                        elif(lines[i+1]=='/'):
                            lines = lines[0:i];
                            break;
                        else:   raise Exception(); 
                i = i+1;
            lines = newLine+lines;
            lines = lines.strip();
            if(lines and lines[0]=='#'):
                lines = lines[1:].rstrip(';').strip();
                break;
            else:
                lines = inFile.readline();
        return lines;

    def __analysis(self,valueStr):
        '''
        P.__analysis(string) --> object

        Return a python object according to the string(valueStr).
            type of valueStr present            return
            Integer(int, long etc)              int
            float and double                    float
            char                                int
            string                              string
            wide-string                         unicode
            {...}                               tuple
        '''
        length = len(valueStr);
        if(length==0): return None;
    
        if(valueStr=="true"): return True;
        if(valueStr=="false"): return False;
        
        index = valueStr.find("'");
        if(index==0):
            endindex = valueStr.rfind("'");
            return self.__ord(valueStr[index+1:endindex]);
        elif(index==1 and (valueStr[0]=='L' or valueStr[0]=='l')):
            endindex = valueStr.rfind('"');
            return self.__ord(valueStr[index+1:endindex]);
        
        index = valueStr.find('"');
        if(index==0):
            endindex = valueStr.rfind('"');
            return self.__str(valueStr[index+1:endindex]);
        elif(index==1 and (valueStr[0]=='L' or valueStr[0]=='l')):
            endindex = valueStr.rfind('"');
            return self.__unicode(valueStr[index+1:endindex]);
        
        if(valueStr[0]=='{'):
            return self.__str2tuple(valueStr[1:length-1]);
        
        numstr = valueStr.lower();
        
        endindex = length;
        for suffix in numsuffix:
            index = numstr.rfind(suffix);
            if(index>=0 and index<endindex):
                endindex = index;
        numstr = numstr[0:endindex];
        
        if(numstr.find("0x")>=0):
            return int(numstr,16);
        
        if(numstr.find('.')>=0):
            if(numstr[-1]=='f' or numstr[-1]=='l'):
            	return float(numstr[0:length-1]);
            else:
                return float(numstr);
        if(numstr.find('e')>=0):
            if(numstr[-1]=='f' or numstr[-1]=='l'):
                return float(numstr[0:length-1]);
            else:
            	return float(numstr);
        
        if(numstr[0]=='0'):
            return int(numstr,8);
        if(numstr[0]=='+' or numstr[0]=='-'):
            if(numstr[1]=='0'):
                return int(numstr,8);
            else:
                return int(numstr);
        return int(numstr);

    def __str2tuple(self,valueStr):
        '''
        P.__str2tuple(string) --> tuple

        return tuple that the valueStr presents.If valueStr is an empty string, return an empty tuple.
        '''
    	valueStr = valueStr.strip();
        length = len(valueStr);
        if(length==0): return tuple();
        li = list();
        i = 0;
        left = 0;
        charMark = False;
        strMark = False;
        bracecnt = 0;
        while(i<length):
            c = valueStr[i];
            
            if(c=="'"):
                if(strMark):
                    pass;
                else:
                    charMark = not charMark;
            
            elif(c=='"'):
                if(charMark):
                    pass;
                else:
                    strMark = not strMark;
            
            elif(c=='\\'):
            	if(charMark or strMark):
            	    i = i+1;

            elif(c=='{'):
                if(charMark or strMark):
                    pass;
                else:
                    bracecnt = bracecnt+1;
            elif(c=='}'):
                if(charMark or strMark):
                    pass;
                else:
                    bracecnt = bracecnt-1;
            
            elif(c==','):
                if(charMark or strMark or bracecnt):
                    pass;
                else:
                    value = valueStr[left:i];
                    value = value.strip();
                    value = self.__analysis(value);
                    li.append(value);
                    left = i+1;
            i = i+1;
        
        value = valueStr[left:];
        value = value.strip();
        if(value):
            value = self.__analysis(value);
            li.append(value);
        return tuple(li);

    def __ord(self,valueStr):
        '''
        P.__ord(string) --> int

        return the numerical value of the character interpreted as an integer.
        if the length of valueStr is more than 1, only the last character that valueStr presents is used.
        '''
        
        length = len(valueStr);
        index = valueStr.rfind('\\');
        if(index<0): return ord(valueStr[-1]);
        if(index>0 and valueStr[index-1]=='\\'): return ord(valueStr[-1]);
        err = length-index;
        if(err==2):
            if(valueStr[-1] in oct_digit): return int(valueStr[-1],8);
            return ord(escape_sequence.get(valueStr[-1],valueStr[-1]));
        if(err==3):
            if(valueStr[-2] in oct_digit and valueStr[-1] in oct_digit): return int(valueStr[-2:],8);
            elif(valueStr[-2]=='x'): return int(valueStr[-1],16);
        elif(err==4):
            if(valueStr[-3] in oct_digit and valueStr[-2] in oct_digit and valueStr[-1] in oct_digit): return int(valueStr[-3:],8);
            elif(valueStr[-3]=='x'): 
                if(valueStr[-2] in hex_digit and valueStr[-1] in hex_digit): return int(valueStr[-2:],16);
        elif(err==5):
            if(valueStr[-4]=='x'):
                if(valueStr[-3] in hex_digit and valueStr[-2] in hex_digit and valueStr[-1] in hex_digit): return int(valueStr[-3:],16);
        return ord(valueStr[-1]);

    def __str(self,valueStr):
        '''
        P.__str(string) --> string

        Return a string with all escape sequences parsed to their original characters in valueStr.
        '''
        length = len(valueStr);
        hexcnt = 0;
        octcnt = 1;
        value = "";
        left = 0;
        i = 0;
        while(i<length):
            c = valueStr[i];
            if(c=='\\'):
                if(valueStr[i+1] in escape_sequence.keys()):
                    value = value+valueStr[left:i]+escape_sequence[valueStr[i+1]];
                    left = i+2;
                    i = i+1;
                elif(valueStr[i+1]=='x'):
                    hexcnt = i+2;
                    while(hexcnt<length and valueStr[hexcnt] in hex_digit):
                        hexcnt = hexcnt+1;
                    value = value+valueStr[left:i]+chr(int(valueStr[i+2:hexcnt],16));
                    left = hexcnt;
                    i = hexcnt-1;
                elif(valueStr[i+1] in oct_digit):
                    octcnt = 2;
                    while(i+octcnt<length and valueStr[i+octcnt] in oct_digit):
                        octcnt = octcnt+1;
                        if(octcnt>3): break;
                    value = value+valueStr[left:i]+chr(int(valueStr[i+1:i+octcnt],8));
                    left = i+octcnt;
                    i = i+octcnt-1;
                else:
                    value = value+valueStr[left:i];
                    left = i+1;
            elif(c=='"'):
                value = value+valueStr[left:i];
                lll = i+1;
                i = valueStr.find('"',i+1);
                if(i<0): break;
                rrr = i;
                left = i+1;
            i = i+1;
        value = value+valueStr[left:];
        return value;


    def __unicode(self,valueStr):
        '''
        P.__unicode(string) --> unicode

        Return a unicode string with all escape sequences parsed to their original characters in valueStr.
        '''
        length = len(valueStr);
        hexcnt = 0;
        octcnt = 1;
        value = u"";
        left = 0;
        i = 0;
        while(i<length):
            c = valueStr[i];
            if(c=='\\'):
                if(valueStr[i+1] in escape_sequence.keys()):
                    value = value+unicode(valueStr[left:i])+unicode(escape_sequence[valueStr[i+1]]);
                    left = i+2;
                    i = i+1;
                elif(valueStr[i+1]=='x'):
                    hexcnt = i+2;
                    while(hexcnt<length and valueStr[hexcnt] in hex_digit):
                        hexcnt = hexcnt+1;
                    value = value+unicode(valueStr[left:i])+unichr(int(valueStr[i+2:hexcnt],16));
                    left = hexcnt;
                    i = hexcnt-1;
                elif(valueStr[i+octcnt] in oct_digit):
                    octcnt = octcnt+1;
                    while(i+octcnt<length and valueStr[i+octcnt] in oct_digit):
                        octcnt = octcnt+1;
                        if(octcnt>3): break;
                    value = value+unicode(valueStr[left:i])+unichr(int(valueStr[i+1:i+octcnt],8));
                    left = i+octcnt;
                    i = i+octcnt-1;
                else:
                    value = value+unicode(valueStr[left:i]);
                    left = i+1;
            elif(c=='"'):
                value = value+unicode(valueStr[left:i]);
                i = i+1;
                left = i+1;
            i = i+1;
        value = value+unicode(valueStr[left:]);
        return value;

    def preDefine(self, s):
        '''
        P.preDefine(string) --> null

        parse the string s and store the predefined macro name in a private list.
        '''
        self.__mark = False;
        self.__sData = list();
        for preDef in s.split(";"):
            if(preDef):
                self.__sData.append(preDef.strip());
        return;

    def dumpDict(self):
        '''
        P.dumpDict() --> dict

        return a dict that stores the macro names and values parsing from preDefine and cpp files.
        '''
        if(not self.__mark):
            self.__makeDict();
        __preDefDic = dict();
        for key in self.__preData:
            __preDefDic[key] = self.__preData[key];

        return __preDefDic;

    def __makeDict(self):
        '''
        P.__makeDict() --> null

        parse the .__preDirective with .__sData from preDefine, and store the result in .__preData.
        '''
        self.__preData = dict();
        for key in self.__sData:
            self.__preData[key] = None;
        length = len(self.__preDirective)
        i = 0;
        while(i<length):
            directive = self.__preDirective[i];
            #define
            if(directive[0]==0):
                self.__preData[directive[1]] = directive[2];
                i = directive[3];
            #undef
            elif(directive[0]==1):
                self.__preData.pop(directive[1],None);
                i = directive[2];
            #if
            elif(directive[0]==2):
                if(self.__preData.has_key(directive[1])==directive[2]):
                    i = directive[3];
                else:
                    i = directive[4];
            #else
            elif(directive[0]==3):
                i = directive[1];
            else:
                raise Exception();
        self.__mark = True;


    def dump(self, f):
        '''
        P.dump(filename) --> null

        Create a cpp file named filename, and write the #define directives to it.
        '''
        __preDefDic = self.dumpDict();
        outFile = open(f,'w');
        for key in __preDefDic.keys():
            if(__preDefDic[key]!=None):
                valueStr = self.__outputStr(__preDefDic[key]);
                outFile.writelines("#define "+key+" "+valueStr+"\n");
            else:
                outFile.writelines("#define "+key+"\n");
        outFile.close();
        return

    def __outputStr(self,value):
        '''
        P.__outputStr(value) --> string

        return the string that represents a macro value of the object value.
        '''
        valueStr = str(value);
        if(isinstance(value,bool)):
            if(value): valueStr = "true";
            else: valueStr = "false";
        elif(isinstance(value,tuple)):
            valueStr = self.__outputtuple(value);
        elif(isinstance(value,str)):
            valueStr = "\""+self.__strout(valueStr)+"\"";
        elif(isinstance(value,unicode)):
        	valueStr = "L\""+self.__strout(valueStr)+"\"";
        elif(value==None):
        	valueStr = "";
        return valueStr;

    def __outputtuple(self,tup):
        '''
        P.__outputtuple(tuple) --> string

        return the string that represents a macro value of the tuple
        '''
        
        valueStr = '{';
        length = len(tup)
        if(length>0):
            i=0;
            valueStr += self.__outputStr(tup[i]);
            i += 1;
            while(i<length):
                valueStr += ','+ self.__outputStr(tup[i]);
                i += 1;
        
        valueStr = valueStr+'}';
        return valueStr;

    def __strout(self,valueStr):
        '''
        P.__strout(tuple) --> string

        return the string that represents a macro value of the string(valueStr)
        '''
        length = len(valueStr);
        left = 0;
        i = 0;
        value = '';
        while(i<length):
            c = valueStr[i];
            if(c in rescape_sequence.keys()):
                value = value+valueStr[left:i]+rescape_sequence[c];
                left = i+1;
            i = i+1;
        value = value+valueStr[left:];
        return value;






    
        
