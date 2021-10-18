from flask_restful import Resource

from models.company import CompanyModel


class CompanyList(Resource):
    """
        Resource that lists all the companies in the database
    """
    def get(self):
        """
        HTTP method of the resource CompanyList
        :return: list of all the companies in the database
        """
        companyList = [x.json() for x in CompanyModel.query.all()]
        if len(companyList) > 0:
            return companyList, 200
        else:
            return {'message': "There are no companies"}, 404