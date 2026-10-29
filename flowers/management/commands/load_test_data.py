import os

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from flowers.models import Bouquet, BudgetInterval, Event


class Command(BaseCommand):
    help = "Наполняет базу данных тестовыми событиями, интервалами бюджета и букетами"

    def handle(self, *args, **options):
        self.stdout.write("Начало загрузки тестовых данных...")

        events_titles = ["День рождения", "Свадьба", "Без повода"]
        events = {}
        for title in events_titles:
            event, created = Event.objects.get_or_create(title=title)
            events[title] = event
            if created:
                self.stdout.write(f"Создано событие: {title}")

        intervals_data = [
            {"title": "До 1 000 руб", "min_price": 0, "max_price": 1000, "sort_order": 1},
            {"title": "1 000 - 5 000 руб", "min_price": 1000, "max_price": 5000, "sort_order": 2},
            {"title": "От 5 000 руб", "min_price": 5000, "max_price": 99999, "sort_order": 3},
            {"title": "Не важно", "min_price": 0, "max_price": 99999, "sort_order": 4},
        ]
        for data in intervals_data:
            interval, created = BudgetInterval.objects.get_or_create(
                title=data["title"],
                defaults={
                    "min_price": data["min_price"],
                    "max_price": data["max_price"],
                    "sort_order": data["sort_order"],
                },
            )
            if created:
                self.stdout.write(f"Создан интервал бюджета: {interval.title}")

        test_bouquets = [
            {
                "title": "Яркое солнце",
                "slug": "yarkoe-solnce",
                "description": (
                    "Этот пышный букет заряжает энергией и теплом"
                    " с первого взгляда. Центральный подсолнух символизирует"
                    " искреннюю радость, а воздушная белая гипсофила"
                    " и темная зелень добавляют композиции легкого"
                    " полевого шарма. Идеальный подарок, чтобы поднять"
                    " настроение без лишних слов."
                ),
                "composition": (
                    "Подсолнух крупный сортовой — 1 шт.,"
                    " Веточки белой гипсофилы — 5 шт., "
                    "Рускус и декоративная зелень — 6 шт., "
                    "Крафтовая упаковка, открытка."
                ),
                "size": "Высота — 45 см, Ширина — 30 см",
                "price": 2800.00,
                "is_recommended": True,
                "event_titles": ["День рождения", "Без повода"],
                "relative_img_path": "cardImg.jpg",
            },
            {
                "title": "Осенний джаз",
                "slug": "osennij-dzhaz",
                "description": (
                    "Невероятно стильная, сочная композиция в теплых огненных тонах."
                    " Экзотический синий чертополох (эрингиум)"
                    " создает потрясающий контраст с пионовидными оранжевыми розами."
                    " Этот букет выглядит дорого, дерзко и очень пышно"
                    " — идеальный выбор для ярких личностей."
                ),
                "composition": (
                    "Роза кустовая оранжевая — 7 шт., "
                    "Эрингиум (чертополох синий) — 3 шт., "
                    "Альстромерия — 4 шт., Зелень декоративная, "
                    "дизайнерская ваза/упаковка."
                ),
                "size": "Высота — 40 см, Ширина — 35 см",
                "price": 3900.00,
                "is_recommended": True,
                "event_titles": ["День рождения", "Без повода"],
                "relative_img_path": os.path.join("catalog", "catalogBg1.jpg"),
            },
            {
                "title": "Розовый зефир",
                "slug": "rozovyj-zefir",
                "description": (
                    "Композиция из стойких стабилизированных цветов и сухоцветов, "
                    "которая будет радовать получателя долгие месяцы и даже годы. "
                    "Нежные пастельные тона делают этот букет невероятно утонченным, "
                    "уютным и романтичным. "
                    "Отличный способ оставить долгую память о празднике."
                ),
                "composition": (
                    "Стабилизированная мини-роза — 3 шт., "
                    "Хлопок натуральный — 1 шт., Лагурус розовый — 7 шт., "
                    "Гипсофила сушеная — 3 шт., Ветки лаванды, "
                    "Нежно-розовая матовая упаковка, Атласная лента"
                ),
                "size": "Высота — 35 см, Ширина — 20 см",
                "price": 1500.00,
                "is_recommended": False,
                "event_titles": ["День рождения", "Без повода"],
                "relative_img_path": "recommendedBg2.jpg",
            },
            {
                "title": "Розовое облако",
                "slug": "rozovoe-oblako",
                "description": (
                    "Роскошные, невероятно пышные пионы с тонким сладким ароматом."
                    " Этот букет символизирует богатство, удачу и расцвет чувств. "
                    "Мы дополнили его стильной стеклянной вазой, чтобы получателю "
                    "не пришлось искать, куда поставить эту невероятную красоту. "
                    "Главный акцент на любом торжестве."
                ),
                "composition": (
                    "Пион премиум розовый — 5 шт., "
                    "Стеклянная ваза-цилиндр — 1 шт., "
                    "Фирменная открытка с вашими пожеланиями"
                ),
                "size": "Высота — 50 см, Ширина — 35 см",
                "price": 5200.00,
                "is_recommended": True,
                "event_titles": ["Свадьба", "День рождения"],
                "relative_img_path": "recommendedBg3.jpg",
            },
            {
                "title": "Огненный фламенко",
                "slug": "ognennyj-flamenko",
                "description": (
                    "Плотный, страстный и харизматичный букет из сочных "
                    "кораллово-оранжевых цветов в контрастной белоснежной бумаге. "
                    "Эта композиция заявляет о себе с первого взгляда "
                    "и идеально подойдет для выражения сильных чувств, "
                    "годовщины или незабываемого поздравления."
                ),
                "composition": (
                    "Роза сортовая коралловая — 11 шт., "
                    "Калла оранжевая/декоративные акценты — 3 шт., "
                    "Плотная белая дизайнерская упаковка, лента."
                ),
                "size": "Высота — 45 см, Ширина — 25 см",
                "price": 4200.00,
                "is_recommended": False,
                "event_titles": ["Свадьба", "Без повода"],
                "relative_img_path": os.path.join("catalog", "catalogBg2.jpg"),
            },
            {
                "title": "Комплимент",
                "slug": "kompliment",
                "description": (
                    "Изящный полевой букет из разноцветных цветов, "
                    "собранный в легком природном стиле. "
                    "Прекрасное сочетание фиолетовых астр, "
                    "нежной ромашковой хризантемы и свежей зелени. "
                    "Идеальный и ненавязчивый способ сказать «Спасибо» или напомнить о себе."
                ),
                "composition": (
                    "Хризантема ромашковая — 3 шт., Астра фиолетовая кустовая — 5 шт., "
                    "Полевые травы и статица — 4 шт., Атласная лента."
                ),
                "size": "Высота — 45 см, Ширина — 25 см",
                "price": 1800.00,
                "is_recommended": False,
                "event_titles": ["День рождения", "Без повода"],
                "relative_img_path": os.path.join("catalog", "catalogBg3.jpg"),
            },
            {
                "title": "Весеннее танго",
                "slug": "vesennee-tango",
                "description": (
                    "Яркие сортовые тюльпаны насыщенного малиново-розового оттенка "
                    "в обрамлении свежих зеленых листьев. Букет буквально дышит свежестью, "
                    "весной и молодостью. Отличный подарок на день рождения или просто "
                    "как романтический сюрприз без особого повода."
                ),
                "composition": (
                    "Тюльпан сортовой розовый — 15 шт., Берграс и декоративные листья — 7 шт., "
                    "Лаконичная прозрачная лента."
                ),
                "size": "Высота — 40 см, Ширина — 30 см",
                "price": 2100.00,
                "is_recommended": False,
                "event_titles": ["День рождения", "Без повода"],
                "relative_img_path": os.path.join("catalog", "catalogBg4.jpg"),
            },
        ]

        static_img_base_dir = os.path.join(settings.BASE_DIR, "static", "img")

        for b_data in test_bouquets:
            bouquet, created = Bouquet.objects.get_or_create(
                slug=b_data["slug"],
                defaults={
                    "title": b_data["title"],
                    "description": b_data["description"],
                    "composition": b_data["composition"],
                    "size": b_data["size"],
                    "price": b_data["price"],
                    "is_recommended": b_data["is_recommended"],
                },
            )

            if created:
                local_file_path = os.path.join(static_img_base_dir, b_data["relative_img_path"])

                if os.path.exists(local_file_path):
                    try:
                        with open(local_file_path, "rb") as f:
                            bouquet.image.save(f"{b_data['slug']}.jpg", File(f), save=True)
                    except Exception as e:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Не удалось прикрепить файл для {b_data['title']}: {e}"
                            )
                        )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"Файл не найден по пути: {local_file_path}")
                    )

                for e_title in b_data["event_titles"]:
                    if e_title in events:
                        bouquet.events.add(events[e_title])

                self.stdout.write(f"Создан букет: {bouquet.title}")

        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно загружены!"))
