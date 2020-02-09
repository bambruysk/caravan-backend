# �������� ������ � � ��������.

����� � �������� ����������� � JSON  ������� ����� HTTP.

## ������� ��������������

### 1. �������������� (�������):

	Root-endpoint: "/login"
	GET
		-> 	login,					// �����
			password				// ������ 
		<-	validate				// ������������� 

	JSON-������:
	Request
	{
		"login": "string",
		"password": "string"
	}
	Response
	{
		"validate": "boolean"
	}


### 2. ����� ������:
	Root-endpoint: "/"
	PUT
		-> 	old_password,			// ������ ������
			new_password			// ����� ������ 
		<-	validate				// �������������

		
	JSON-������:
	Request
	{
		"old_password": "string",
		"new_password": "string"
	}
	Response
	{
		"validate": "boolean"
	}

## ��������
### 3. ������ ��������� � ���������:
	Root-endpoint: "/"
	GET
		<- 	routes [				// ������ ��������� 
				route_id 			// ������������� ��������
				route_name 			// �������� ��������
				route_level 		// ������� 5-������� ������
				route_description 	// �������� ��������
				master_instruction	// ���������� �������
			]
			
	JSON-������:
	Response
	{
		"routes": [
			{
				"route_id": "integer",
				"route_name": "string",
				"route_level": "integer",
				"route_description": "string",
				"master_instruction": "string"
			},
			......
		]
	}

-------------------------------------------------

### 4. ����� �������� � �������� ������:

	Root-endpoint: "/"
	POST
		->	user_id					// id ������(�������)
			user_name,				// ��� ������
			route_id,				// id ��������
		<-	map,					// ������ �� ����� "http://"
			geo_points [			// ������ ���-�����
				point_id,			// id ���-�����
				latitude,			// ������
				longitude			// �������
			],
			route_points [			// ������ ���������� �����
				point_id,			// id ���-�����
				message				// ���������
			]

		
	JSON-������:
	Request
	{
		"user_id": "integer",
		"user_name": "string",
		"route_id": "integer"
	}
	Response
	{
		"map": "string",
		"geo_points": [
			{
				"point_id": "integer",
				"latitude": "double",
				"longitude": "double"
			},
			......
		],
		"route_points" [
			{
				"point_id": "integer",
				"message": "string"
			},
			......
		]
	}

-------------------------------------------------

### 5. ����������� ����� ��������:

	Root-endpoint: "/"
	POST
		->	user_id,				// id ������
			point_id				// id - ���������� ���-�����

		
	JSON-������:
	Request
	{
		"user_id": "integer",
		"point_id": "integer"
	}

-------------------------------------------------
