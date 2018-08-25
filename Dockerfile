#FROM nvidia/cuda:8.0-cudnn5-runtime
FROM ubuntu:16.04
MAINTAINER srtm
LABEL OBJECT="just a practice"
ARG http_proxy
ARG https_proxy
ENV http_proxy ${http_proxy}
ENV https_proxy ${https_proxy}
ENV DEBIAN_FRONTEND noninteractive

# packages
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y --no-install-recommends apt-utils
RUN apt-get install -y --no-install-recommends apt-transport-https ca-certificates
RUN apt-get install -y --no-install-recommends software-properties-common
RUN apt-get install -y curl
RUN apt-get install -y language-pack-ja-base language-pack-ja
RUN apt-get install -y git
RUN apt-get install -y build-essential checkinstall
RUN apt-get install -y zlib1g-dev
RUN apt-get install -y unzip
RUN apt-get install -y libssl-dev
RUN apt-get install -y libbz2-dev libreadline-dev libsqlite3-dev
RUN apt-get install -y cmake libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
RUN apt-get install -y libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev
RUN apt-get install -y libeigen3-dev libarpack2-dev
RUN apt-get install -y libblas-dev liblapack-dev
RUN apt-get install -y liblog4cxx-dev
RUN apt-get install -y libboost-graph-dev libboost-system-dev libboost-graph-parallel1.58-dev
RUN apt-get install -y libhdf5-dev
# (optional) vim
RUN apt-get -y install vim
COPY .vimrc /root/
#
RUN apt-get -y update
RUN apt-get -y upgrade

# locale
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
RUN locale-gen en_US.UTF-8

# pyenv & python 3.6.3
RUN git clone https://github.com/yyuu/pyenv.git /root/.pyenv
ENV HOME /root
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/bin:$PATH
RUN echo 'export PYENV_ROOT="$HOME/.pyenv"' >> /root/.bashrc
RUN echo 'export PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"' >> /root/.bashrc
RUN echo 'eval "$(pyenv init -)"' >> /root/.bashrc
RUN ["/bin/bash", "-c", "source /root/.bashrc"]
RUN pyenv install 3.6.3
RUN pyenv global 3.6.3
RUN pyenv rehash
#RUN /root/.pyenv/shims/pip install numpy scipy matplotlib pandas h5py networkx
RUN /root/.pyenv/shims/pip install numpy scipy matplotlib pandas h5py networkx opencv-pytho

# codes
RUN mkdir -p /root/src
COPY extract_hesaff /root/src/extract_hesaff
