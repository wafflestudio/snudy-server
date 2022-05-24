from rest_framework import serializers

from semester.models import Semester


class SemesterSerializer(serializers.Serializer):
    year = serializers.IntegerField(required=True)
    type = serializers.CharField(required=True, max_length=10)

    def validate(self, data):
        type = data.get('type')

        if type not in ['FIRST', 'SECOND', 'SUMMER', 'WINTER']:
            raise serializers.ValidationError("type should be FIRST / SECOND / SUMMER / WINTER")
        return data

    def create(self, validated_data):
        year = validated_data.get('year', '')
        type = validated_data.get('type', '')

        semester = Semester.objects.create(year=year, type=type)

        return semester