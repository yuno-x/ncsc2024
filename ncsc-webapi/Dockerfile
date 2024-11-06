FROM python:3

RUN chmod 1733 /tmp; \
    useradd -m -s /bin/bash ncsc-user; \
    su ncsc-user -c 'pip install flask'; \
    chmod 1733 /tmp /var/tmp; \
    chown -R root:root /home/ncsc-user/; \
    touch /home/ncsc-user/.hushlogin; \
    chmod o+rx /home/ncsc-user/;

CMD su ncsc-user -c '( cd /home/ncsc-user/; python3 app.py; )'
