from rest_framework import serializers
from .models import AwardedMarks, SubtractMarks, Disciplinetype, StudentScore, Voice


class AwardedMarksSerializer(serializers.ModelSerializer):
    class Meta:
        model=AwardedMarks
        fields='__all__'


class SubtractMarksSerializer(serializers.ModelSerializer):
    # Marks=serializers.CharField(write_only=True,allow_null=True)
    Disciplinetype_id=serializers.IntegerField()
    Disciplinetype=serializers.SlugRelatedField(slug_field='name',read_only=True)
    class Meta:
        model=SubtractMarks
        fields='__all__'


class DisciplinetypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Disciplinetype
        fields='__all__'


class MarksListSerializer(serializers.ModelSerializer):
    # disciplinetype=serializers.SlugRelatedField(queryset=MarksList.objects.all(),slug_field="name")
    # disciplinetype_id=serializers.IntegerField(read_only=True)
    avatar=serializers.CharField(write_only=True)
    # avatar=serializers.FileField(read_only  =True)
    class Meta:
        model=StudentScore
        fields='__all__'

        # exclude = ['avatar']

class MarksListSerializert(serializers.ModelSerializer):
    # avatar=serializers.CharField(write_only=True)
    avatar=serializers.FileField(read_only  =True)
    class Meta:
        model=StudentScore
        fields='__all__'

class VoiceSerializer(serializers.ModelSerializer):
    # avatar=serializers.CharField(write_only=True)
    # avatar=serializers.FileField(read_only  =True)
    class Meta:
        model=Voice
        fields='__all__'




