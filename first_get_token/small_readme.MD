Для первоначального получения 'access_token' и 'refresh_token':
1. руками запустить get_auth_code.py
2. авторизоваться на hh.ru
3. хром переадресует на страницу hh.ru, скопировать ссылку из адресной строки
4. code в ссылке это и есть authorization_code
5. запустить руками функцию get_tokens(code=authorization_code) в файле get_token.py