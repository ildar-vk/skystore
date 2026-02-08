import requests
import sys

base_url = "http://localhost:8002"

print("=" * 60)
print("ПРОВЕРКА РАБОТЫ КАТЕГОРИЙ")
print("=" * 60)

# Сначала получим главную страницу, чтобы узнать категории
try:
    response = requests.get(base_url + "/", timeout=5)
    if response.status_code != 200:
        print("❌ Не удалось загрузить главную страницу")
        sys.exit(1)
        
    # Проверяем наличие кнопок категорий
    if "Категории товаров" in response.text:
        print("✅ Блок категорий найден на главной странице")
    else:
        print("❌ Блок категорий не найден")
        
    # Проверяем ссылки на категории (примерные ID)
    categories_to_test = [
        ("Электроника", 1),
        ("Книги", 2),
        ("Одежда", 3)
    ]
    
    for category_name, category_id in categories_to_test:
        url = f"{base_url}/category/{category_id}/"
        try:
            cat_response = requests.get(url, timeout=5)
            if cat_response.status_code == 200:
                if category_name in cat_response.text:
                    print(f"✅ Категория '{category_name}' работает: {url}")
                else:
                    print(f"⚠️  Страница категории {category_id} загружается, но '{category_name}' не найден")
            else:
                print(f"❌ Категория '{category_name}': статус {cat_response.status_code}")
        except Exception as e:
            print(f"❌ Ошибка при проверке категории '{category_name}': {e}")
            
except Exception as e:
    print(f"❌ Общая ошибка: {e}")

print("\n" + "=" * 60)
print("РУЧНАЯ ПРОВЕРКА:")
print("1. Откройте http://localhost:8002/")
print("2. Нажмите на кнопку 'Книги'")
print("3. Убедитесь, что отображаются только книги")
print("4. Проверьте другие категории")
print("=" * 60)
