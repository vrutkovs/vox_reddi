FROM fedora:23

RUN dnf install -y python3-pip git && dnf clean all


RUN pip3 install git+https://github.com/pyGrowler/growler \
                 git+https://github.com/pyGrowler/growler-mako \
                 ipdb praw
ADD . /voxreddi
WORKDIR /voxreddi
#RUN pip3 install -r requirements.txt

EXPOSE 8080

CMD ["python3", "vox_reddi_web.py", "0.0.0.0:8080"]
