#!/bin/bash
FOLDER="https://raw.githubusercontent.com/Git-Clarusway/clarusway-aws-workshop/master/006-kittens-carousel-static-web-s3-cf/static-web/"
curl -s --create-dirs -o "/home/ec2-user/index.html" -L "$FOLDER"index.html
curl -s --create-dirs -o "/home/ec2-user/cat0.jpg" -L "$FOLDER"cat0.jpg
curl -s --create-dirs -o "/home/ec2-user/cat1.jpg" -L "$FOLDER"cat1.jpg
curl -s --create-dirs -o "/home/ec2-user/cat2.jpg" -L "$FOLDER"cat2.jpg
aws s3 cp cat0.jpg s3://clarusway.us
aws s3 cp cat1.jpg s3://clarusway.us
aws s3 cp cat2.jpg s3://clarusway.us
aws s3 cp index.html s3://bucket_name