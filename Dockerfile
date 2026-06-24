FROM ubuntu:22.04

# आवश्यक पैकेज इंस्टॉल करना
RUN apt-get update && apt-get install -y \
    openssh-server \
    nodejs \
    npm \
    git \
    && rm -rf /var/lib/apt/lists/*

# SSH कॉन्फ़िगरेशन
RUN mkdir /var/run/sshd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# तुम्हारा कस्टम यूजर (shivam) और पासवर्ड (s) बनाना
RUN useradd -m -s /bin/bash shivam
RUN echo 'shivam:s' | chpasswd

# तुम्हारा कस्टम बैनर सेट करना
COPY banner.txt /etc/ssh/banner.txt
RUN echo "Banner /etc/ssh/banner.txt" >> /etc/ssh/sshd_config

# वेबसॉकेट प्रॉक्सी स्क्रिप्ट सेट करना
WORKDIR /app
COPY package.json .
COPY server.js .
RUN npm install

# रेंडर का डिफ़ॉल्ट पोर्ट एक्सपोज़ करना
EXPOSE 10000

# SSH और WS Server दोनों को एक साथ चालू करना
CMD service ssh start && node server.js
