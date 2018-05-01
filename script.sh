#!/bin/bash

function essential(){
  ### Update repositories
  sudo apt-get -y update

  ### Install essential packages
  sudo apt-get install -y python-pip3 python-dev build-essential

  # Check Essential packages install
  if [ $? = 0 ]; then
    echo "Installation Successfully"
  else
    echo "Problems to install Essential packages, check this!"
    exit 1
  fi
}

function flask() {
  # Install numpy
  sudo pip3 install Flask

  # Check numpy install
  if [ $? = 0 ]; then
    echo "Installation Successfully"
  else
    echo "Problems to install Flask, check this!"
    exit 1
  fi
}

function SQLalchemy() {
  # Install numpy
  sudo pip3 install SQLalchemy

  # Check numpy install
  if [ $? = 0 ]; then
    echo "Installation Successfully"
  else
    echo "Problems to install SQLalchemy, check this!"
    exit 1
  fi
}

function FlaskUser() {
  # Install numpy
  sudo pip3 install "Flask-User<0.7"

  # Check numpy install
  if [ $? = 0 ]; then
    echo "Installation Successfully"
  else
    echo "Problems to install Flask-User, check this!"
    exit 1
  fi
}

function FlaskAdmin() {
  # Install numpy
  sudo pip3 install Flask-Admin

  # Check numpy install
  if [ $? = 0 ]; then
    echo "Installation Successfully"
  else
    echo "Problems to install Flask-Admin, check this!"
    exit 1
  fi
}

function FlaskUploads() {
  # Install numpy
  sudo pip3 install Flask-Uploads

  # Check numpy install
  if [ $? = 0 ]; then
    echo "Installation Successfully"
  else
    echo "Problems to install Flask-Uploads, check this!"
    exit 1
  fi
}

essential
flask
SQLalchemy
Flask-User
Flask-Admin
Flask-Uploads