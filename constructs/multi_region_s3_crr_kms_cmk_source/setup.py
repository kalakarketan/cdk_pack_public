import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="multi_region_s3_crr_kms_cmk_source",
    version="0.0.1",
    description="Multi region S3 CRR KMS CMK Source Construct",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="author",
    package_dir={"": "constructs/multi_region_s3_crr_kms_cmk_source/lib"},
    packages=setuptools.find_packages(where="multi_region_s3_crr_kms_cmk_source"),
    install_requires=[
        "aws-cdk-lib==2.94.0",
        "constructs>=10.0.0,<11.0.0"
    ],
)
