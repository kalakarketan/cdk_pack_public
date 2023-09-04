import aws_cdk as core
import aws_cdk.assertions as assertions

from multi_region_s3_crr_kms_cmk_source.multi_region_s3_crr_kms_cmk_source_stack import MultiRegionS3CrrKmsCmkSourceStack

# example tests. To run these tests, uncomment this file along with the example
# resource in multi_region_s3_crr_kms_cmk_source/multi_region_s3_crr_kms_cmk_source_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MultiRegionS3CrrKmsCmkSourceStack(app, "multi-region-s3-crr-kms-cmk-source")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
