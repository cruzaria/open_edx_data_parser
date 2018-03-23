import pymysql


def get_course_enrollments(config: dict):
    connection = pymysql.connect(
        host=config['host'],
        user=config['user'],
        password=config['pass'],
        db=config['db'],
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            sql = "SELECT sc.id AS `номер`, " \
                  "coc.display_name AS `название курса`, " \
                  "sc.created AS `дата записи`, " \
                  "au.username AS `логин`, " \
                  "au.first_name AS `имя`, " \
                  "au.last_name AS `фамилия`, " \
                  "au.email AS email " \
                  "FROM student_courseenrollment AS sc " \
                  "INNER JOIN auth_user AS au " \
                  "ON sc.user_id = au.id " \
                  "INNER JOIN course_overviews_courseoverview AS coc " \
                  "ON sc.course_id = coc.id"
            cursor.execute(sql)
            result = cursor.fetchall()
            return True, result
    except Exception as e:
        print(e)
        return False, e
    finally:
        connection.close()


def get_user_data(config: dict):
    connection = pymysql.connect(
        host=config['host'],
        user=config['user'],
        password=config['pass'],
        db=config['db'],
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            sql = "SELECT au.id AS `номер`, au.username AS `логин`, " \
                  "au.first_name AS `имя`, au.last_name AS `фамилия`, " \
                  "au.date_joined AS `дата регистрации`, au.email AS `email`, " \
                  "au.last_login AS `последнее посещение`, aup.country AS `страна`, " \
                  "aup.city AS `город`, aup.year_of_birth AS `дата рождения`, " \
                  "aup.language AS `язык`, aup.location AS `местоположение`, " \
                  "aup.gender AS `пол`, aup.level_of_education AS `образование` " \
                  "FROM auth_user AS au " \
                  "INNER JOIN auth_userprofile AS aup " \
                  "ON au.id = aup.user_id"
            cursor.execute(sql)
            result = cursor.fetchall()
            return True, result
    except Exception as e:
        print(e)
        return False, e
    finally:
        connection.close()
