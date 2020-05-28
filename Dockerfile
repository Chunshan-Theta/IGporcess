FROM joyzoursky/python-chromedriver:3.7-selenium 

RUN mkdir -p ~/home/lib
#RUN apt-get update
#RUN apt-get install autokey-gtk -y
#RUN apt-get install dbus-x11 -y
#RUN export $(dbus-launch)



ADD ./ /home

WORKDIR /home
CMD ["/bin/bash"]



