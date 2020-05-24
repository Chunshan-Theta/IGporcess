FROM joyzoursky/python-chromedriver:3.7-selenium 

ADD ./test.py /home

CMD ["/bin/bash"]



