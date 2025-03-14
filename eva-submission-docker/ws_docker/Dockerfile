FROM tomcat:9.0-jdk11

RUN apt update  \
    && apt install -y git maven

COPY maven-settings.xml /root
ADD ws_docker/docker_mocked_services /usr/local/software/docker_mocked_services

WORKDIR /usr/local/software

# make manager app available
RUN cp -avT /usr/local/tomcat/webapps.dist/manager /usr/local/tomcat/webapps/manager

RUN mvn package -f docker_mocked_services/pom.xml
RUN cp docker_mocked_services/target/docker_mocked_services-*.war.original /usr/local/tomcat/webapps/docker_mocked_services.war

# deploy count-stats
RUN git clone https://github.com/EBIvariation/eva-ws.git
RUN mvn package -s /root/maven-settings.xml -f eva-ws/count-stats/pom.xml -P docker -DskipTests
RUN cp eva-ws/count-stats/target/count-stats-*.war /usr/local/tomcat/webapps/count-stats.war

RUN git clone https://github.com/EBIvariation/contig-alias.git
RUN mvn package -s /root/maven-settings.xml -f contig-alias/pom.xml -P docker -DskipTests
RUN cp contig-alias/target/contig-alias-*.war.original /usr/local/tomcat/webapps/contig-alias.war

EXPOSE 8080

CMD ["catalina.sh", "run"]


