import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="multi_region_s3_crr_kms_cmk_target",
    version="0.0.1",
    description="Multi region S3 CRR KMS CMK Target Construct",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="author",
    package_dir={"": "lib"},
    packages=setuptools.find_packages(where="multi_region_s3_crr_kms_cmk_target"),
    install_requires=[
        "aws-cdk-lib==2.94.0",
        "constructs>=10.0.0,<11.0.0"
    ],
)
