import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS 'levels' (
    'id_level' INTEGER PRIMARY KEY,
    'name' VARCHAR(255)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS 'majors'(
    'id_major' INTEGER PRIMARY KEY,
    'name' VARCHAR(255)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS 'study_types' (
    'id_type' INTEGER PRIMARY KEY,
    'name' VARCHAR(255)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS 'students' (
    'id_student' INTEGER PRIMARY KEY,
    'id_level' INTEGER,
    'id_major' INTEGER,
    'id_type' INTEGER,
    'last_name' VARCHAR(255),
    'first_name' VARCHAR(255),
    'middle_name' VARCHAR(255),
    'average_score' INTEGER,
    FOREIGN KEY ('id_level') REFERENCES levels ('id_level'),
    FOREIGN KEY ('id_major') REFERENCES majors ('id_major'),
    FOREIGN KEY ('id_type') REFERENCES study_types ('id_type')
)
""")


def load_data_from_file(file_name, table_name):
    try:
        cursor.execute(f"DELETE FROM {table_name}")
        conn.commit()

        with open(file_name, "r", encoding="utf-8") as file:
            data = []
            if table_name in ["levels", "majors", "study_types"]:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        parts = line.split(",", 1)
                        if len(parts) == 2:
                            record_id = int(parts[0].strip())
                            record_name = parts[1].strip()
                            data.append((record_id, record_name))
                        else:
                            print(
                                f"Предупреждение: Неправильный формат строки в {file_name}: '{line}'"
                            )
                    except ValueError:
                        print(
                            f"Предупреждение: Не удалось преобразовать ID в число в {file_name}: '{line}'"
                        )
                    except Exception as e:
                        print(f"Ошибка обработки строки в {file_name}: '{line}' - {e}")

            elif table_name == "students":
                lines = file.readlines()
                for i, line in enumerate(lines):
                    parts = line.strip().split(",")
                    try:
                        student_id_from_file = (
                            int(parts[0])
                            if len(parts) > 0 and parts[0].isdigit()
                            else i + 1
                        )
                        level_id = (
                            int(parts[1])
                            if len(parts) > 1 and parts[1].isdigit()
                            else (i % 3) + 1
                        )
                        major_id = (
                            int(parts[2])
                            if len(parts) > 2 and parts[2].isdigit()
                            else (i % 3) + 1
                        )
                        type_id = (
                            int(parts[3])
                            if len(parts) > 3 and parts[3].isdigit()
                            else (i % 3) + 1
                        )
                        last_name = (
                            parts[4].strip() if len(parts) > 4 else f"Фамилия{i + 1}"
                        )
                        first_name = (
                            parts[5].strip() if len(parts) > 5 else f"Имя{i + 1}"
                        )
                        middle_name = (
                            parts[6].strip() if len(parts) > 6 else f"Отчество{i + 1}"
                        )
                        avg_score = (
                            int(parts[7])
                            if len(parts) > 7 and parts[7].isdigit()
                            else 75
                        )

                        data.append(
                            (
                                student_id_from_file,
                                level_id,
                                major_id,
                                type_id,
                                last_name,
                                first_name,
                                middle_name,
                                avg_score,
                            )
                        )
                    except IndexError:
                        print(
                            f"Предупреждение: Недостаточно данных в строке {i + 1} файла {file_name}: '{line.strip()}'"
                        )
                    except ValueError:
                        print(
                            f"Предупреждение: Ошибка преобразования числа в строке {i + 1} файла {file_name}: '{line.strip()}'"
                        )
                    except Exception as e:
                        print(
                            f"Ошибка обработки строки {i + 1} в {file_name}: '{line.strip()}' - {e}"
                        )
            else:
                for line in file:
                    data.append(tuple(part.strip() for part in line.strip().split(",")))

            if data:
                placeholders = ", ".join(["?"] * len(data[0]))
                cursor.executemany(
                    f"INSERT INTO {table_name} VALUES ({placeholders})", data
                )
                conn.commit()
            else:
                print(
                    f"Нет данных для вставки в таблицу {table_name} из файла {file_name}"
                )

    except sqlite3.Error as e:
        print(f"Ошибка SQLite при работе с таблицей {table_name}: {e}")
        conn.rollback()
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_name} не найден.")
    except Exception as e:
        print(f"Произошла ошибка при загрузке данных для {table_name}: {e}")
        conn.rollback()


load_data_from_file("levels.txt", "levels")
load_data_from_file("majors.txt", "majors")
load_data_from_file("study_types.txt", "study_types")
load_data_from_file("students.txt", "students")


cursor.execute("SELECT COUNT(id_student) AS amount_of_students FROM students")
result = cursor.fetchone()
print(f"Общее кол-во студентов - {result[0]}")


cursor.execute("""
SELECT majors.name AS major_name, COUNT(students.id_student) AS student_count
FROM students 
JOIN majors 
ON students.id_major = majors.id_major
GROUP BY majors.name
ORDER BY student_count DESC
""")
results = cursor.fetchall()
print("\nКоличество студентов по направлениям:")
for row in results:
    print(f"Направление: {row[0]}, Количество студентов: {row[1]}")


cursor.execute("""
SELECT levels.name AS level_name, COUNT(students.id_student) AS student_count
FROM students 
JOIN levels
ON students.id_level = levels.id_level
GROUP BY levels.name
ORDER BY student_count DESC
""")
result = cursor.fetchall()
print("\nКоличество студентов по уровням обучения: ")
for row in result:
    print(f"Уровень обучение: {row[0]}, Количество студентов:{row[1]}")


cursor.execute("""
SELECT 
    majors.name AS Major,
    MAX(students.average_score) AS Max_score,
    MIN(students.average_score) AS Min_score,
    AVG(students.average_score) AS Average_score
FROM 
    students
JOIN 
    majors ON students.id_major = majors.id_major
GROUP BY 
    majors.name
ORDER BY 
    Major
""")
result = cursor.fetchall()
print("\nМаксимальный, минимальный, средний баллы студентов по направлениям: ")
for row in result:
    print(
        f"Направление: {row[0]}, Макс: {row[1]}, Мин: {row[2]}, Средний: {row[3]:.2f}"
    )


cursor.execute("""
SELECT 
    majors.name AS Major,
    levels.name AS Education_level,
    study_types.name AS Study_form,
    AVG(students.average_score) AS Average_score
FROM 
    students
JOIN 
    majors ON students.id_major = majors.id_major
JOIN 
    levels ON students.id_level = levels.id_level
JOIN 
    study_types ON students.id_type = study_types.id_type
GROUP BY 
    majors.name, 
    levels.name, 
    study_types.name
ORDER BY 
    Major, 
    Education_level, 
    Study_form
""")
result = cursor.fetchall()
print("\nСредний балл студентов по направлениям, уровням и формам обучения:")
for row in result:
    print(
        f"Направление: {row[0]}, Уровень: {row[1]}, Форма: {row[2]}, Средний балл: {row[3]:.2f}"
    )


cursor.execute("""
SELECT 
    students.last_name AS Фамилия,
    students.first_name AS Имя,
    students.middle_name AS Отчество,
    students.average_score AS Средний_балл
FROM 
    students
JOIN 
    majors ON students.id_major = majors.id_major
JOIN 
    study_types ON students.id_type = study_types.id_type
WHERE 
    majors.name = 'Applied Informatics' 
    AND study_types.name = 'Full-time'
ORDER BY 
    students.average_score DESC
LIMIT 5;
""")

result = cursor.fetchall()
print("\nТоп-5 студентов направления 'Applied Informatics' (очная форма обучения):")
for row in result:
    print(
        f"Фамилия: {row[0]}, Имя: {row[1]}, Отчество: {row[2]}, Средний балл: {row[3]}"
    )

cursor.execute("""
SELECT 
    last_name AS Фамилия, 
    COUNT(*) AS Количество_однофамильцев
FROM 
    students
GROUP BY 
    last_name
HAVING 
    COUNT(*) > 1
ORDER BY
    Количество_однофамильцев DESC, Фамилия; 
""")

print("-")
result = cursor.fetchall()
print("Найдены следующие группы однофамильцев:")
for row in result:
    print(f"Фамилия: {row[0]}, Количество человек: {row[1]}")


cursor.execute("""
SELECT 
    last_name AS Фамилия, 
    first_name AS Имя, 
    middle_name AS Отчество, 
    COUNT(*) AS Количество_тезок
FROM 
    students
GROUP BY 
    last_name, first_name, middle_name
HAVING 
    COUNT(*) > 1
ORDER BY
    Количество_тезок DESC, Фамилия, Имя;
""")

print("-")
result = cursor.fetchall()
print("Найдены следующие полные тезки:")
for row in result:
    print(f"ФИО: {row[0]} {row[1]} {row[2]}, Количество человек: {row[3]}")


conn.commit()
conn.close()
