from flask import g
from flask_restful import Resource, Api, reqparse
from models import EducationsModel, JobSeekersModel
from models.job_seeker import auth
from db import db


class Educations(Resource):

    def get(self, username):
        account = JobSeekersModel.find_by_username(username)
        if not account:
            return {'account': None}, 404
        return [education.json() for education in account.educations], 200

    @auth.login_required(role='user')
    def post(self, username):

        if username != g.user.username:
            return {'message': 'Access denied'}, 400

        parser = reqparse.RequestParser()

        parser.add_argument('title', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('institution', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('start_date', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('end_date', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('currently', type=bool, required=True, help="This field cannot be left blank")

        data = parser.parse_args()

        user = JobSeekersModel.find_by_username(username)

        if data.title.isspace():
            return {"message": "Title cannot be blank"}, 400

        if not user:
            return {'user': None}, 404

        start_year, start_month = data.start_date.split('-')
        end_year, end_month = data.end_date.split('-')
        if not data.currently and int(start_year) >= int(end_year):
            if int(start_month) > int(end_month):
                return {"message": "Start date cannot be later than end date"}, 400

        new_education = EducationsModel(data.title, data.institution, data.start_date, data.end_date, data.currently)
        user.educations.append(new_education)

        try:
            db.session.add(user)
            db.session.add(new_education)
            db.session.commit()
            return {'education': new_education.json()}, 200
        except:
            db.session.rollback()
            return {"message": "An error occurred inserting the order."}, 500

    #@auth.login_required(role='user')
    def delete(self, username):

        #if username != g.user.username:
            #return {'message': 'Access denied'}, 400

        parser = reqparse.RequestParser()

        parser.add_argument('id', type=int, required=True, help="This field cannot be left blank")

        data = parser.parse_args()

        user = JobSeekersModel.find_by_username(username)

        education=user.delete_education(data.id)

        if education:
            education.delete_from_db(db)
            return {'message': "Education with id [{}] deleted".format(id)}, 200

        return {'message': "Education with id [{}] don't exists".format(id)}, 400



