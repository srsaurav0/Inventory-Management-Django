from inventory.models import LocalizeAccommodation, Accommodation

def run():
    descriptions = {
        "EN": "A luxurious stay with top-notch amenities.",
        "FR": "Un séjour luxueux avec des équipements de premier ordre.",
        "ES": "Una estancia lujosa con servicios de primera calidad.",
        "BD": "শীর্ষস্থানীয় সুযোগ-সুবিধাসহ একটি বিলাসবহুল থাকার ব্যবস্থা।",
        "AR": "إقامة فاخرة مع وسائل الراحة من الدرجة الأولى."
    }

    policies = {
        "EN": {"pet_policy": "Pets are allowed with prior approval."},
        "FR": {"pet_policy": "Les animaux sont autorisés avec approbation préalable."},
        "ES": {"pet_policy": "Se permiten mascotas con aprobación previa."},
        "BD": {"pet_policy": "পূর্ব অনুমোদনের সঙ্গে পোষা প্রাণীদের অনুমতি দেওয়া হয়।"},
        "AR": {"pet_policy": "مسموح بالحيوانات الأليفة بموافقة مسبقة."}
    }

    accommodations = Accommodation.objects.all()[:10]  # Get 10 accommodations

    for accommodation in accommodations:
        for lang, description in descriptions.items():
            LocalizeAccommodation.objects.get_or_create(
                property=accommodation,
                language=lang,
                defaults={
                    "description": description,
                    "policy": policies[lang],
                }
            )

    print("Localized data added successfully!")

run()