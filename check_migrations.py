#!/usr/bin/env python3
"""
Проверка состояния миграций базы данных
"""

import asyncio
import os
import sys

# Добавляем корневую директорию в путь для импортов
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.database import db
from sqlalchemy import text


async def check_migration_status():
    """Проверяет текущее состояние миграций"""
    print("🔍 Проверка состояния миграций базы данных...")
    print("=" * 60)

    async with db.session() as session:
        try:
            # Проверяем таблицу alembic_version
            result = await session.execute(text('SELECT version_num FROM alembic_version'))
            current_version = result.scalar()
            print(f'📊 Текущая версия миграции в БД: {current_version}')

            # Проверяем, какие миграции существуют локально
            migration_dir = 'migrations/versions'
            migration_files = [f for f in os.listdir(migration_dir) if f.endswith('.py')]
            print(f'📁 Локальные файлы миграций: {len(migration_files)} файлов')

            # Показываем историю миграций
            for i, filename in enumerate(sorted(migration_files), 1):
                revision_id = filename.split('_')[0]
                description = ' '.join(filename.split('_')[1:]).replace('.py', '')
                print(f'  {i}. {revision_id} - {description}')

            # Проверяем, какие таблицы существуют
            result = await session.execute(text('''
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
            '''))
            tables = [row[0] for row in result]
            print(f'\n🗃️  Таблицы в базе данных: {len(tables)} таблиц')
            for table in tables:
                print(f'  - {table}')

            # Проверяем ключевые таблицы
            key_tables = ['users', 'bots', 'user_bots', 'alembic_version']
            missing_tables = [t for t in key_tables if t not in tables]

            if missing_tables:
                print(f'\n⚠️  Отсутствуют ключевые таблицы: {missing_tables}')
                return False
            else:
                print(f'\n✅ Все ключевые таблицы присутствуют')
                return True

        except Exception as e:
            print(f'❌ Ошибка при проверке миграций: {e}')
            return False


async def test_migration_consistency():
    """Проверяет согласованность миграций"""
    print("\n" + "=" * 60)
    print("🧪 Проверка согласованности миграций...")

    try:
        # Проверяем, что можем применить миграции
        import subprocess
        result = subprocess.run(
            ['python', '-m', 'alembic', 'current'],
            capture_output=True, text=True
        )

        if result.returncode == 0:
            print('✅ Команда alembic current работает корректно')
            print(f'   Вывод: {result.stdout.strip()}')
        else:
            print(f'❌ Ошибка выполнения alembic current: {result.stderr}')
            return False

        # Проверяем историю
        result = subprocess.run(
            ['python', '-m', 'alembic', 'history'],
            capture_output=True, text=True
        )

        if result.returncode == 0:
            print('✅ Команда alembic history работает корректно')
            lines = result.stdout.strip().split('\n')
            for line in lines:
                print(f'   {line}')
        else:
            print(f'❌ Ошибка выполнения alembic history: {result.stderr}')
            return False

        return True

    except Exception as e:
        print(f'❌ Ошибка при проверке согласованности: {e}')
        return False


async def main():
    """Основная функция проверки"""
    print("=" * 60)
    print("Проверка состояния миграций базы данных")
    print("=" * 60)

    # Проверяем статус миграций
    migration_ok = await check_migration_status()

    # Проверяем согласованность
    consistency_ok = await test_migration_consistency()

    print("\n" + "=" * 60)
    if migration_ok and consistency_ok:
        print("✅ Миграции находятся в корректном состоянии!")
        print("💡 Рекомендация: Можно безопасно делать коммит")
        return 0
    else:
        print("❌ Обнаружены проблемы с миграциями!")
        print("💡 Рекомендация: Исправьте проблемы перед коммитом")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
