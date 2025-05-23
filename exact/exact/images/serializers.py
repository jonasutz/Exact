from rest_framework.serializers import ModelSerializer

from exact.administration.serializers import ProductSerializer
from exact.images.models import FrameDescription
from exact.users.serializers import UserSerializer, TeamSerializer
from exact.images.models import ImageSet, Image, SetTag, ScreeningMode, SetVersion, ImageRegistration
from typing import Dict, Any
from rest_flex_fields import FlexFieldsModelSerializer

class ImageSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Image
        fields = (
            'id',
            'name',
            'filename',
            'time',
            'height',
            'width',
            'depth',
            'frames',
            'channels',
            'mpp',
            'objectivePower',
            'FrameDescriptions',
            'defaultFrame',
            'image_type',
            'image_set',
            'annotations'
        )

        expandable_fields = {
            "image_set": ('exact.images.serializers.ImageSetSerializer', {'read_only': True}),
            "annotations": ('exact.annotations.serializers.AnnotationSerializer', {'read_only': True}),
            "FrameDescriptions" : ('exact.images.serializers.FrameDescriptionSerializer', {'read_only': True, 'many':True}),
        }

class AuxiliaryFileSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Image
        fields = (
            'id',
            'name',
            'filename',
            'description',
            'creator',
            'associated_to_image',
            'time',
            'filesize',
            'image_set',
        )

        expandable_fields = {
            "image_set": ('exact.images.serializers.ImageSetSerializer', {'read_only': True}),
            "associated_to_image": ('exact.images.serializers.ImageSerializer', {'read_only': True}),
        }




class SetTagSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = SetTag
        fields = (
            'id',
            'name',
            'imagesets'
        )

        expandable_fields = {
            "imagesets": ('exact.images.serializers.ImageSetSerializer', {'read_only': True, 'many': True}),
        }

class SetVersionSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = SetVersion
        fields = (
            'id',
            'name',
            'imagesets',
            'time',
            'annotationversion_set',
            'file'
        )

        expandable_fields = {
            "annotationversion_set": ('exact.annotations.serializers.AnnotationVersionSerializer', {'read_only': True, 'many': True}),
            "imagesets": ('exact.images.serializers.ImageSetSerializer', {'read_only': True, 'many': True}),
        }

class ScreeningModeSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = ScreeningMode
        fields = (
            'id',
            'image',
            'user',
            'screening_tiles',
            'x_steps',
            'y_steps',
            'x_resolution',
            'y_resolution',
            'current_index'
        )

        expandable_fields = {
            "image": (ImageSerializer, {'read_only': True}),
            "user": (UserSerializer, {'read_only': True}),
        }

class ImageRegistrationSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = ImageRegistration
        fields = (
            'id',
            'source_image',
            'target_image',
            'transformation_matrix',
            'registration_error',
            'runtime',
            'file',
            'rotation_angle',
            'inv_matrix',
            'get_scale',
            'get_inv_scale'
        )

        expandable_fields = {
            "source_image": (ImageSerializer, {'read_only': True}),
            "target_image": (ImageSerializer, {'read_only': True}),
        }

class FrameDescriptionSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = FrameDescription 
        fields = ('description',
                  'frame_id',
                  'frame_type')
        

class ImageSetSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = ImageSet
        fields = (
            'id',
            'name',
            'path',
            'location',
            'description',
            'images',
            'product_set',
            'main_annotation_type',
            'set_tags',
            'team',
            'creator',
            'collaboration_type',
            'show_registration'
        )

        expandable_fields = {
            "team": (TeamSerializer, {'read_only': True}),
            "creator": (UserSerializer, {'read_only': True}),
            "images": (ImageSerializer, {'read_only': True, 'many': True}),
            "product_set": (ProductSerializer, {'read_only': True, 'many': True}),
            "set_tags": (SetTagSerializer, {'read_only': True, 'many': True}),
            "main_annotation_type": ('exact.annotations.serializers.AnnotationTypeSerializer', {'read_only': True}),
        }

def serialize_imageset(imageset: ImageSet) -> Dict[str, Any]:
    return {
        'id': imageset.id,
        'name': imageset.name,
        'location': imageset.location,
        'description': imageset.description,
        'team': {
            'id': imageset.team.id,
            'name': imageset.team.name
        },
        'images': [ {
            'id': image.id,
            'name': image.name,
            "height": image.height,
            "width": image.width,
            "mpp": image.mpp,
            "objectivePower": image.objectivePower,
            'image_type': image.image_type
        } for image in imageset.images.all()
        ],
        'products' : 
        [ 
            {'name': product.name,
             'id' : product.id,
             'annotation_types': [{
                 'id': annotation_type.id,
                 'closed': annotation_type.closed,
                 'name': annotation_type.name,
                 'vector_type': annotation_type.vector_type,
                 'color_code': annotation_type.color_code,
                 'multi_frame': annotation_type.multi_frame,
                 'area_hit_test': annotation_type.area_hit_test
             } for annotation_type in product.annotationtype_set.all()]
             }
            for product in imageset.product_set.all()
        ],
        'tags':
            [
                {
                    'name': tag.name,
                    'id': tag.id,
                 }
                for tag in imageset.set_tags.all()
            ],
        'main_annotation_type': 
        { 
            'id': imageset.main_annotation_type.id,
            'closed': imageset.main_annotation_type.closed,
            'name': imageset.main_annotation_type.name,
            'vector_type': imageset.main_annotation_type.vector_type,
            'color_code': imageset.main_annotation_type.color_code,
            'multi_frame' : imageset.main_annotation_type.multi_frame,
            'area_hit_test' : imageset.main_annotation_type.area_hit_test
        } if imageset.main_annotation_type is not None else None
    }