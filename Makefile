BUILD_VERSION=0.1

S3_BUCKET=<your bucket name>

all: package upload upload-config

package:
	@printf "Packaging application...\n"
	zip -r embriq-some-$(BUILD_VERSION).zip app/

upload:
	@printf "\nUploading application to S3-bucket: $(S3_BUCKET)...\n"
	aws s3 cp embriq-some-$(BUILD_VERSION).zip s3://$(S3_BUCKET)/application/
	rm embriq-some-$(BUILD_VERSION).zip

upload-config:
	@printf "\nUploading config to S3-bucket: $(S3_BUCKET)...\n"
	aws s3 cp config/config.json s3://$(S3_BUCKET)/config/
