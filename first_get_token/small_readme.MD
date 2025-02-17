Хромдрайвер качать отсюда
https://googlechromelabs.github.io/chrome-for-testing/
(инструкция тут https://stepik.org/lesson/25969/step/9)
1. wget https://chromedriver.storage.googleapis.com/102.0.5005.61/chromedriver_linux64.zip
2. unzip chromedriver_linux64.zip
3. sudo mv chromedriver /usr/local/bin/chromedriver
4. sudo chown root:root /usr/local/bin/chromedriver
5. sudo chmod +x /usr/local/bin/chromedriver


Для первоначального получения 'access_token' и 'refresh_token':
1. руками запустить get_auth_code.py
2. авторизоваться на hh.ru
3. хром переадресует на страницу hh.ru, скопировать ссылку из адресной строки
4. code в ссылке это и есть authorization_code
5. запустить руками функцию get_tokens(code=authorization_code) в файле get_token.py