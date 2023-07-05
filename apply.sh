docker build -t globantcompiler:1.0.0 .
docker run --name flasgger -p 4000:4000 -d globantcompiler:1.0.0