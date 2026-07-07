@echo off
SET _JAVA_OPTIONS=-Djava.library.path=C:\hadoop\bin
SET HADOOP_HOME=C:\hadoop
SET PATH=C:\hadoop\bin;%PATH%

python -m src.streaming.kafka_to_bronze