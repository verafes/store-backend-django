docker run \
  -p 9000:9000 \
  -p 9090:9090 \
  --name minio1 \
  -v D:\Assigments\Project\django\minio\data:/data \
  -e "MINIO_ROOT_USER=ROOTNAME" \
  -e "MINIO_ROOT_PASSWORD=CHANGEME123" \
  quay.io/minio/minio server /data --console-address ":9090"