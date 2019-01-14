import requests,json,os,pprint

url = "http://saral.navgurukul.org/api/courses"

def child_exe(user_input):

	file_name = 'request_data/course_exe/exercises_'+ str(user_input) + '.json'
	debug = False
	text = None
	if os.path.exists(file_name):
		debug =  True
		with open(file_name,'r') as file2:
			raw = file2.read() # the type of raw is unicode_type
			s = json.loads(raw) # The type of s is also unicode_type
			text = json.loads(s) # The type of dic is dic_type
			data = text['data']
			for i in (data):
				parent_exe = i['name']
				child_exe = i['childExercises']
				index = 1
				for j in child_exe:
					sub_exe = j['name']
					if index == 1:
						print('---------' + parent_exe + '---------')
						print('     ' + str(index) + '.' + sub_exe)
					else:
						print('     '+ str(index) + '.' + sub_exe)
					index+=1



	if debug is False:
		exercises_url = url +"/" + str(user_input) + '/exercises'
		api_2 = requests.get(exercises_url)
		raw = json.dumps(api_2.text)
		file1 = open(file_name,'w')
		file1.write(raw)
		file1.close()

		with open(file_name,'r') as file2:
				raw = file2.read() # the type of raw is unicode_type
				s = json.loads(raw) # The type of s is also unicode_type
				text = json.loads(s) # The type of dic is dic_type
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
		path = 'request_data/exercise_slug/exercise_' + str(user_input)
		os.mkdir(path)
		for slug in slugs:
			exercises_url = url +"/" + str(user_input) + '/exercise'
			slug_url = exercises_url + '/getBySlug?slug=' + slug
			slug_requests = requests.get(slug_url)
			a = ''
			for i in slug:
				if '/' not in i:
					a += i
				else:
					a +='_'
			slug1 = a
			file_name = slug1 + '.json'
			
			with open( path + "/" + file_name ,'w') as file3:
				json.dump(slug_requests.text,file3)
				


# This code for parent exercises.
def request_api(url):
	# Task 2
	file_name = 'request_data/course.json'
	debug = False
	text = None
	if os.path.exists(file_name):
		debug = True
		with open("request_data/course.json",'r') as file1:
			raw = file1.read() # the type of raw is unicode_type
			s = json.loads(raw) # The type of s is also unicode_type
			text = json.loads(s) # The type of dic is dic_type
			# dic = ast.literal_eval(s) # Here we are directly convert unicode_type to dic_type in json
			course = text['availableCourses']
			course_dic = {}
			for i in range(len(course)):
				course_id = course[i]['id']
				course_name = course[i]['name']
				course_dic[course_id] = course_name
			print(course_dic)
			user_input = int(input("Enetr Index number of Course: "))
			print("")
			print(course_dic[user_input])
			print("")
			child_exe(user_input)

				
	if debug is False:
		# Task 1
		api_1 = requests.get(url)
		raw = json.dumps(api_1.text)
		file1 = open(file_name,'w')
		file1.write(raw)
		file1.close()

		# Task 2
		with open("request_data/course.json",'r') as file1:
			raw = file1.read() # the type of raw is unicode_type
			s = json.loads(raw) # The type of s is also unicode_type
			text = json.loads(s) # The type of dic is dic_type
			# dic = ast.literal_eval(s) # Here we are directly convert unicode_type to dic_type in json
			course = text['availableCourses']
			course_dic = {}
			for i in range(len(course)):
				course_id = course[i]['id']
				course_name = course[i]['name']
				course_dic[course_id] = course_name
			print(course_dic)
			user_choice = int(input("Enetr id of course: "))
			print("")
			print(course_dic[user_choice])
			print("")
			child_exe(user_choice)
request_api(url)
