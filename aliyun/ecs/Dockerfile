FROM python:3.7-slim
LABEL maintainer="yaokun <yaokun@bwcxtech.com>"
ENV TZ "Asia/Shanghai"

COPY aliyun /opt

WORKDIR /opt

RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

ENTRYPOINT ["python3", "security_group.py"]