from typing import List

from src.aeroplane import Aeroplane
from src.api import AeroplanesAPI
from src.file_storage import JSONStorage


def user_interaction():
    """Основная функция взаимодействия с пользователем."""
    api = AeroplanesAPI()
    storage = JSONStorage()

    print("Добро пожаловать в систему мониторинга самолётов!")

    country = input("Введите название страны для поиска самолётов: ").strip()
    try:
        raw_data = api.get_aeroplanes(country)
        if not raw_data:
            print("Самолётов в указанном регионе не найдено.")
            return
        aeroplanes = Aeroplane.cast_to_object_list(raw_data)
        print(f"Найдено {len(aeroplanes)} самолётов.")
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return

    for plane in aeroplanes:
        storage.add_aeroplane(plane)

    while True:
        print("\nВыберите действие:")
        print("1. Показать топ N самолётов по высоте")
        print("2. Получить самолёты по стране регистрации")
        print("3. Удалить самолёт из хранилища")
        print("4. Выйти")

        choice = input("Ваш выбор: ").strip()
        if choice == "1":
            try:
                n = int(input("Введите N: "))
                sorted_planes = sorted(
                    aeroplanes, key=lambda p: p.baro_altitude, reverse=True
                )
                top = sorted_planes[:n]
                print(f"\nТоп {n} самолётов по высоте:")
                for i, p in enumerate(top, 1):
                    print(f"{i}. {p}")
            except ValueError:
                print("Некорректный ввод N.")
        elif choice == "2":
            country_filter = input("Введите страну регистрации: ").strip()
            filtered = [
                p
                for p in aeroplanes
                if p.origin_country.lower() == country_filter.lower()
            ]
            if filtered:
                print(f"\nНайдено {len(filtered)} самолётов из {country_filter}:")
                for p in filtered:
                    print(p)
            else:
                print("Самолётов из указанной страны не найдено.")
        elif choice == "3":
            callsign = input("Введите позывной самолёта для удаления: ").strip()
            country_reg = input("Введите страну регистрации: ").strip()
            to_delete = None
            for p in aeroplanes:
                if p.callsign == callsign and p.origin_country == country_reg:
                    to_delete = p
                    break
            if to_delete:
                storage.delete_aeroplane(to_delete)
                aeroplanes.remove(to_delete)
                print("Самолёт удалён из хранилища.")
            else:
                print("Самолёт не найден.")
        elif choice == "4":
            break
        else:
            print("Неверный ввод, попробуйте снова.")
