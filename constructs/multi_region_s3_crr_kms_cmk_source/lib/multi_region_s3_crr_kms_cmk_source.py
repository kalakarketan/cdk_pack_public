from constructs import Construct
from aws_cdk import (
  aws_s3 as s3,
  aws_kms as kms,
  Stack,
  custom_resources as cr,
  PhysicalName,
  aws_iam as iam
)
import time
from dataclasses import dataclass


@dataclass
class MultiRegionS3CrrKmsCmkSourceProps:
  target_bucket: s3.Bucket
  target_key_id_ssm_parameter_name: str
  target_region: str

class MultiRegionS3CrrKmsCmkSource(Construct):

    def __init__(self, scope: Construct, construct_id: str,
                 props: MultiRegionS3CrrKmsCmkSourceProps, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        _source_kms_key = kms.Key(self, 'MySourceKey')

        _stack = Stack.of(self)
        _parameter_arn = _stack.format_arn(
            account=_stack.account,
            region=props.target_region,
            resource='parameter',
            resource_name=props.target_key_id_ssm_parameter_name,
            service='ssm'
        )
        
        _target_key_lookup_cr = cr.AwsCustomResource(self, 'TargetKeyLookup',
            on_update = cr.AwsSdkCall(  # will also be called for a CREATE event
                service = 'SSM',
                action = 'getParameter',
                parameters = {
                    'Name': props.target_key_id_ssm_parameter_name
                    },
                region = props.target_region,
                physical_resource_id = cr.PhysicalResourceId.of(str(int(time.time())))
            ),
            policy=cr.AwsCustomResourcePolicy.from_sdk_calls(resources=[_parameter_arn])
        )
        
        _source_bucket = s3.Bucket(self, 'MySourceBucket',
            bucket_name=PhysicalName.GENERATE_IF_NEEDED,
            encryption=s3.BucketEncryption.KMS,
            encryption_key=_source_kms_key,
            versioned=True
        )
        
        _role = iam.Role(self, 'MyCrrRole',
            assumed_by=iam.ServicePrincipal('s3.amazonaws.com'),
            path='/service-role/'
        )
        
        _role.add_to_policy(iam.PolicyStatement(
            resources=[_source_bucket.bucket_arn],
            actions=['s3:GetReplicationConfiguration', 's3:ListBucket']
        ))
        
        _role.add_to_policy(iam.PolicyStatement(
            resources=[_source_bucket.arn_for_objects('*')],
            actions=[
                's3:GetObjectVersion',
                's3:GetObjectVersionAcl',
                's3:GetObjectVersionForReplication',
                's3:GetObjectLegalHold',
                's3:GetObjectVersionTagging',
                's3:GetObjectRetention'
            ]
        ))
        
        _role.add_to_policy(iam.PolicyStatement(
            resources=[props.target_bucket.arn_for_objects('*')],
            actions=[
                's3:ReplicateObject',
                's3:ReplicateDelete',
                's3:ReplicateTags',
                's3:GetObjectVersionTagging'
            ]
        ))
        
        _role.add_to_policy(iam.PolicyStatement(
            resources=[_source_kms_key.key_arn],
            actions=['kms:Decrypt']
        ))
        
        _role.add_to_policy(iam.PolicyStatement(
            resources=[_target_key_lookup_cr.get_response_field('Parameter.Value')],
            actions=['kms:Encrypt']
        ))
        
        # Get the AWS CloudFormation resource
        _cfn_bucket = _source_bucket.node.default_child
        
        # Change its properties
        _cfn_bucket.replication_configuration = s3.CfnBucket.ReplicationConfigurationProperty(
            role=_role.role_arn,
            rules=[
                s3.CfnBucket.ReplicationRuleProperty(
                    destination=s3.CfnBucket.ReplicationDestinationProperty(
                        bucket=props.target_bucket.bucket_arn,
                        encryption_configuration=s3.CfnBucket.EncryptionConfigurationProperty(
                            replica_kms_key_id=_target_key_lookup_cr.get_response_field('Parameter.Value')
                        )
                    ),
                    source_selection_criteria=s3.CfnBucket.SourceSelectionCriteriaProperty(
                        sse_kms_encrypted_objects=s3.CfnBucket.SseKmsEncryptedObjectsProperty(
                            status='Enabled'
                        )
                    ),
                    status='Enabled'
                )
            ]
        )
