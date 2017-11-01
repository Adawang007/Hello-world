#_*_coding:utf-8_*_
import re
'''读取目标文件并且按照行进行分割'''
def read_data_and_handle(path):
	content = open(path,'r').read()
	split_temp = content.split('\n')
	result = []
	#print content
	for i in split_temp:
		result.append(i.decode('gbk').replace('\n',''))
	return result
'''提取单条信息的出生地点'''
def get_birthpalce_singal(target):
	end_sign = ['。'.decode('gbk'),'！'.decode('gbk'),'；'.decode('gbk'),'？'.decode('gbk'),'，'.decode('gbk')]
	forward_list=["出生"]				#向前触发词
	later_list=["生于","出生于"]		#向后触发词
	both_list=["出生地点","出生地"]		#向两边扩展的触发词
	data_temp = target.split(" ")		#用空格将不同词性单词分开
	unicode_data = []					#存放中文单词
	attribute_data=[]					#存放对应单词的词法属性
	for i in data_temp:
		try:
			unicode_data.append(i[:i.index('/')])
			attribute_data.append(i[i.index('/')+1:])
		except:
			pass
		#print i[:i.index('/')]

	#处理前向触发词,case=1代表向前触发，case=2代表向后触发，case=3代表双向触发
	for pos in range(len(unicode_data)):
		find=0			#标记是否找到触发词
		case=0
		for enum in forward_list:
			if enum.decode('gbk')==unicode_data[pos]:
				find=1
				case=1
				break
		for enum in later_list:
			if enum.decode('gbk')==unicode_data[pos]:
				find=1
				case=2
				break
		for enum in forward_list:
			if enum.decode('gbk')==unicode_data[pos]:
				find=1
				case=3
				break
		if find==1:
			break
	#print pos,case
	#然后就是依据不同的case处理提取
	forward_words=""
	word_list_forward=[]		#存放向前触发词提取出数列的index值
	for index in range(pos-1,-1,-1):
		if unicode_data[index] in end_sign:
			break
		elif attribute_data[index]=="ns" or attribute_data[index]=="nsf":
			if len(word_list_forward)==0:
				forward_words+=unicode_data[index]
				word_list_forward.append(index)
			elif word_list_forward[len(word_list_forward)-1]-index>1:
				break
			else:
				forward_words+=unicode_data[index]
				word_list_forward.append(index)
	
	
	later_words=""
	word_list_later=[]		#存放向前触发词提取出数列的index值
	for index in range(pos+1,len(unicode_data)):
		if unicode_data[index] in end_sign:
			break
		elif attribute_data[index]=="ns" or attribute_data[index]=="nsf":
			if len(word_list_later)==0:
				later_words+=unicode_data[index]
				word_list_later.append(index)
			elif word_list_later[len(word_list_later)-1]-index>1:
				break
			else:
				later_words+=unicode_data[index]
				word_list_later.append(index)
	if case==1:
		return forward_words
	elif case==2:
		return later_words
	else:
		if forward_words=="" and  later_words=="":
			return ""
		elif forward_words=="" and  later_words!="":
			return later_words
		elif forward_words!="" and  later_words=="":
			return forward_words
		else:
			if pos-word_list_forward[0]<word_list_later[0]-index:
				return forward_words
			else:
				return later_words

def get_name_singal(target):
	data_temp = target.split(" ")		#用空格将不同词性单词分开
	unicode_data = []					#存放中文单词
	attribute_data=[]					#存放对应单词的词法属性
	for i in data_temp:
		try:
			unicode_data.append(i[:i.index('/')])
			attribute_data.append(i[i.index('/')+1:])
		except:
			pass
	for index in range(len(attribute_data)):
		if attribute_data[index]=="nr" or attribute_data[index]=="nz" or attribute_data[index]=="nrf":
			return unicode_data[index]
			break
	return ""
def main():
	path = 'C:\Users\Administrator\Desktop\Bigdata\people.txt'
	content = read_data_and_handle(path)
	for i in range(len(content)):
		birthplace=get_birthpalce_singal(content[i])
		username=get_name_singal(content[i])
		print str(i+1)+"."+username+" was born on "+birthplace

if __name__=='__main__':
	main()
