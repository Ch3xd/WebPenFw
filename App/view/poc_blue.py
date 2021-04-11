from App.ext import db
from App.model import User
from App.public.fofa_public import getip_list
from App.public.file_oper import *
from App.public.global_var import *
from flask import Blueprint, render_template, request

blue_poc = Blueprint('blue_poc',__name__)

@blue_poc.route('/poc')
def index_poc():
    return render_template('poc.html')