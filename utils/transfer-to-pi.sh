#!/bin/bash

PI_IP="<your pis IP>"
PI_USER="pi"

rsync -av ../piUtils/ $PI_USER@$PI_IP:programs/embriq-some/
