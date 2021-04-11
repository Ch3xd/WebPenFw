import os

from flask import Blueprint, render_template, request, make_response

from App.settings import fuzz_domian_path

blueEnum = Blueprint('domain_blue',__name__)


@blueEnum.route('/Log',methods=['GET','POST'])
def domainEnum():
    return render_template('log.html')