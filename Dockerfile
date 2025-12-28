FROM ubuntu:22.04

# जरूरी सॉफ्टवेयर इंस्टॉल करना
RUN apt-get update && apt-get install -y openssh-server figlet

# तुम्हारा SHIVA NETWORK वाला धाकड़ बैनर (लोगो)
RUN figlet -f slant "SHIVA NETWORK" > /etc/ssh/banner.txt && \
    echo "====================================" >> /etc/ssh/banner.txt && \
    echo "   WELCOME TO SHIVA VIP SERVER      " >> /etc/ssh/banner.txt && \
    echo "   STATUS: CONNECTED (PORT 80)      " >> /etc/ssh/banner.txt && \
    echo "====================================" >> /etc/ssh/banner.txt

# SSH को पोर्ट 80 पर सेट करना और बैनर लिंक करना
RUN sed -i 's/#Port 22/Port 80/' /etc/ssh/sshd_config && \
    echo "Banner /etc/ssh/banner.txt" >> /etc/ssh/sshd_config && \
    mkdir /var/run/sshd

# यूजर और पासवर्ड (User: shiva | Pass: shiva123)
RUN useradd -m shiva && echo "shiva:shiva123" | chpasswd

EXPOSE 80
CMD ["/usr/sbin/sshd", "-D"]
