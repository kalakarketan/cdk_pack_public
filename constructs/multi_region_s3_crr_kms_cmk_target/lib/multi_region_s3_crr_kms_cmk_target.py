from constructs import Construct
from aws_cdk import (
    aws_kms as kms,
    PhysicalName,
    aws_s3 as s3,
    Stack,
    aws_ssm as ssm
)


class MultiRegionS3CrrKmsCmkTarget(Construct):
    @property
    def target_bucket(self):
        return self._target_bucket
    @property
    def target_key_id_ssm_parameter_name(self):
        return self._parameter_name

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        _target_kms_key = kms.Key(self, 'MyTargetKey')
        
        _target_bucket = s3.Bucket(self, 'MyTargetBucket',
            bucket_name=PhysicalName.GENERATE_IF_NEEDED,
            encryption=s3.BucketEncryption.KMS,
            encryption_key=_target_kms_key,
            versioned=True
        )

        _stack = Stack.of(self)
        _parameter_name = f'{_stack.stack_name}.MyTargetKeyId'
        
        ssm.StringParameter(self, 'MyTargetKeyIdSSMParam',
            parameter_name=_parameter_name,
            description='The KMS Key Id for the target stack',
            string_value=_target_kms_key.key_arn
        )
        
        self._target_bucket = _target_bucket
        self._parameter_name = _parameter_name
