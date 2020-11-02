
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -q -y doxygen graphviz python3-pip python3-yaml wget
RUN pip3 install sphinx
RUN pip3 install breathe
RUN pip3 install exhale

RUN mkdir -p  /cross-refs /output /doc_root/package
COPY build_docs.py /doc_root
COPY conf.py /doc_root
COPY index.rst /doc_root
RUN chmod -R a+rwx /doc_root
WORKDIR /doc_root
