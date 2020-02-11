# Протокол обмена с с сервером.

Обмен с сервером выполняется в JSON  формате через HTTP.

## Процесс аутентификации

### 1. Аутентификация (мастера):

	Root-endpoint: "/login"
	POST
		->  login,	    // логин
		    password	// пароль 
		<-  token       // токен авторизации.

	JSON-формат:
	Request
	{
		"login": "string",
		"password": "string"
	}
	Response
	{
		"validate": "boolean"
		"token" : "string"
	}


### 2. Смена пароля:
	Root-endpoint: "/change_passwd"
	PUT
		-> 	old_password,			// старый пароль
			new_password			// новый пароль 
		<-	validate				// подтверждение

		
	JSON-формат:
	Request
	{
		"old_password": "string",
		"new_password": "string"
	}
	Response
	{
		"validate": "boolean"
	}

## Маршруты
### 3. Список маршрутов с описанием:
	Root-endpoint: "/"
	GET
		<- 	routes [				// список маршрутов 
				route_id 			// идентификатор маршрута
				route_name 			// название маршрута
				route_level 		// уровень 5-бальная оценка
				route_description 	// описание маршрута
				master_instruction	// инструкции мастеру
			]
			
	JSON-формат:
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

### 4. Выбор маршрута и загрузка данных:

	Root-endpoint: "/"
	POST
		->	user_id					// id игрока(сундука)
			user_name,				// имя игрока
			route_id,				// id маршрута
		<-	map,					// ссылка на карту "http://"
			geo_points [			// список гео-точек
				point_id,			// id гео-точки
				latitude,			// широта
				longitude			// долгота
			],
			route_points [			// список маршрутных точек
				point_id,			// id гео-точки
				message				// сообщение
			]

		
	JSON-формат:
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

### 5. Прохождение точек игроками:

	Root-endpoint: "/"
	POST
		->	user_id,				// id игрока
			point_id				// id - пройденной гео-точки

		
	JSON-формат:
	Request
	{
		"user_id": "integer",
		"point_id": "integer"
	}

-------------------------------------------------
