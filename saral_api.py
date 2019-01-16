import requests
import json
import os
import pprint

# This is our main url of api 
saral_api_url = "http://saral.navgurukul.org/api/courses"

def user():
	choice_user = int(input("Enetr Index number of Course: ")) 
	return choice_user

# Here we grab the slug of child_exercises.
def slug_api(user_input,slug):
	path = 'request_data/exercise_slug/exercise_' + str(user_input)
	os.mkdir(path)
	for s in slug:
		exercises_url = saral_api_url +"/" + str(user_input) + '/exercise'
		slug_url = exercises_url + '/getBySlug?slug=' + s
		slug_requests = requests.get(slug_url)
		slug1 = ''
		for i in s:
			if '/' not in i:
				slug1 += i
			else:
				slug1 +='_'
		file_name = slug1 + '.json'
		
		with open( path + "/" + file_name ,'w') as file3:
			json.dump(slug_requests.text,file3)

# Here we read the child exercises of saral_api_url
def read_child_exercise(user_input):
	file_name = 'request_data/course_exe/exercises_'+ str(user_input) + '.json'
	with open(file_name,'r') as file2:
		raw = file2.read() # the type of raw is unicode_type
		unicode_s = json.loads(raw) # The type of unicode_s is also unicode_type of string_type.
		text = json.loads(unicode_s) # The type of text is dic_type
		data = text['data']
		slugs = []
		for i in (data):
			parent_exe = i['name']
			child_exe = i['childExercises']
			child_slug = i['slug']
			slugs.append(child_slug)
			index = 1
			for j in child_exe:
				sub_exe = j['name']
				if index == 1:
					print('---------' + parent_exe + '---------')
					print('     ' + str(index) + '.' + sub_exe)
				else:
					print('     '+ str(index) + '.' + sub_exe)
				index+=1
	return slugs

# Here we grab the child exercises from sarl_api_url
def child_exe(user_input):
	file_name = 'request_data/course_exe/exercises_'+ str(user_input) + '.json'
	debug = False
	text = None
	if os.path.exists(file_name):
		debug =  True
		read_child_exercise(user_input)

	if debug is False:
		exercises_url = saral_api_url +"/" + str(user_input) + '/exercises'
		api_2 = requests.get(exercises_url)
		raw = json.dumps(api_2.text)
		file1 = open(file_name,'w')
		file1.write(raw)
		file1.close()

		# The read_child_exercise() return the slugs list  
		slugs = read_child_exercise(user_input)
		# Here we call the function called slug_api and passes user_input & slugs as argument in this function
		slug_api(user_input,slugs)
		

# Here we create some empty list
user_choice_list = []	
course_id_list = []
course_dic = {}
# Here We read the course.json file.
def read_course():
	file_name = 'request_data/course.json'
	with open(file_name,'r') as file1:
		raw = file1.read() # the type of raw is unicode_type
		s = json.loads(raw) # The type of s is also unicode_type
		text = json.loads(s) # The type of dic is dic_type
		# dic = ast.literal_eval(s) # Here we are directly convert unicode_type to dic_type in json
		course = text['availableCourses']
		for i in range(len(course)):
			course_id = course[i]['id']
			course_id_list.append(course_id)
			course_name = course[i]['name']
			course_dic[course_id] = course_name
			print(i+1,course_name)
		user_choice = user()
		user_choice_list.append(user_choice-1)
		check = course_id_list[user_choice-1]
		print("")
		print(course_dic[check])
		print("")
		child_exe(check)			

# Here we create the file called course.json and also check the that file is exist or not.
def request_api(api_url):
	file_name = 'request_data/course.json'
	debug = False
	text = None
	if os.path.exists(file_name):
		debug = True
		read_course()

	if debug is False:
		api_1 = requests.get(api_url)
		raw = json.dumps(api_1.text)
		file1 = open(file_name,'w')
		file1.write(raw)
		file1.close()

		read_course()

request_api(saral_api_url)

def previous_next():
	if number >=0:
		check = course_id_list[number]
		print(course_dic[check])
		child_exe(check)
	else:
		print("Course is not available")

while True:
	print("")
	message = ''' Go to Main Menu enter: up\n For previous course enter: p\n For next course enter: n'''
	print(message)
	print("")
	choice = input("Enter your Choice: ").upper()
	if choice == 'UP':
		request_api(saral_api_url)
	elif choice == 'P':
		number = user_choice_list[-1]-1
		previous_next()
	elif choice == 'N':
		number = user_choice_list[-1]+1
		previous_next()
	else:
		print("Enter the correct choice")
