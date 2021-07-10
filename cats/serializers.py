from rest_framework import serializers
import datetime as dt
import webcolors

from .models import Cat, Owner, Achievement, AchievementCat, CHOICES


class Hex2NameColor(serializers.Field):
    """Конвертация цвета из HEX в название."""
    # При чтении данных ничего не меняем - просто возвращаем как есть
    def to_representation(self, value):
        return value
    # При записи код цвета конвертируется в его название
    def to_internal_value(self, data):
        # Доверяй, но проверяй
        try:
            # Если имя цвета существует, то конвертируем код в название
            data = webcolors.hex_to_name(data)
        except ValueError:
            # Иначе возвращаем ошибку
            raise serializers.ValidationError('Для этого цвета нет имени')
     # Возвращаем данные в новом формате
        return data


class AchievementSerializer(serializers.ModelSerializer):
    achievement_name = serializers.CharField(source='name')

    class Meta:
        model = Achievement
        fields = ('id', 'achievement_name')


class CatSerializer(serializers.ModelSerializer):
    achievements = AchievementSerializer(many=True)
    age = serializers.SerializerMethodField()
    # color = Hex2NameColor()
    # color = serializers.ChoiceField(choices=CHOICES)

    class Meta:
        model = Cat
        fields = ('id', 'name', 'color', 'birth_year', 'owner', 'achievements', 'age')

    def create(self, validated_data):
        # Если в исходном запросе не было поля achievements
        if 'achievements' not in self.initial_data:
            # То создаём запись о котике без его достижений
            cat = Cat.objects.create(**validated_data)
            return cat
        else:
            # Уберем список достижений из словаря validated_data и сохраним его
            achievements = validated_data.pop('achievements')
            # Иначе сначала добавляем котика в БД
            cat = Cat.objects.create(**validated_data)
            # А потом добавляем его достижения в БД
            for achievement in achievements:
                # Создадим новую запись или получим существующий экземпляр из БД
                current_achievement, status = Achievement.objects.get_or_create(
                    **achievement)
                # И связываем каждое достижение с этим котиком
                AchievementCat.objects.create(
                    achievement=current_achievement, cat=cat)
            return cat

    def get_age(self, obj):
        return dt.datetime.now().year - obj.birth_year


class CatListSerializer(serializers.ModelSerializer):
    color = serializers.ChoiceField(choices=CHOICES)

    class Meta:
        model = Cat
        fields = ('id', 'name', 'color')


class OwnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Owner
        fields = ('first_name', 'last_name', 'cats')
