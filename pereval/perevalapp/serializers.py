from rest_framework import serializers
from .models import Pereval, Coordinate, Image, User, Level


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'surname',
            'name',
            'patronymic',
            'email',
            'phone_number'
        )


class CoordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinate
        fields = (
            'length',
            'width',
            'height'
        )


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = (
            'winter_level',
            'summer_level',
            'spring_level',
            'autumn_level'
        )


class ImageSerializer(serializers.ModelSerializer):


    class Meta:
        model = Image
        fields = (
            'title',
            'data'
        )


class PerevalSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordSerializer()
    level = LevelSerializer()
    image = ImageSerializer(many=True)
    add_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Pereval
        fields = (
            'beauty_title',
            'title',
            'other_titles',
            'connect',
            'add_time',
            'user',
            'coords',
            'level',
            'image',
            'status'
        )

    def validate(self, data):
        if self.instance is not None and 'user' in data:
            instance_user = self.instance.user
            data_user = data['user']  # Необходимо убедиться, что это словарь
            for field in ['email', 'phone_number', 'surname', 'name', 'patronymic']:
                if field in data_user and getattr(instance_user, field) != data_user[field]:
                    raise serializers.ValidationError({'Ошибка': 'Данные пользователя заменить нельзя'})

        return data



    def create(self, validated_data):
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        level_data = validated_data.pop('level')
        image_data = validated_data.pop('image')

        user_instance = User.objects.create(**user_data)
        coords_instance = Coordinate.objects.create(**coords_data)
        level_instance = Level.objects.create(**level_data)
        pereval = Pereval.objects.create(**validated_data, user=user_instance, coords=coords_instance,
                                         level=level_instance)

        for img_data in image_data:
            title = img_data.pop('title')
            image_file = img_data.pop('data')
            Image.objects.create(pereval=pereval, title=title,
                                 image=image_file)
        return pereval

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()

        coords_data = validated_data.pop('coords')
        if coords_data:
            for attr, value in coords_data.items():
                setattr(instance.coords, attr, value)
            instance.coords.save()

        level_data = validated_data.pop('level')
        if level_data:
            for attr, value in level_data.items():
                setattr(instance.level, attr, value)
            instance.level.save()

        image_data = validated_data.pop('image', [])
        exlisting_images = {img.id: img for img in instance.image.all()}

        for img_data in image_data:
            img_id = img_data.get('id')
            if img_id and img_id in exlisting_images:
                img_instance = exlisting_images[img_id]
                img_instance.title = img_data.get('title', img_instance.title)
                img_instance.image = img_data.get('data', img_instance.data)
                img_instance.save()
            else:
                Image.objects.create(pereval=instance, **img_data)

        image_ids_in_request = {img.get('id') for img in image_data if img.get('id')}
        for img_id in exlisting_images:
            if img_id not in image_ids_in_request:
                exlisting_images[img_id].delete()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

