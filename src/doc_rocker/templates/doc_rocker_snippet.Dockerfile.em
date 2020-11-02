
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -q -y doxygen graphviz python3-empy python3-pip python3-yaml wget
RUN pip3 install catkin-pkg
RUN pip3 install sphinx
RUN pip3 install breathe
RUN pip3 install exhale

RUN mkdir -p  /crossref /output /doc_root/package
COPY build_docs.py /doc_root
COPY conf.py.em /doc_root
COPY index.rst.em /doc_root
RUN chmod -R a+rwx /doc_root
WORKDIR /doc_root
