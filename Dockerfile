FROM fedora:23

RUN dnf install -y dnf-plugins-core && \
    dnf copr enable -y mstuchli/Python3.5 && \
    dnf install -y python35-python3 git && \
    dnf clean all


RUN pip3.5 install aiohttp aiohttp_mako ipdb praw
ADD . /voxreddi
WORKDIR /voxreddi
#RUN pip3 install -r requirements.txt

EXPOSE 8080

CMD ["env", "PYTHONASYNCIODEBUG=1", "python3.5", "vox_reddi_web.py", "0.0.0.0:8080"]
