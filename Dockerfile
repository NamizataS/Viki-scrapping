FROM python:3.8

RUN mkdir /home/dev/ && mkdir /home/dev/code/

WORKDIR /home/dev/code/

#ENV http_proxy http://147.215.1.189:3128
#ENV https_proxy http://147.215.1.189:3128

COPY . .
RUN  pip install --upgrade pip &&  pip install pipenv && pipenv install --skip-lock

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

# install selenium
RUN pip install selenium==3.8.0

CMD ["pipenv", "run", "jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--allow-root", "--NotebookApp.token=''"]
#CMD ["/bin/bash"]
