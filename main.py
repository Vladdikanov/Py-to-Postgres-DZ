import psycopg2

db = "clientdb"
user = "postgres"
pw = "03051997"
conn = psycopg2.connect(database=db, user=user, password=pw)

def create_structure(connect):
    with connect.cursor() as cur:

        cur.execute("""create table if not exists client_info(
                client_id serial primary key,
                first_name varchar(40),
                second_name varchar(40),
                email varchar(40));""")

        cur.execute("""create table if not exists number_phone(
                phone_id serial primary key,
                number varchar(40));""")

        cur.execute("""create table if not exists client_phone(
                client_id integer references client_info(client_id),
                phone_id integer references number_phone(phone_id),
                constraint cp primary key(client_id, phone_id));""")

        conn.commit()
        print("Структура базы данных создана")

def add_client(connect):
    with connect.cursor() as cur:
        fname = str(input("Ведите имя")).title()
        sname = str(input("Введите фамилию")).title()
        email = str(input("Введите email"))
        cur.execute(""" insert into client_info(first_name, second_name, email)
        values (%s,%s,%s)""", (fname,sname,email))
        conn.commit()
        print("Клиент добавлен в БД")

def add_phone(connect):
    with connect.cursor() as cur:
        fname = str(input("Ведите имя")).title()
        sname = str(input("Введите фамилию")).title()
        num = str(input("Введите телефон"))
        cur.execute(""" select client_id from client_info
        where first_name = %s and second_name = %s;""", (fname,sname))
        cl_id = cur.fetchone()[0]
        cur.execute("""insert into number_phone(number)
        values(%s) returning phone_id;""",(num,))
        ph_id = cur.fetchone()[0]
        cur.execute("""insert into client_phone
        values(%s,%s);""",(cl_id,ph_id))
        conn.commit()

def edit_info(connect):
    with connect.cursor() as cur:
        print("Поиск клиента")
        fname = str(input("Введите имя")).title()
        print("Поиск клиента")
        sneme = str(input("Введите фамилию")).title()
        cur.execute("""select client_id from client_info
        where first_name = %s and second_name = %s;""",(fname,sneme))
        cl_id = cur.fetchone()[0]
        print(cl_id)
        print("Обновление данных о клиенте. Для пропуска введите '-'")
        fname2 = str(input("Имя")).title()
        print("Обновление данных о клиенте. Для пропуска введите '-'")
        sname2 = str(input("Фамилия")).title()
        print("Обновление данных о клиенте. Для пропуска введите '-'")
        email2 = str(input("Email"))
        if fname2 != "-":
            cur.execute("""update client_info 
            set first_name = %s
            where client_id = %s;""", (fname2,cl_id))
        if sname2 != "-":
            cur.execute("""update client_info 
            set second_name = %s
            where client_id = %s;""", (sname2,cl_id))
        if email2 != "-":
            cur.execute("""update client_info 
            set email = %s
            where client_id = %s;""", (email2,cl_id))
        print("Данные обновлены")
        conn.commit()

def del_phone(connect):
    with connect.cursor() as cur:
        print("Поиск клиента")
        fname = str(input("Введите имя")).title()
        print("Поиск клиента")
        sneme = str(input("Введите фамилию")).title()
        cur.execute("""select client_info.client_id, client_info.first_name, 
        client_info.second_name, number_phone.phone_id, number_phone.number from client_info
        left join client_phone on client_info.client_id = client_phone.client_id
        left join number_phone on client_phone.phone_id = number_phone.phone_id
        where client_info.first_name = %s and client_info.second_name = %s;""", (fname, sneme))
        info = cur.fetchall()
        cl_id = info[0][0]
        print(info)
        ph_id = int(input("Введите ID номера, который хотите удалить"))
        cur.execute("""delete from client_phone 
        where client_id = %s and phone_id = %s;
        delete from number_phone
        where phone_id = %s;""", (cl_id,ph_id,ph_id))
        conn.commit()
        print("Номер удален")

def del_client(connect):
    with connect.cursor() as cur:
        print("Поиск клиента")
        fname = str(input("Введите имя")).title()
        print("Поиск клиента")
        sneme = str(input("Введите фамилию")).title()
        cur.execute("""select client_info.client_id, client_info.first_name, 
        client_info.second_name, number_phone.phone_id, number_phone.number from client_info
        left join client_phone on client_info.client_id = client_phone.client_id
        left join number_phone on client_phone.phone_id = number_phone.phone_id
        where client_info.first_name = %s and client_info.second_name = %s;""", (fname, sneme))
        info = cur.fetchall()
        cl_id = info[0][0]
        ph_ids = [i[3] for i in info]
        cur.execute("""delete from client_phone
        where client_id = %s;
        delete from client_info
        where client_id = %s;""",(cl_id,cl_id))
        conn.commit()
        for id_cls_ph in ph_ids:
            cur.execute("""delete from number_phone
            where phone_id = %s;""",(id_cls_ph,))
            conn.commit()
        print("Клиент удален")

def find_client(connect):

    print("Поиск клиента по:\n1.Имени\n2.Фамилии\n3.Email\n4.Номеру телефона\n5.Остановить поиск")

    while True:

        choice = int(input("Модификатор поиска>>>"))

        if choice == 1:
            fname = input("Введите имя").title()
            with connect.cursor() as cur:
                cur.execute("""select client_info.client_id, client_info.first_name, 
                client_info.second_name, client_info.email, number_phone.phone_id, number_phone.number from client_info
                left join client_phone on client_info.client_id = client_phone.client_id
                left join number_phone on client_phone.phone_id = number_phone.phone_id
                where client_info.first_name = %s;""", (fname,))
                clients = cur.fetchall()
                print(clients)
        if choice == 2:
            sname = input("Введите Фамилию").title()
            with connect.cursor() as cur:
                cur.execute("""select client_info.client_id, client_info.first_name, 
                client_info.second_name, client_info.email, number_phone.phone_id, number_phone.number from client_info
                left join client_phone on client_info.client_id = client_phone.client_id
                left join number_phone on client_phone.phone_id = number_phone.phone_id
                where client_info.second_name = %s;""", (sname,))
                clients = cur.fetchall()
                print(clients)
        if choice == 3:
            email = input("Введите Email")
            with connect.cursor() as cur:
                cur.execute("""select client_info.client_id, client_info.first_name, 
                client_info.second_name, client_info.email, number_phone.phone_id, number_phone.number from client_info
                left join client_phone on client_info.client_id = client_phone.client_id
                left join number_phone on client_phone.phone_id = number_phone.phone_id
                where client_info.email = %s;""", (email,))
                clients = cur.fetchall()
                print(clients)
        if choice == 4:
            number = input("Введите Номер")
            with connect.cursor() as cur:
                cur.execute("""select client_info.client_id, client_info.first_name, 
                client_info.second_name, client_info.email, number_phone.phone_id, number_phone.number from client_info
                left join client_phone on client_info.client_id = client_phone.client_id
                left join number_phone on client_phone.phone_id = number_phone.phone_id
                where number_phone.number = = %s;""", (number,))
                clients = cur.fetchall()
                print(clients)
        if choice == 5:
            break

# with conn.cursor() as cur:
#     cur.execute("""drop table client_phone;
#     drop table client_info;
#     drop table number_phone;""")
#     conn.commit()

print("Управление БД:\n1.Создать структуру БД\n2.Добавить клиента\n"
      "3.Добавить телефон\n4.Редактировать информацию о клиенте\n5.Удалить телефон\n6.Удалить клиента\n7.Найти клиента\n8.Остановить")
comands = {1:create_structure,2:add_client,3:add_phone,4:edit_info,5:del_phone,6:del_client,7:find_client}
while True:
    comand = int(input("Введите команду >>>"))
    if comand != 8:
        try:
            comands[comand](conn)
        except TypeError:
            print("Неверные данные")
    else:
        break
conn.close()


# def find_client(connect):
#
#     print("Поиск клиента по:\n1.Имени\n2.Фамилии\n3.Email\n4.Номеру телефона\n5.Сброс\n6.Поиск")
#     find = {1: "Имя", 2: "Фамилия", 3: "Email", 4: "Номер телефона"}
#     find_list = []
#     mod = []
#     print(bool(mod))
#     while True:
#         choice = int(input("Модификатор поиска>>>"))
#         if choice in mod:
#             print(
#                 "Этот критерий поиска уже введен.\nВы можете:\n1.Ввести новый критерий\n2.Сбросить все критерии\n3.Начать поиск")
#             continue
#         if choice == 1:
#             sname = input("Введите имя")
#             str = f"client_info.first_name = {sname}"
#             find_list.append(str)
#             mod.append(choice)
#         if choice == 2:
#             fname = input("Введите Фамилию")
#             str = f"client_info.second_name = {fname}"
#             find_list.append(str)
#             mod.append(choice)
#         if choice == 3:
#             email = input("Введите Email")
#             str = f"client_info.email = {email}"
#             find_list.append(str)
#             mod.append(choice)
#         if choice == 4:
#             number = input("Введите Номер")
#             str = f"number_phone.number = {number}"
#             find_list.append(str)
#             mod.append(choice)
#         if choice == 5:
#             find_list.clear()
#             print("Критерии поиска сброшены")
#         if choice == 6:
#             str = (", ".join(find_list))
#             break
#     with connect.cursor() as cur:
#         cur.execute("""select client_info.client_id, client_info.first_name,
#         client_info.second_name, number_phone.phone_id, number_phone.number from client_info
#         left join client_phone on client_info.client_id = client_phone.client_id
#         left join number_phone on client_phone.phone_id = number_phone.phone_id
#         where %s;""", (str,))
#         clients = cur.fetchall()
#         print(clients)


