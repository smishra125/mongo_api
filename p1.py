from flask import Flask
from flask_pymongo import PyMongo
import simplejson as json
from flask import request, jsonify
from flask_cors import CORS
import datetime as dt
import pytz
from  hourly_data import Hourly
from weekly import Weekly
from daily import Daily

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/parserdb"
mongo = PyMongo(app)
CORS(app)

@app.route('/hourlyreport/', methods=['GET'])
def hourly_report1():
    if 'site_id' in request.args:
        siteId = int(request.args['site_id'])
    else:
        return jsonify({})

    if 'sdate' in request.args:
        startDateStr = request.args['sdate']
    else:
        return jsonify({})
    if 'edate' in request.args:
        endDateStr = request.args['edate']
    else:
        return jsonify({})

    starttimeStr = startDateStr + " 04:30:00"
    endtimeStr = endDateStr + " 20:30:00"
    startDate = dt.datetime.strptime(starttimeStr, '%Y-%m-%d %H:%M:%S')
    endDate = dt.datetime.strptime(endtimeStr, '%Y-%m-%d %H:%M:%S')

    timezone = pytz.timezone('Asia/Kolkata')
    startDate = timezone.localize(startDate)
    endDate = timezone.localize(endDate)

    startTs = startDate.strftime('%s')
    endTs = endDate.strftime('%s')

    print("Start time ", startTs)
    print("End time ", endTs)

    site = list(mongo.db.m_site.find( {"$and":[ {"site_id":siteId},]}))
    plantrecord = list(mongo.db.plant_history.find( {"$and":[ {"site_id":siteId},{"record_timestamp": { "$gte": int(startTs)}},{"record_timestamp": {"$lte": int(endTs)}}]}))
    wst = list(mongo.db.wst_history.find( {"$and":[ {"site_id":siteId},{"record_timestamp": { "$gte": int(startTs)}},{"record_timestamp": {"$lte": int(endTs)}}]}))

    responseJson = {}
    if site is not None:
        for name in site:
            nameArr = []
            if name['site_id'] == siteId:
                data = name.get('site_name')
                nameArr.append(data)
                responseJson['site_Name'] = nameArr
    if plantrecord is not None and len(plantrecord) > 0:
        tsArr = []
        energyArr = []
        prArr = []
        cufArr = []
        for plant in plantrecord:
            ts = plant.get('record_time')
            todayenergy = plant.get('p_today_energy')
            pr = plant.get('p_pr')
            cuf = plant.get('p_cuf')
            tsArr.append(ts)
            energyArr.append(todayenergy)
            prArr.append(pr)
            cufArr.append(cuf)
            responseJson['timestamp'] = tsArr
            responseJson['Energy'] = energyArr
            responseJson['PR'] = prArr
            responseJson['CUF'] = cufArr
    if wst is not None and len(wst):
        wstArr = []
        for record in wst:
            irr = record.get('WSNSR')
            wstArr.append(irr)
            responseJson['Irradiance'] = wstArr
    # print(responseJson)
    data_report = Hourly(responseJson)
    hourly_data = data_report.get_hourly_report()
#    return jsonify(hourly_data)
    final_data = {
        "data" : hourly_data,

        "site_name": responseJson['site_Name'][0]
    }
    return jsonify(final_data)


@app.route('/weeklyreport/', methods=['GET'])
def weekly_report():
    if 'site_id' in request.args:
        siteId = int(request.args['site_id'])
    else:
        return jsonify({})

    site = list(mongo.db.m_site.find({"site_id":siteId}))
    plantrecord = list(mongo.db.plant_todayenergy.find({"site_id":siteId}))

    responseJson = {}
    if site is not None:
        for name in site:
            nameArr = []
            if name['site_id'] == siteId:
                data = name.get('site_name')
                nameArr.append(data)
                responseJson['site_Name'] = nameArr
    if plantrecord is not None and len(plantrecord) > 0:
        tsArr = []
        energyArr = []
        for plant in plantrecord:
            ts = plant.get('record_time')
            todayenergy = plant.get('p_today_energy')
            tsArr.append(ts)
            energyArr.append(todayenergy)
            responseJson['timestamp'] = tsArr
            responseJson['Energy'] = energyArr
    responseJson = {}
    if site is not None:
        for name in site:
            nameArr = []
            if name['site_id'] == siteId:
                data = name.get('site_name')
                nameArr.append(data)
                responseJson['site_Name'] = nameArr
    if plantrecord is not None and len(plantrecord) > 0:
        tsArr = []
        energyArr = []
        prArr = []
        cufArr = []
        for plant in plantrecord:
            ts = plant.get('record_time')
            todayenergy = plant.get('p_today_energy')
            pr = plant.get('p_pr')
            cuf = plant.get('p_cuf')
            tsArr.append(ts)
            energyArr.append(todayenergy)
            prArr.append(pr)
            cufArr.append(cuf)
            responseJson['timestamp'] = tsArr
            responseJson['Energy'] = energyArr
            responseJson['PR'] = prArr
            responseJson['CUF'] = cufArr
    if wst is not None and len(wst):
        wstArr = []
        for record in wst:
            irr = record.get('WSNSR')
            wstArr.append(irr)
            responseJson['Irradiance'] = wstArr
    # print(responseJson)
    data_report = Weekly(responseJson)
    weekly_data = data_report.get_weekly_report()
    return jsonify(weekly_data)

@app.route('/dailyreport/', methods=['GET'])
def daily_report():
    if 'site_id' in request.args:
        siteId = int(request.args['site_id'])
    else:
        return jsonify({})

    if 'sdate' in request.args:
        startDateStr = request.args['sdate']
    else:
        return jsonify({})
    if 'edate' in request.args:
        endDateStr = request.args['edate']
    else:
        return jsonify({})

    starttimeStr = startDateStr + " 04:30:00"
    endtimeStr = endDateStr + " 20:30:00"
    startDate = dt.datetime.strptime(starttimeStr, '%Y-%m-%d %H:%M:%S')
    endDate = dt.datetime.strptime(endtimeStr, '%Y-%m-%d %H:%M:%S')

    timezone = pytz.timezone('Asia/Kolkata')
    startDate = timezone.localize(startDate)
    endDate = timezone.localize(endDate)

    startTs = startDate.strftime('%s')
    endTs = endDate.strftime('%s')

    print("Start time ", startTs)
    print("End time ", endTs)

    site = list(mongo.db.m_site.find( {"$and":[ {"site_id":siteId},]}))
    plantrecord = list(mongo.db.plant_history.find( {"$and":[ {"site_id":siteId},{"record_timestamp": { "$gte": int(startTs)}},{"record_timestamp": {"$lte": int(endTs)}}]}))
    wst = list(mongo.db.wst_history.find( {"$and":[ {"site_id":siteId},{"record_timestamp": { "$gte": int(startTs)}},{"record_timestamp": {"$lte": int(endTs)}}]}))

    responseJson = {}
    if site is not None:
        for name in site:
            nameArr = []
            if name['site_id'] == siteId:
                data = name.get('site_name')
                nameArr.append(data)
                responseJson['site_Name'] = nameArr
    if plantrecord is not None and len(plantrecord) > 0:
        tsArr = []
        energyArr = []
        for plant in plantrecord:
            ts = plant.get('record_time')
            todayenergy = plant.get('p_today_energy')
            tsArr.append(ts)
            energyArr.append(todayenergy)
            responseJson['timestamp'] = tsArr
            responseJson['Energy'] = energyArr
    responseJson = {}
    if site is not None:
        for name in site:
            nameArr = []
            if name['site_id'] == siteId:
                data = name.get('site_name')
                nameArr.append(data)
                responseJson['site_Name'] = nameArr
    if plantrecord is not None and len(plantrecord) > 0:
        tsArr = []
        energyArr = []
        prArr = []
        cufArr = []
        for plant in plantrecord:
            ts = plant.get('record_time')
            todayenergy = plant.get('p_today_energy')
            pr = plant.get('p_pr')
            cuf = plant.get('p_cuf')
            tsArr.append(ts)
            energyArr.append(todayenergy)
            prArr.append(pr)
            cufArr.append(cuf)
            responseJson['timestamp'] = tsArr
            responseJson['Energy'] = energyArr
            responseJson['PR'] = prArr
            responseJson['CUF'] = cufArr
    if wst is not None and len(wst):
        wstArr = []
        for record in wst:
            irr = record.get('irradiation')
            wstArr.append(irr)
            responseJson['Irradiance'] = wstArr
    # print(responseJson)
    data_report = Daily(responseJson)
    daily_data = data_report.get_daily_report()
    return jsonify(daily_data)

app.run(host="0.0.0.0")  # host to listen to all the ports
