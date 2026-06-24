FROM ubuntu:latest

RUN apt-get update && apt-get install -y dropbear python3 curl && apt-get clean

# Yahan tera fixed username aur password set ho raha hai system me
RUN useradd -M -s /bin/false shivam && echo "shivam:boss" | chpasswd
RUN echo "/bin/false" >> /etc/shells

WORKDIR /app
COPY . /app

RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]
